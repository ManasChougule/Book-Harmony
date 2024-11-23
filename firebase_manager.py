import firebase_admin
from firebase_admin import credentials, auth, db, storage
import hashlib
import datetime
import os

import string
import random

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
		
	def generate_random_id(self):
		chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
		return ''.join(random.choice(chars) for _ in range(6))

	def generate_sha_password(self, password):
		sha_password = hashlib.sha256(password.encode()).hexdigest()
		return sha_password
	
	def generate_sha(self, password):
		sha = hashlib.sha256(password.encode()).hexdigest()
		return sha
	
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
	
	def add_book(self, user, title, author, price, location, description, category, cover_img):
		try:
			bucket = storage.bucket()

			cover_img.save(cover_img.filename)

			# Generate timestamp
			timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

			# Define the new file name with timestamp
			new_file_name = f"cover_image_{timestamp}.jpg"

			blob = bucket.blob(new_file_name)
			blob.upload_from_filename(cover_img.filename)
			cover_url = blob.public_url

			book_id = self.generate_random_id()

			# Save additional user details to Realtime Database
			book_ref = db.reference('Books').child(book_id)
			book_ref.set({
				'id': book_id,
				'title': title,
				'author': author,
				'price': price,
				'cover_url': cover_url,
				'filename': new_file_name,
				'location': location,
				'description': description,
				'category': category,
				'seller' : user.uid
			})

			user_ref = db.reference('Users').child(user.uid).child('Books').child(book_id)
			user_ref.set({
				'id': book_id,
				'title': title,
				'author': author,
				'price': price,
				'cover_url': cover_url,
				'filename': new_file_name,
				'location': location,
				'seller' : user.uid
			})

			os.remove(cover_img.filename)

			return True

		except Exception as err:
			print(f'[*] Err {err}')
		
		return False
	
	def	update_book_price(self, user, book_id, book_price):
		user_ref = db.reference('Users').child(user.uid).child('Books').child(book_id)

		# Update the node
		new_data = {
		    'price': book_price
		}

		book_ref = db.reference('Books').child(book_id)

		user_ref.update(new_data)
		book_ref.update(new_data)
		
	def fetch_transaction(self):
		ref = db.reference('Delivery')
		return ref.get()

	def fetch_books(self):
		ref = db.reference('Books')
		return ref.get()
	
	def fetch_cart_books(self, user):
		ref = db.reference('Users').child(user.uid).child('Cart')
		return ref.get()
	
	def fetch_mybooks(self, user):
		ref = db.reference('Users').child(user.uid).child('Books')
		return ref.get()
	
	def fetch_specific_books(self, book_id):
		ref = db.reference('Books').child(book_id)
		
		seller_ref = db.reference('Books').child(book_id).child('seller')
		seller_id = seller_ref.get()

		seller_ref = db.reference('Users').child(seller_id).child('name')
		seller_name = seller_ref.get()

		new_data = {'seller_name': seller_name}
		ref.update(new_data)
		return ref.get()
	
	def fetch_orders(self, user):
		order_ref = db.reference('Users').child(user.uid).child('Orders')
		orders = order_ref.get()
		new_orders = {}
		if orders:
			for key, value in orders.items():
				t_ref = db.reference('Delivery').child(key)
				new_orders[key] = t_ref.get()
			return new_orders
		else:
			return None
		
	def fetch_purchase_orders(self, user):
		ref = db.reference('Users').child(user.uid).child('Purchase')
		return ref.get()
	
	def fetch_buyers(self, user):
		buyers_ref = db.reference('Chats').child(user.uid)
		return buyers_ref.get()
	
	def get_image(self, filename):
		if os.path.exists(f'static/cover/{filename}'):
			pass
		else:
			bucket = storage.bucket()
			# Download the image
			blob = bucket.blob(filename)
			blob.download_to_filename(f'static/cover/{filename}')
			
	def is_node_present(self, node_path):
		ref = db.reference(node_path)
		snapshot = ref.get()
		return snapshot is not None
	
	def delete_node(self, path):
		node_ref = db.reference(path)
		node_ref.delete()
	
	def add_to_users_cart(self, user, book_id):
		user_ref = db.reference('Users').child(user.uid).child('Cart').child(book_id)
		user_ref.set({
			'id': book_id
		})
		
	def give_rate(self, user, bookId, bookRating):
		book_ref = db.reference('Books').child(bookId).child('Ratings')
		book_ref.update({
			user.uid: bookRating
		})

		rating_ref = db.reference('Books').child(bookId).child('bookrating')
		if rating_ref.get():
			rating = rating_ref.get()

			rating_avg = ((int(bookRating) + int(rating)) / 2)

			rating_ref = db.reference('Books').child(bookId)
			rating_ref.update({
				'bookrating': rating_avg
			})
		else:
			rating_ref = db.reference('Books').child(bookId)
			rating_ref.update({
				'bookrating': bookRating
			})
			

	def purchase_transaction(self, user, node, book_ids, amount, timestamp):
		# Generate timestamp
		data = {}

		for book_id in book_ids:
			ref = db.reference('Books').child(book_id)

			# Update the node
			new_data = {
			    'purchase': True
			}

			ref.update(new_data)

			seller_ref = db.reference('Users').child('Books').child(book_id)
			seller_ref.update(new_data)

			data[book_id] = ref.get()

		user_ref = db.reference('Users').child(user.uid).child('Orders').child(node)
		user_ref.set({
			'amount': amount,
			'id': node,
			'books': data, 
			'time': timestamp
		})

		seller_data = {}

		for book_id in book_ids:
			ref = db.reference('Books').child(book_id).child('seller')
			seller_id = ref.get()

			seller_ref = db.reference('Users').child(seller_id)
			seller_data[seller_id] = seller_ref.get()

			user_ref = db.reference('Users').child(user.uid).child('name')

			seller_ref = db.reference('Users').child(seller_id).child('Purchase').child(node)
			seller_ref.set({
				'amount': amount,
				'id': node,
				'books': data, 
				'time': timestamp,
				'buyer_id': user.uid,
				'buyer_name': user_ref.get()
			})

		user_ref = db.reference('Users').child(user.uid)

		deliver_ref = db.reference('Delivery').child(node)
		deliver_ref.set({
			'amount': amount,
			'id': node,
			'books': data, 
			'seller_data': seller_data, 
			'time': timestamp,
			'buyer': user_ref.get()
		})
		
	def mark_deliver(self, tid):
		deliver_ref = db.reference('Delivery').child(tid)
		deliver_ref.update({
			'deliver': True
		})
		
    