def testfunc(a, b):
	return a

def get_search_string(string):
	tokens = string.split(' ')
	# get important relevant tokens
	return tokens[0]