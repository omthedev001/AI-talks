import pyrebase

# Configure your Firebase project
config = {
  'apiKey': "AIzaSyBhOKvH-P9nf4-_cHeAmjyOGiyI0PXsa-Y",
  'authDomain': "eahs-389407.firebaseapp.com",
  'databaseURL': "https://eahs-389407-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "eahs-389407",
  'storageBucket': "eahs-389407.appspot.com",
  'messagingSenderId': "562115977942",
  'appId': "1:562115977942:web:82439118215677b44b9f77",
  'measurementId': "G-T0PDF2Z6P1"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)

# Get a reference to the database
db = firebase.database()

# Define the stream callback function
def stream_handler(message):
    if message["event"] == "put":
        print("New data added:")
        print(message["data"])  # Print the added data

# Create a stream to monitor data additions
stream = db.stream(stream_handler)

# Keep the program running
while True:
    pass