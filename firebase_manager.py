import firebase_admin
from firebase_admin import credentials, auth, db, storage
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access variables
storage_bucket = os.getenv("FIREBASE_STORAGE_BUCKET")
database_url = os.getenv("FIREBASE_DATABASE_URL")

class FirebaseManager:
	def __init__(self):
		cred = credentials.Certificate('key.json')
		firebase_admin.initialize_app(cred, {
			'storageBucket': storage_bucket,
			'databaseURL': database_url
		})

    def generate_sha_password(self, password):
        sha_password = hashlib.sha256(password.encode()).hexdigest()
        return sha_password

    def register_user(self, email, password, fullname, address, phone, pincode, state, city):
		try:
			# Create user with email and password
			user = auth.create_user(
				email=email,
				password=password
			)
	        
			# Save additional user details to Realtime Database
			user_ref = db.reference('Users').child(user.uid)
			user_ref.set({
				'email': email,
				'password': self.generate_sha_password(password),
				'name': fullname,
				'address': address,
				'phone': phone,
				'pincode': pincode,
				'state': state,
				'city': city
			})
	        
			return user	

		except firebase_admin._auth_utils.EmailAlreadyExistsError:
			return None


	def login_user(self, email, password):
		try:
			user = auth.get_user_by_email(email)

			# Reference to your Firebase Realtime Database
			ref = db.reference(f'Users/{user.uid}/password')

			# Retrieve data
			data = ref.get()

			if self.generate_sha_password(password) in data:
				return user

			print(f'[*] Data : {data}')
			# If no exception is raised, the user exists
			# Now, we try to sign in with the provided credentials
			# user = auth.sign_in_with_email_and_password(email, password)
			# Redirect to a success page
		except Exception as e:
			# Redirect back to the login page with an error message
			print(f'[*] Error {e}')

		return None

	def get_user_data(self, user):

		# Reference to your Firebase Realtime Database
		ref = db.reference(f'Users/{user.uid}')

		# Retrieve data
		data = ref.get()

		return data


	def fetch_books(self):
		ref = db.reference('Books')
		return ref.get()
