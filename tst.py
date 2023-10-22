import openrouteservice as ors
import os
import folium
ors_key = os.environ.get('ORS_KEY')

ors_client = ors.Client(key=ors_key)

coords =[[81.6587798,21.2058006],[81.654631,21.204669],[81.655994,21.207267]]
route = ors_client.directions(coordinates=coords,
                              profile='driving-car',
                              format='geojson')
print(route)
duration = (route['features'][0]['properties']['summary']['duration'])
print(duration)
map = folium.Map(location=[21.20,81.65],zoom_start=10)
folium.GeoJson(route,name='route').add_to(map)
folium.LayerControl().add_to(map)
map.save('map.html')