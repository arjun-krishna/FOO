import sys
import os
import subprocess
from wit import Wit
import logging
import pickle 
# if len(sys.argv) != 2:
    # print('usage: python ' + sys.argv[0] + ' <wit-token>')
#access_token = sys.argv[1]

foldernames=["home","documents","downloads","music","pictures","Videos"]
appset1=["firefox","gedit","eclipse","vlc","emacs","matlab"]
appset2=["calculator","chess","maps","contacts","terminal"]

L = [" ","(",")","[","]","&","'","\""]

def strprocess(fname):
    for c in L :
        fname = fname.replace(c,"\\"+c)
    return fname

def get_execlist(request):
    context = request['context']
    entities = request['entities']
    # print '$$$ cont $$$'
    # print context
    # print '$$$ ent $$$'
    # print entities
    listindex = first_entity_value(entities, 'number')
    if(listindex is None) :
        print 'cont'
        print context
        context = {}
        print 'ent'
        print entities
        return context
    try :
        fname = context['musiclist'][listindex-1]
        updatedfile =strprocess(fname)
        proc = subprocess.Popen("gnome-open "+updatedfile+" * 2> /tmp/foo.unwanted >/tmp/foo.unwanted", shell=True,
          stdin=None, stdout=None, stderr=None, close_fds=True)
        context['retstmt'] = 'Sure !'

    except:
        context['retstmt'] = 'Sorry, couldn\'t catch that? Could you repeat ! It might be the case that I lost my context! \n Please give an apt command' 
    return context


def get_merge(request):
    context = request['context']
    entities = request['entities']


    tempappname = first_entity_value(entities, 'appname')
    if tempappname:
        context['AppName']=tempappname
        context['OpenApp']=True
    return context


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    if isinstance(val, dict):
        return val['value']
    else:
        return val
    #return val['value'] if isinstance(val, dict) else val

def send(request, response):
    print(response['text'])

def get_playsong(request):
    #print request
    #print "##################################"
    context = request['context']
    #print context
    #print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    entities = request['entities']
    entnum=first_entity_value(entities, 'number')
    if entnum:
        return get_execlist(request)
    # print request
    # print entities
    mname = first_entity_value(entities, 'musictitle')
    context={}
    if mname:
        #flist=os.system("find ~/Music ~/Videos | grep -i \""+mname+"\" ")
        command="find ~/Music ~/Videos | grep -i \""+mname+"\" | grep -e .mp3 -e .mp4 -e .vlc -e .avi"
        print command
        process1 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        flist=process1.communicate()
        # print flist
        # print "#################"
        newlist=flist[0].split('\n')
        newlist.pop()
        context['count'] =len(newlist) 
        context['musicname'] = mname
        s = ""
        i = 1
        for elem in newlist :
            s += str(i)+'. '+elem+'\n'
            i += 1
        context['musiclist']=newlist
        context['displaylist']=s
        # print "Trying to open "+opencmdname
        if context['count'] is 0 :
            context = {}
            context['missingFile'] = True
        elif context['count'] is 1 :
            del context['count']
            context['oneFile'] = True
            print '$'
            print context

    else:
        context['missingFile'] = True
        if context.get('typename') is not None:
            del context['typename']

    return context        
    #loc = first_entity_value(entities, 'location')



def get_appopen(request):
    context = request['context']
    # print context
    #entities = request['entities']
    checkcon=context['OpenApp']
    loc=""
    if checkcon:
        loc=context['AppName']
    #loc = first_entity_value(entities, 'appname')
    val1=appset1.count(loc)
    updatedloc=loc
    cv=0
    if(val1<=0):
        val2=appset2.count(loc)
        if(val2<=0):
            #print "something wrong by wit!!!!"
            context['retstmt']="Looks like there is no application with the name "+loc
            return context
        else:
            listind=appset2.index(loc)
            updatedloc=appset2[listind]
            cv=2
    else:
        listind=appset1.index(loc)
        updatedloc=appset1[listind]
        cv=1
    if updatedloc:
        context['retstmt'] ="I have opened "+updatedloc+" !!"
        command=""
        if(cv==1):
            command=updatedloc            
        if(cv==2):
            command="gnome-"+updatedloc
        proc = subprocess.Popen(command+" * 2> /tmp/foo.unwanted >/tmp/foo.unwanted", shell=True,
          stdin=None, stdout=None, stderr=None, close_fds=True)

    else:
        context['missingLocation'] = True
        if context.get('retstmt') is not None:
            del context['retstmt']
    # print context
    return context 

def get_deleteContext(request) :
    context = request['context']
    context = {}
    return context

def get_execBool(request) :
    context = request['context']
    entities = request['entities']
    # print context
    # print entities
    listindex = 1
    try :
        fname = context['musiclist'][listindex-1]
        updatedfile =strprocess(fname)
        proc = subprocess.Popen("gnome-open "+updatedfile, shell=True,
          stdin=None, stdout=None, stderr=None, close_fds=True)
    except:
        pass # can capture a error if we want
    context = {}
    return context

actions = {
    'send': send,
    'MyAppOpen': get_appopen,
    'MyPlaySong':get_playsong,
    'MyExecList':get_execlist,
    'MyDeleteContext': get_deleteContext,
    'MyExecBool' : get_execBool,
    'Merge'      : get_merge,
    }

client = Wit(access_token="UBTCYTFGDP3K3DJIGRV462NLNG2MM4I7", actions=actions)
# # client.interactive()
client.logger.setLevel(logging.WARNING)
# #resp = client.message('play katy')
# print('Yay, got Wit.ai response: ' + str(resp))
# f = open('file.txt')

session_id = 'f0607fe6-aa6f-11e6-b121-3417eb627e2d'
context = pickle.load(open('context.pkl', "r"))
file = open('file.txt', 'r')
query = file.read()
file.close()
context = client.run_actions(session_id, query , context)
# context = client.run_actions(session_id, 'yes', context)
# print('The session state is now: ' + str(context))
pickle.dump(context, open('context.pkl','w'))

#resp = client.converse('my-user-session-42', 'play katy', {})
#print('Yay, got Wit.ai response: ' + str(resp))
#resp = client.converse('my-user-session-42', 'play panjaa', {})
#print('Yay, got Wit.ai response: ' + str(resp))
# def chat_bot( client, context, session_id, query):
	# context = client.run_actions(session_id, query, context)
