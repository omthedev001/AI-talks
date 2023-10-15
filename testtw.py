import os 
import flask
import what3words
import webbrowser
import time
import openrouteservice as ors
import random
import dotenv
client = ors.Client(key='5b3ce3597851110001cf62488603f4ba0cbe4b149200076a33b1fd7b')
app = flask.Flask(__name__)
from wasendmessage import sendMessage,sendQr
geocoder = what3words.Geocoder('S63QZKOR')

sayhi = False
sendlink = False
getlocation = False
@app.route('/whatsapp', methods = ['GET','POST'])
def whatsapp():
    print(flask.request.get_data())
    message = flask.request.form['Body']
    number = flask.request.form['From']
    name = flask.request.form['ProfileName']
    print(f'message---> {message}')
    print(f'sender---->{number}')
    print(f'Name------>{name}')
    

    
    if message.count(".") == 2:
        sendMessage(number,"Getting your location...")
        res = geocoder.convert_to_coordinates(message)
        lat = res['square']['southwest']['lat']
        lng = res['square']['southwest']['lng']
        webbrowser.open('https://www.google.com/maps/dir/' + '21.2058006,81.6587798' + '/' + str(lat) + ',' + str(lng) + '/' + '@' + str(lat) + ',' + str(lng) + ',17z/am=t/data=!3m1!4b1!4m5!4m4!1m1!4e1!1m0!3e0')
        lat = float(lat)
        lng = float(lng)
        print(lng,lat)
        random_time = random.randint(3,9)
        
        coords = [[81.6587798,21.2058006], [lng,lat]]

        route = client.directions(coordinates=coords,
                          profile='driving-car',
                          format='geojson')

        duration = (route['features'][0]['properties']['summary']['duration'])
        print(route)
        duration = int(duration / 60)
        print (f'Duration: {duration} minutes')
        sendMessage(number,f'Dont need to worry {name},Your Ambulance would arrive in {duration} -- {duration + random_time} minutes')
        sendMessage(number,"After the ambulance arrives you may complete the formalities and then also pay the charges through the 'QR code")
        sendQr(number)

    else:
        sendMessage(number,f'Hello There {name},thanks for contacting our panick messaging service\nTo start click on the link below\nThen send us the 3 words')
        time.sleep(2)
        sendMessage(number,"https://what3words.com\nPlease send us the real words")
    return'200'

if __name__ == "__main__":
    app.run(port=5000,debug=True)
    
