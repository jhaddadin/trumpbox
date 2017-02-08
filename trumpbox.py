import urequests
import time

def insert_newlines(string, every=64):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

def subs(string):
    string = string.replace('January', 'Jan.')
    string = string.replace('February', 'Feb.')
    string = string.replace('August', 'Aug.')
    string = string.replace('September', 'Sept.')
    string = string.replace('October', 'Oct.')
    string = string.replace('November', 'Nov.')
    string = string.replace('December', 'Dec.')
    return string

def get_tweet():
    global created
    global tweet
    global created2
    global tweet2
    latest = urequests.get('https://api.thingspeak.com/channels/218968/feeds.json?results=2').json()
    tweet = insert_newlines(latest['feeds'][1]['field1'].replace("'", ""), every=16)
    created = latest['feeds'][1]['field2'].replace(', 2017 at ', '\n')
    created = subs(created)
    tweet2 = insert_newlines(latest['feeds'][0]['field1'].replace("'", ""), every=16)
    created2 = latest['feeds'][0]['field2'].replace(', 2017 at ', '\n')
    created2 = subs(created2)
    
def scrolltweet(hw, string):
    hw.oled.contrast(255)
    for i in range(12):
        hw.oled.fill(0)
        hw.inc14.set_textpos((64-(17*i)),0)
        hw.inc14.printstring(string)
        hw.oled.show()
    

def showtime(hw, string):
    hw.oled.fill(0)
    hw.oled.contrast(0)
    hw.free20.set_textpos(0,0)
    hw.free20.printstring(string)
    hw.oled.show()
    for i in range(255):
        hw.oled.contrast(i)
        time.sleep(0.005)
    time.sleep(7)
    for i in range(255):
        hw.oled.contrast(255-i)
        time.sleep(0.005)
    hw.oled.fill(0)
    hw.oled.show()

def blather(hw):
    while True:
        get_tweet()
        for i in range(20):
            showtime(hw, created)
            scrolltweet(hw, tweet)
            showtime(hw, created2)
            scrolltweet(hw, tweet2)
        
    

