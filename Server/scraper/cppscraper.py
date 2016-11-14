import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from soscraper import soscrape
import time
import re
#browser = webdriver.PhantomJS()
browser = webdriver.Firefox()

def best_ans(answers):
    upvts = 0
    best = None
    for ans in answers:
        acc = ans['accepted_ans']
        if acc:
            if acc['upvotes'] > upvts:
                best = ans
                upvts = acc['upvotes']
        elif not best:
            best = ans

    return best

def googlescrape(search_string):
	# do the search
	# in the top 10 results, choose best stackoverflow/askubuntu/whatever site's answer
	# Now, scrape the required page for info
	# get relevant data from the question + answer in the following format,
	# this is an incomplete version, please add additional relevant info to the object
	# stackoverflowresult {
	# 	"question" : String,
	# 	"link"  : String
        #       "accepted_ans" : answer,
	# 	"answers" : [
	# 		answerStruct
	# 	],

	# }

	# answerStruct {
	# 	text : "String",
	# 	upvotes : Integer,
	# 	has_exec_code : Boolean,
	# 	exec_code : List(String)
	# }

    browser.get('https://www.google.com')
    search_field = browser.find_element_by_name('q')
    search_field.send_keys(search_string)
    search_field.send_keys(Keys.RETURN)
    time.sleep(1)
    body = browser.find_element_by_tag_name('body')

    results = browser.find_elements_by_css_selector('div.g')
    cppref = re.compile("http://en.cppreference.com")
    URIs = []
    # stackOverflow = re.compile("http://stackoverflow.com")
    for  result in results:
        try :
            link = result.find_element_by_tag_name("a")
            href = link.get_attribute("href")
            if cppref.search(href) :
                print "CPP : ",href
                URIs.append(href)
        except :
            pass
    # URLs = []
    # for uri in URIs:
    #     if 'stackoverflow.com/questions/tagged' not in uri:
    #         URLs.append(uri)
    #print "No. of urls found : %d" %len(URIs)
    #print URIs
    browser.get(URIs[0])
    content = browser.find_elements_by_class_name('t-example-code ')
    #example = content.find_element_by_class_name('t-example')
    for c in content:
       print c.text


googlescrape("vectors in c++ inside:cppreference")