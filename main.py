# importing Libs
from twilio.rest import Client
from collections.abc import Mapping 
import flask
import openrouteservice as ors
import what3words as w3w
import time
import webbrowser 
import random
import os
from datetime import datetime
import pyrebase

# Declaring vars
acc_sid = os.environ.get('TWILIO_ACCOUNT_SID')
acc_auth = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_number = os.environ.get('TWILIO_WHATSAPP')
ors_key = os.environ.get('ORS_KEY')
w3w_key = os.environ.get('W3W_KEY')
# csv_path = "record.csv"

# making clients
twilio_client = Client(acc_sid,acc_auth)
ors_client = ors.Client(key=ors_key)
w3w_geocoder = w3w.Geocoder(w3w_key)
# making firebase instance
config = {
  'apiKey': "AIzaSyBhOKvH-P9nf4-_cHeAmjyOGiyI0PXsa-Y",
  'authDomain': "eahs-389407.firebaseapp.com",
  'databaseURL': "https://eahs-389407-default-rtdb.asia-soxutheast1.firebasedatabase.app",
  'projectId': "eahs-389407",
  'storageBucket': "eahs-389407.appspot.com",
  'messagingSenderId': "562115977942",
  'appId': "1:562115977942:web:82439118215677b44b9f77",
  'measurementId': "G-T0PDF2Z6P1"
}

# create app instance
app = flask.Flask(__name__)
firebase = pyrebase.initialize_app(config)
database = firebase.database()
# def to send messages and records
def record_data(name,number,lat,lng,Duration):
    now = datetime.now()
    data = {'Name':name,'Number':number,'coords':f'{lat},{lng}','Duration':Duration,'Date':now.date(),'Time':now.strftime('%H:%M:%S'),'Payment Mode':'UPI'}
    database.child('Whatsapp').child('Users').child(name).set(data)
def SendMsg(number,msg):
    response = twilio_client.messages.create(to=number,
                                  from_= twilio_number,
                                  body=msg)
    return response
def SendQr(number):
    qrres = twilio_client.messages.create(to=number,
                                  media_url='https://tring10.github.io/images/Screenshot_20230528-162436.jpg',
                                  from_=twilio_number,)
    print(qrres.sid)

# app
@app.route('/whatsapp', methods = ['GET','POST'])
def whatsapp():
    print(flask.request.get_data())
    message = flask.request.form['Body']
    number = flask.request.form['From']
    name = flask.request.form['ProfileName']
    print(f'Message----> {message}')
    print(f'Number-----> {number}')
    print(f'Name-------> {str(name)}')
    # def MakeRecord(name,number):
    #     with open(csv_path,'r+') as f:
    #         mydatalist = f.readlines()
    #         namelist = []
    #         for line in mydatalist:
    #             entry = line.split(',')
    #             namelist.append(entry[0])
    #         now = datetime.now()
    #         dtstring = now.strftime('%H:%M:%S')
    
    #         f.writelines(f'\n{name},{number},{dtstring}')
    if (message.count(".") == 2):
        try:

            SendMsg(number,"Getting Your Location....... ")
            res = w3w_geocoder.convert_to_coordinates(message)
            lat = res['square']['southwest']['lat']
            lng = res['square']['southwest']['lng']
            print(lng,lat)
            webbrowser.open('https://www.google.com/maps/dir/' + '21.2058006,81.6587798' + '/' + str(lat) + ',' + str(lng) + '/' + '@' + str(lat) + ',' + str(lng) + ',17z/am=t/data=!3m1!4b1!4m5!4m4!1m1!4e1!1m0!3e0')
            lat = float(lat)
            lng = float(lng)
            random_time = random.randint(2,8)
            coords =[[81.6587798,21.2058006],[lng,lat]]
            route = ors_client.directions(coordinates=coords,
                              profile='driving-car',
                              format='geojson')
            print(route)
            duration = (route['features'][0]['properties']['summary']['duration'])
            duration = (duration / 60)
            duration = int(duration)
            

            print(f'Duration----> {duration}')
            time.sleep(1)
            
            SendMsg(number,"Got it!")
            time.sleep(0.5)
            SendMsg(number,f"Dont Worry {name}, Your Ambulance Would Be Arriving in\n{duration}---{duration + random_time} minutes")
            time.sleep(0.5)
            SendMsg(number,"After the ambulance arrives you may pay the charges\nthrough the QR Code given below ")
            
            time.sleep(2)
            SendQr(number)
            
            
            extracted_name= name.encode('utf-8')
            # printing result
            print("Extracted String : " + str(extracted_name))
            
            now = datetime.now()
            number = number.split(":")
            
            record_data(name,number[1],lat,lng,duration)
            
        except Exception:
            SendMsg(number,"Something went wrong please try again by saying hi")
            
        
    else:
        SendMsg(number,f'Hey there {name}!,\nThanks for contacting our panic messaging service.\nTo begin you may click on the link below and send the three words on the top\nExample =alien.wages.pepper')
        time.sleep(1)
        SendMsg(number,'https://www.what3words.com\n Make sure to send the correct words and have a good internet connection')
    return'200'
if __name__ == "__main__":
    app.run(port=5000,debug=True)
