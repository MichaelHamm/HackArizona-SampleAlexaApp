from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
from twilio.rest import TwilioRestClient

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")

def send_text(outgoing, body):
    # put your own credentials here
    ACCOUNT_SID = "AC3fa7dba82f00ec577cd9da96e50ee0f2"
    AUTH_TOKEN = "54ded7973a552d9fb6defccd3efac9ed"

    #client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    print(outgoing, body)

    #client.messages.create(
    #    to=outgoing,
    #    from_="+14807712950",
    #    body=body,
    #)

def get_headlines():
    user_pass_dict = {'user': 'sampleaccountname',
                      'passwd': 'SampleAccountPassword',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: sampleaccountname'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/worldnews/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles
    
@app.route('/')
def homepage():
    return "hi there, how ya doin?"

@ask.launch
def start_skill():
    welcome_message = 'Hi there, is this an emergency?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'Calling 911 and alerting your emergency contacts. Hold on...'
    send_text("+16025617960", "Your emergency contact is wanting to notify you.")
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'what is happening then?'
    return statement(bye_text)
    
if __name__ == '__main__':
    app.run(debug=True)
