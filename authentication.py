import pyrebase
config = {
  "apiKey": "AIzaSyCs5zm4bUJsGX-pXYRbpQPqLNANrH_3Ie8",
  "authDomain": "resume-screening-b8567.firebaseapp.com",
  "databaseURL": "https://resume-screening-b8567-default-rtdb.firebaseio.com",
  "projectId": "resume-screening-b8567",
  "storageBucket": "resume-screening-b8567.appspot.com",
  "messagingSenderId": "134972310230",
  "appId": "1:134972310230:web:936cda3b0031c154433f77",
  "measurementId": "G-NRF8TL7ZJR",
  'databaseURL' : "",
}

firebase = pyrebase.initialize_app(config)
Resume_screening = firebase.auth()
db = firebase.database()

email= 'waleed@gmail.com'
password = 'asdf@123'

user = Resume_screening.create_user_with_email_and_password(email, password)
 
#user = Resume_screening.sign_in_with_email_and_password(email, password)

#info = Resume_screening.get_account_info(user['idToken'])

#Resume_screening.send_email_verification(user['id_token'])

#Resume_screening.send_password_reset_email(email)