import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from soscraper import soscrape
import time

#browser = webdriver.PhantomJS()


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

    browser = webdriver.PhantomJS()
    browser.set_window_size(1280, 720)
    browser.get('https://www.google.com')
    time.sleep(1)
    search_field = browser.find_element_by_name('q')
    search_field.send_keys('site: stackoverflow.com ' + search_string)
    search_field.send_keys(Keys.RETURN)
    time.sleep(1)
    body = browser.find_element_by_tag_name('body')
    print "_____________________________body: "
    print body.text

    print "\n___________________find_elements_by_xpath_________________"
    print browser.find_elements_by_xpath(
                    "//a[starts-with(@href, 'http://stackoverflow.com')]")

    URIs = [obj.get_attribute('href') for obj in 
                browser.find_elements_by_xpath(
                    "//a[starts-with(@href, 'http://stackoverflow.com')]")
            ]
    print "\n_________________________URIs_____________________"
    print URIs

    URLs = []
    for uri in URIs:
        if 'stackoverflow.com/questions/tagged' not in uri:
            URLs.append(uri)

    print "No. of urls found : %d" %len(URLs)

    ans_list = soscrape(URLs, browser, bs, time)
    browser.quit()
    return best_ans(ans_list)
