import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from soscraper import soscrape
import time
import re

browser = webdriver.PhantomJS()
# browser = webdriver.Firefox()

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

    browser.get('http://www.google.com')
    search_field = browser.find_element_by_name('q')
    search_field.send_keys(search_string)
    search_field.send_keys(Keys.RETURN)
    time.sleep(1)
    body = browser.find_element_by_tag_name('body')
    URIs = []
    results = browser.find_elements_by_css_selector('div.g')
    askUbuntu = re.compile("http://askubuntu.com")
    stackOverflow = re.compile("http://stackoverflow.com")
    for  result in results:
        try :
            link = result.find_element_by_tag_name("a")
            href = link.get_attribute("href")
            if askUbuntu.search(href) :
                print "AU : ",href
                # URIs.append(href)

            elif stackOverflow.search(href) :
                print "SO : ",href
                URIs.append(href)
        except :
            pass
    # URIs = [obj.get_attribute('href') for obj in 
    #             browser.find_elements_by_xpath(
    #                 "//a[starts-with(@href, 'http://askubuntu.com')]")
    #         ] + [obj.get_attribute('href') for obj in 
    #             browser.find_elements_by_xpath(
    #                 "//a[starts-with(@href, 'http://stackoverflow.com')]")
    #         ]
    # URLs = []
    # for uri in URIs:
    #     if 'stackoverflow.com/questions/tagged' not in uri:
    #         URLs.append(uri)

    # print "No. of urls found : %d" %len(URIs)
    try :
        ans_list = soscrape([URIs[0]], browser, bs, time)
        # Change the above query to `soscrape(URIs, browser, bs, time)` to want the best answer by scraping all the urls
        return best_ans(ans_list)
    except :
        # print "Sorry :("
        return None