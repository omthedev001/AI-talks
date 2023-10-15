import openrouteservice as ors
import folium
import csv

client = ors.Client(key="5b3ce3597851110001cf62488603f4ba0cbe4b149200076a33b1fd7b")
geojson = {"type": "point", "coordinates": [81.6582986,21.2093663]}
coordinates = [21.2093663,81.6582986]

# places of interest
pois = client.places(request='pois',
                     geojson=geojson,
                     # buffer searches (in meters) around specified point
                     
                     buffer=1000,
                    #  hospital: 206, restaurant: 570
                     filter_category_ids=[206])


for poi in pois['features']:
    holpitals = poi['properties']['osm_tags']['name']
    coordinates_hospitals = list(poi['geometry']['coordinates'])
    coords = [[81.6587798,21.2058006],coordinates_hospitals]
    print(holpitals)
    print(coords)
    route = client.directions(coordinates=coords,
                              profile='driving-car',
                              format='geojson')
    # duration = (route['features'][0]['properties']['summary']['duration'])
    
    duration = (route['features'][0]['properties']['summary']['duration'])
       
    duration = int(duration / 60)
    
    print (f'Duration: {duration} minutes')
    

# # 

# map_pois = folium.Map(location=coordinates, tiles='cartodbpositron', zoom_start=14)

# # add center point
# folium.Marker(coordinates, icon=folium.Icon(color='red')).add_to(map_pois)

# # add search area circle
# folium.Circle(radius=2000, location=coordinates, color='green').add_to(map_pois)

# # add markers to map
# for poi in pois['features']:
#     folium.Marker(location=list(reversed(poi['geometry']['coordinates'])),
#                   icon=folium.Icon(color='blue'),
#                   popup=folium.Popup(poi['properties']['osm_tags']['name'])).add_to(map_pois)

# # display map
# map_pois