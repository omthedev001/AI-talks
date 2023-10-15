import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('eahs-389407-1969969dec74.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://eahs-389407-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Define the event handler for data additions
def handle_data_addition(event):
    print('New data added:')
    print(event.data)  # Print the added data
    state = event.data['App']['Users']['State']
    if state == "0":
        print("calculated")
        time.sleep(1)
        state = "1"


#           
ref = db.reference('/')

# Set up the listener for data additions
ref.listen(handle_data_addition)

# Keep the program running
while True:
    pass