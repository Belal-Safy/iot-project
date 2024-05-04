import firebase_admin
from firebase_admin import credentials

# Initialize Firebase app
cred = credentials.Certificate('firebase_service_account.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-project-45ad3-default-rtdb.firebaseio.com'
})