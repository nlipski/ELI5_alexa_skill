from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode


app = Flask(__name__)
ask = Ask(app,"/")

def get_info():
    user_info_dict = {
        'user':'*****',
        'passwd':'*****',
        'api_type':'json'
    }
    sess = requests.Session()
    sess.headers.update({'User-Agent':'I am testing Alexa: Sentdex'})
    sess.post('https://ssl.reddit.com/api/login', data = user_info_dict)
    time.sleep(1)
    url = 'https://google.com'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode._unidecode(listing['data']['']) for listing in data ['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles

@app.route('/')
def homepage():
    return "sample"

@ask.launch
def start_skill():
    welcome_massage = "Hello there, how are you doing?"
    return question(welcome_massage)

@ask.initent("YesIntent")
def share_headlines():
    headlines = get_info()
    headline_msg =  "The Current world news are {}".format(headlines)
    return statement(headline_msg)


@ask.initent("NoIntent")
def no_intent():
    bye_text = "bye,bye..."
    return statement(bye_text)


if __name__ == '__main__':
    print(get_info())
    #app.run(debug=True)
