import sys
import os
import subprocess
from wit import Wit
import logging
from googlelinks import wiki_info

# if len(sys.argv) != 2:
#     print('usage: python ' + sys.argv[0] + ' <wit-token>')
#access_token = sys.argv[1]

foldernames=["home","documents","downloads","music","pictures","Videos"]
appset1=["firefox","gedit","eclipse","vlc","emacs","matlab"]
appset2=["calculator","chess","maps","contacts","terminal"]

L = [" ","(",")","[","]","&","'","\""]

def strprocess(fname):
    for c in L :
        fname = fname.replace(c,"\\"+c)
    return fname

def get_newexeclist(request):
    context = request['context']
    entities = request['entities']
    # print '$$$ cont $$$'
    # print context
    # print '$$$ ent $$$'
    # print entities
    listindex = first_entity_value(entities, 'number')
    if(listindex is None) :
        #print 'cont'
        #print context
        context = {}
        context['retstmt']="Sorry! unable to open that music file"
        #print 'ent'
        #print entities
        return context
    try :
        fname = context['musiclist'][listindex-1]
        updatedfile =strprocess(fname)
        proc = subprocess.Popen("gnome-open "+updatedfile+" * 2> /tmp/foo.unwanted >/tmp/foo.unwanted", shell=True,
          stdin=None, stdout=None, stderr=None, close_fds=True)
        context['retstmt'] = 'Sure Sucess!'

    except:
        context['retstmt'] = 'Sorry, couldn\'t catch that? Could you repeat ! It might be the case that I lost my context! \n Please give an apt command' 
    return context

def get_fileexeclist(request):
    context = request['context']
    entities = request['entities']
    # print '$$$ cont $$$'
    # print context
    # print '$$$ ent $$$'
    # print entities
    listindex = first_entity_value(entities, 'number')
    
    val=10
    if context.has_key("filelist"):
        val=len(context['filelist'])
     
    if(val>10):
        val=10
    if(listindex<=0 or listindex>10):
        #context['fileretstmt']="Please choose a number between 1 and "+str(val)
        context['fileretstmt']="Sorry! unable to open that file"
        #print context
        return context
    if(listindex is None) :
        #print 'cont'
        #print context
        context = {}
        context['fileretstmt']="Sorry! unable to open that file"
        #print 'ent'
        #print entities
        return context
    try :
        fname = context['filelist'][listindex-1]
        updatedfile =strprocess(fname)
        proc = subprocess.Popen("gnome-open "+updatedfile+" * 2> /tmp/foo.unwanted >/tmp/foo.unwanted", shell=True,
          stdin=None, stdout=None, stderr=None, close_fds=True)
        context['fileretstmt'] = 'Sure Sucess!'

    except:
        context['fileretstmt'] = 'Sorry, couldn\'t catch that? Could you repeat ! It might be the case that I lost my context! \n Please give an apt command' 
    return context    


def get_describe(request):
    context = request['context']
    #print context
    #print "$$$$$$$$$"
    context={}
    entities = request['entities']
    #print request
    #print "FDFFFFFFFFFFFFFFFFFFFFFFF"
    wikiname = first_entity_value(entities, 'wikiname')
    if wikiname:
        context['keyname']=wikiname
        result=wiki_info(wikiname)
        context['retstr']=result['url']
        context['returl']=result['data']
        #print result['url']
        #print result['data']
        #print "#######"
    return context

def get_deviceset(request):
    context = request['context']
    entities = request['entities']
    devname = first_entity_value(entities, 'devicename')
    devmode=  first_entity_value(entities, 'myon_off')
    #print devmode
    #print devname
    #print "$$$$$$$$$$$"

    if devname=="wifi":
        command="nmcli radio wifi "+str(devmode)
        proc = subprocess.Popen(command, shell=True,
          stdin=None, stdout= None, stderr=None, close_fds=True)
        context['myretstmt']="Turned "+devmode+" "+devname
        return context

    elif devname=="bluetooth":
        mystr=str(devmode)
        if mystr=="on":
            typestr="unblock"
        else:
            typestr="block"
        command="rfkill "+typestr+" bluetooth"
        proc = subprocess.Popen(command, shell=True,
          stdin=None, stdout= None, stderr=None, close_fds=True)
        context['myretstmt']="Turned "+str(devmode)+" "+devname
        return context
        


    context['myretstmt']="Sorry! Could you please ask properly"
    return context 


def get_merge(request):
    context = request['context']
    entities = request['entities']


    tempappname = first_entity_value(entities, 'appname')
    if tempappname:
        context['AppName']=tempappname
        context['OpenApp']=True
    return context

def get_fileopen(request):
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
    tempfname = first_entity_value(entities, 'filename')
    context={}
    if tempfname:
        #flist=os.system("find ~/Music ~/Videos | grep -i \""+mname+"\" ")
        command="find ~/Documents ~/Downloads | grep -i \""+tempfname+"\" "
        process1 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        flist=process1.communicate()
        # print flist
        # print "#################"
        newlist=flist[0].split('\n')
        newlist.pop()
        context['count'] =len(newlist) 
        context['filename'] = tempfname
        s = ""
        i = 1
        val=len(newlist)
        templist=[]
        tv=0
        vstr="So here are the 10 suggestions for you\n"
        if(val>10):
            val=10
            tv=1
        for  i in range(0,val):
            s += str(i+1)+'. '+newlist[i]+'\n'
            templist.append(newlist[i])
        context['filelist']=newlist
        context['displaylist']=s
        if(tv==0):
            context['more']=""
        else:
            context['more']=vstr
        # print "Trying to open "+opencmdname
        if context['count'] is 0 :
            context = {}
            context['missingFile'] = True
        elif context['count'] is 1 :
            del context['count']
            context['oneFile'] = True
            #print '$'
            #print context
        #print "some error"
    else:
        context['Illegal']=True
    #     if context.get('typename') is not None:
    #         del context['typename']

    return context        
    #loc = first_entity_value(entities, 'location')


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
    #return 
    #print "sollu"
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
            #print '$'
            #print context
    # else:
    #     context['missingFile'] = True
    #     if context.get('typename') is not None:
    #         del context['typename']

    return context        
    #loc = first_entity_value(entities, 'location')



def get_appopen(request):
    context = request['context']
    # print context
    entities = request['entities']
    # checkcon=""
    # if(context.has_key("OpenApp")):
    #     checkcon=context['OpenApp']
    # loc=""
    # if checkcon:
    #     loc=context['AppName']
    context={}
    loc = first_entity_value(entities, 'appname')
    if not loc:
        context['retstmt']="Sorry, couldn\'t catch that?"
    #print loc
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
        proc = subprocess.Popen(command, shell=True,
          stdin=None, stdout= open('/tmp/foo.unwanted','w'), stderr=open('/tmp/foo.unwanted2','w'), close_fds=True)

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

def get_fileexecBool(request) :
    context = request['context']
    entities = request['entities']
    # print context
    # print entities
    listindex = 1
    try :
        myfname = context['filelist'][listindex-1]
        updatedfile =strprocess(myfname)
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
    'MyNewExecList':get_newexeclist,
    'MyDeleteContext': get_deleteContext,
    'MyExecBool' : get_execBool,
    'Merge'      : get_merge,
    'MyDescribe'  : get_describe,
    'MyDeviceSet'  :get_deviceset,
    'MyFileOpen'    :get_fileopen,
    'MyFileExecBool' :get_fileexecBool,
    'MyFileExecList'  :get_fileexeclist,
    }

client = Wit(access_token="UBTCYTFGDP3K3DJIGRV462NLNG2MM4I7", actions=actions)
client.interactive()
#client.logger.setLevel(logging.WARNING)
#resp = client.message('play katy')
#print('Yay, got Wit.ai response: ' + str(resp))

# session_id = 'f0607fe6-aa6f-11e6-b121-3417eb627e2d'
# context0 = {}
# context1 = client.run_actions(session_id, 'play SAtya', context0)
# context1 = client.run_actions(session_id, '2', context1)
# print('The session state is now: ' + str(context1))


#resp = client.converse('my-user-session-42', 'play katy', {})
#print('Yay, got Wit.ai response: ' + str(resp))
#resp = client.converse('my-user-session-42', 'play panjaa', {})
#print('Yay, got Wit.ai response: ' + str(resp))
