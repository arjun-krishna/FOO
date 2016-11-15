# Cannot be used standalone
# Another script is needed to import required modules and work

def get_answer(obj):
    final_obj = {}
    final_obj['text'] = obj.find(class_='post-text').get_text()
    final_obj['upvotes'] = int(obj.find(class_='vote-count-post').get_text())
    try:
        codes = obj.find_all('pre', class_='prettyprint')
        code_list = []
        for code in codes:
            code_list.append(code.get_text())
        final_obj['has_exec_code'] = True
        final_obj['exec_code'] = code_list
    except:
        final_obj['has_exec_code'] = False
        final_obj['exec_code'] = None
    
    
    return final_obj

def soscrape(URLs, browser, bs, time):
    final_list = []
    for url in URLs:
        browser.get(url)
        time.sleep(1)
        soup = bs(browser.page_source, 'html.parser')

        final_obj = {'link': url}
        title = soup.find(id = 'question-header').get_text()
        question = soup.find(class_ = 'question').find(
                class_ = 'post-text').get_text()

        final_obj['title'] = title
        final_obj['question'] = question

        objs = soup.find_all(class_ = 'answer')
        if len(objs) == 0:
            continue
        i = 0
        accepted_ans = None
        if 'accepted-answer' in objs[0]['class']:
            accepted_ans = get_answer(objs[0])
            i += 1

        final_obj['accepted_ans'] = accepted_ans

        answers = []
        for obj in objs[i:]:
            ans = get_answer(obj)
            if ans: answers.append(ans)
        # final_obj['answers'] = answers
        if ans :
            if accepted_ans == None:
                final_obj['accepted_ans'] = ans[0] # better soln, upvotes max   
                final_obj['answers'] = ans[1:]         
            final_list.append(final_obj)
        else :
            final_obj['accepted_ans'] = None
            final_obj['answers'] = []
    return final_list
    
