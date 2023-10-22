import openrouteservice as ors
import os
import folium
ors_key = os.environ.get('ORS_KEY')

ors_client = ors.Client(key=ors_key)
hospital_list = {}
# coords =[[81.6587798,21.2058006],[81.654631,21.204669],[81.655994,21.207267]]
geojson = {"type": "point", "coordinates": [81.6587798,21.2058006]}
pois = ors_client.places(request = "pois",
                         geojson=geojson,
                         buffer=2000,
                         filter_category_ids=[206])
# print(pois)
for poi in pois['features']:
    hospitals = poi['properties']['osm_tags']['name']
    coords1 = poi['geometry']['coordinates']
    coords = [[81.6587798,21.2058006],coords1]
    
    route = ors_client.directions(coordinates=coords,
                              profile='driving-car',
                              format='geojson')
    # print(route)
    duration = (route['features'][0]['properties']['summary']['duration'])
    hospital_list[hospitals]=duration
    print(f'{hospitals},{duration}')
temp = min(hospital_list.values())
res = [key for key in hospital_list if hospital_list[key] == temp]
print(hospital_list)
print(f'{res[0]}:{temp}')
# route = ors_client.directions(coordinates=coords,
#                               profile='driving-car',
#                               format='geojson')
# print(route)
# duration = (route['features'][0]['properties']['summary']['duration'])
# print(duration)
# map = folium.Map(location=[21.2058006,81.6587798],zoom_start=10)
# folium.GeoJson(route,name='route').add_to(map)
# folium.LayerControl().add_to(map)
# map.save('map.html')
# n = input()
# n = n.split(',')
# location = n[0]
# injury = n[1]
# print(f'location:{location} injury:{injury}')