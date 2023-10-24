import folium
import openrouteservice
import os
# Replace 'your_api_key' with your actual OpenRouteService API key
api_key = os.environ.get('ORS_KEY')
client = openrouteservice.Client(key=api_key)

# Specify the coordinates (latitude and longitude) of the location you're interested in
# Example coordinates for Bangalore, India
coordinates =[[81.6587798,21.2058006]]
coords =[21.2058006,81.6587798]
# isochrone
isochrone = client.isochrones(locations=coordinates,
                              range_type='time',
                              # 900 seconds, 15 minutes
                              range=[300],
                              attributes=['total_pop'])

# map
map= folium.Map(location=[25.784097, -80.127995], tiles='cartodbpositron', zoom_start=12)

# add geojson to map with population
population = isochrone['features'][0]['properties']['total_pop']
folium.GeoJson(isochrone, name='isochrone', tooltip=f'population: {population:,.0f}').add_to(map)

# add marker to map
minutes = isochrone['features'][0]['properties']['value']/60
popup_message = f'outline shows areas reachable within {minutes} minutes'
folium.Marker([21.2058006,81.6587798], popup=popup_message, tooltip='click').add_to(map)

# add layer control to map (allows layer to be turned on or off)
folium.LayerControl().add_to(map)
hospital_list = {}
# coords =[[81.6587798,21.2058006],[81.654631,21.204669],[81.655994,21.207267]]
geojson = {"type": "point", "coordinates": [81.6587798,21.2058006]}
pois = client.places(request = "pois",
                         geojson=geojson,
                         buffer=2000,
                         filter_category_ids=[206])
# print(pois)


# add center point
folium.Marker(coords, icon=folium.Icon(color='red')).add_to(map)

# add search area circle
folium.Circle(radius=2000, location=coords, color='green').add_to(map)
index = 0
for poi in pois['features']:
    hospitals = poi['properties']['osm_tags']['name']
    coords1 = poi['geometry']['coordinates']
    
    coords = [[81.6587798,21.2058006],coords1]
    
    route = client.directions(coordinates=coords,
                              profile='driving-car',
                              format='geojson')
    # print(route)
    duration = (route['features'][0]['properties']['summary']['duration'])
    hospital_list[index]={}
    hospital_list[index]['name']=hospitals
    hospital_list[index]['duration']=duration
    
    hospital_list[index]['coords']=coords1
    hospital_list[index]['coords_rev']= list(reversed(coords1))
    
    print(f'{hospitals},{duration}')
    folium.Marker(location=list(reversed(poi['geometry']['coordinates'])),
                  icon=folium.Icon(color='blue'),
                  popup=folium.Popup(poi['properties']['osm_tags']['name'])).add_to(map)
    print(list(reversed(coords1)))
    index = index+1
# temp = min(hospital_list.values())
# res = [key for key in hospital_list if hospital_list[key] == temp]
print(hospital_list)
# print(f'{res[0]}:{temp}')
print(hospital_list[0])
print(hospital_list[0]['duration'])
print(hospital_list[0]['coords_rev'])
print(hospital_list[0]['coords'])
print(hospital_list[0]['name'])
index = 0
for i in hospital_list:
    duration = hospital_list[index]['duration']
    if duration<500:
        print(hospital_list[index])
    index = index+1

# display map
map.save('map_isochrone.html')