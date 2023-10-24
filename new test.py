import openrouteservice as ors
import os
ors_key = os.environ.get('ORS_KEY')

ors_client = ors.Client(key=ors_key)

pickup_points = [[[81.650402,21.211172],"om"],
                [[81.637685,21.227515],"om"],
                [[81.658727,21.205652],"om"],
                [[81.657879,21.271156],"om"],
                [[81.670563,21.210926],"om"]]
route_durations = []
coords = [21.215733, 81.636802]
for points in pickup_points:
                coords_temp = [points[0],list(reversed(coords))]
                route_temp = ors_client.directions(coordinates=coords_temp,
                              profile='driving-car',
                              format='geojson')
                duration_temp = route_temp['features'][0]['properties']['summary']['duration']
                route_durations.append(duration_temp)
shortest_duration_index = route_durations.index(min(route_durations))

# Get the coordinates and duration of the shortest route
shortest_duration_coordinates = [pickup_points[shortest_duration_index]]
shortest_duration = route_durations[shortest_duration_index]

# Print the shortest route coordinates and duration
print("Shortest Route Coordinates:", shortest_duration_coordinates[0][0])
print("Driver name:",shortest_duration_coordinates[0][1])
print("Shortest Duration (in minutes):", (shortest_duration/60))