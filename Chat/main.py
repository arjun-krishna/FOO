from wit import Wit

def send(request, response):
    print('Sending to user...', response['text'])
def my_action(request):
    print('Received from user...', request['text'])

actions = {
    'send': send,
    'my_action': my_action,
}
access_token = 'FFODPCAPXPE7W2D7QLDH7WADWHERT5LQ'

client = Wit(access_token=access_token, actions=actions)

resp = client.message('what is the weather in London?')
print('Yay, got Wit.ai response: ' + str(resp))
