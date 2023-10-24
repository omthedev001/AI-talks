# importing Libs
from twilio.rest import Client
import flask
import openrouteservice as ors
import what3words as w3w
import time 
import random
import os
from datetime import datetime
import pyrebase
import folium 

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
# create map for example
map= folium.Map(location=[81.6587798,21.2058006], tiles='cartodbpositron', zoom_start=15)
hospital_list =[]
#creating a list of ambulance coordinates

pickup_points = [[[81.650402,21.211172],"Om:+919752893365"],
                [[81.637685,21.227515],"Rajiv:+919752893365"],
                [[81.658727,21.205652],"Raju:+919752893365"],
                [[81.657879,21.271156],"Pramod:+919752893365"],
                [[81.670563,21.210926],"Darsh:+919752893365"]]

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
                                  media_url='https://omthedev001.github.io/cheems.png.png',
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
            message.split(',')
            SendMsg(number,"Getting Your Location....... ")
            res = w3w_geocoder.convert_to_coordinates(message[0])
            lat = res['square']['southwest']['lat']
            lng = res['square']['southwest']['lng']
            print(lng,lat)
            folium.Marker([lat,lng],popup="Patients location",icon=folium.Icon(color='Green'),tooltip="click").add_to(map)
            # webbrowser.open('https://www.google.com/maps/dir/' + '21.2058006,81.6587798' + '/' + str(lat) + ',' + str(lng) + '/' + '@' + str(lat) + ',' + str(lng) + ',17z/am=t/data=!3m1!4b1!4m5!4m4!1m1!4e1!1m0!3e0')
            lat = float(lat)
            lng = float(lng)
            random_time = random.randint(2,8)
            route_durations = []
            for points in pickup_points:
                coords_temp = [points[0],[lng,lat]]
                route_temp = ors_client.directions(coordinates=coords_temp,
                              profile='driving-car',
                              format='geojson')
                duration_temp = route_temp['features'][0]['properties']['summary']['duration']
                route_durations.append(duration_temp)
                shortest_duration_index = route_durations.index(min(route_durations))

                # Get the coordinates and duration of the shortest route
                shortest_duration_coordinates = [pickup_points[shortest_duration_index]]
                shortest_duration = route_durations[shortest_duration_index]
                folium.Marker(list(reversed(shortest_duration_coordinates[0][0])),popup="Starting point.Ambulance confirms to pick up the patient",icon=folium.Icon(color='Red'),tooltip="click").add_to(map)
                

                 
                

            coords =[shortest_duration_coordinates[0][0],[lng,lat]]
            route = ors_client.directions(coordinates=coords,
                              profile='driving-car',
                              format='geojson')
            print(route)
            duration = (route['features'][0]['properties']['summary']['duration'])
            duration = (duration / 60)
            duration = int(duration)
            geojson = geojson = {"type": "point", "coordinates": [lng,lat]}
            pois = ors_client.places(request='pois',
                                     geojson=geojson,
                                     buffer=2000,
                                     filter_category_ids=[206])
            folium.Circle(radius=2000, location=coords, color='green').add_to(map)
            index = 0
            for poi in pois['features']:
                hospitals = poi['properties']['osm_tags']['name']
                coords1 = poi['geometry']['coordinates']
    
                coords2 = [[81.6587798,21.2058006],coords1]
    
                route = ors_client.directions(coordinates=coords2,
                                            profile='driving-car',
                                            format='geojson')
                # print(route)
                duration1 = (route['features'][0]['properties']['summary']['duration'])
                hospital_list[index]={}
                hospital_list[index]['name']=hospitals
                hospital_list[index]['duration']=duration1
                hospital_list[index]['coords']=coords1
                hospital_list[index]['coords_rev']= list(reversed(coords1))

                print(f'{hospitals},{duration}')
                folium.Marker(location=list(reversed(poi['geometry']['coordinates'])),
                              icon=folium.Icon(color='Orange'),
                              popup=folium.Popup(poi['properties']['osm_tags']['name'])).add_to(map)
                print(list(reversed(coords1)))
                index = index+1
            folium.Marker([81.6587798,21.2058006],popup="Starting point.Ambulance confirms to pick up the patient",icon=folium.Icon(color='Blue'),tooltip="click").add_to(map)
            
            print(f'Duration----> {duration}')
            time.sleep(1)
            
            SendMsg(number,"Got it!")
            time.sleep(0.5)
            SendMsg(number,f"Dont Worry {name}, Your Ambulance Would Be Arriving in\n{duration}---{duration + random_time} minutes and will take you to the hospital")
            time.sleep(0.5)
            SendMsg(number,"Your driver's number is --------- ")
            SendMsg(number,"The ambulance will take you to this hospital which is ----minutes away")

            
            time.sleep(2)
            SendQr(number)
            
            
            extracted_name= name.encode('utf-8')
            # printing result
            print("Extracted String : " + str(extracted_name))
            
            now = datetime.now()
            number = number.split(":")
            
            record_data(name,number[1],lat,lng,duration)
            
        except Exception:
            SendMsg(number,"Something went wrong please try again by saying hi,please check if you have filled the details correctly")
            
        
    else:
        SendMsg(number,f'Hey there {name}!,\nThanks for contacting our panic messaging service.\nTo begin you may click on the link below and send the three words on the top along with the type of ambulanceseperated with a comma from the following\n1.Basic Ambulances\n2.Advanced Life Support Ambulances
        \n3.Mortuary Ambulances
        \n4.Air Ambulances
        \n5.Neonatal Ambulances
        \n6.Patient Transfer Ambulances\nExample =alien.wages.pepper,Basic Ambulances')
        time.sleep(1)
        SendMsg(number,'https://www.what3words.com\n Make sure to send the correct information and have a good internet connection')
    return'200'
if __name__ == "__main__":
    app.run(port=5000,debug=True)
