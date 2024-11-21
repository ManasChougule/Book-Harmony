from flask import Flask, request, render_template, jsonify
from firebase_manager import FirebaseManager
import datetime

class BookHarmonyServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.manager = FirebaseManager()

        # New User
        self.user = None

        # Seller Id
        self.seller = None

        # Buyer Id
        self.buyer = None 

    def setup_routes(self):
        # Index Page
        self.app.add_url_rule('/', 'index', self.index_page)

        # Login Page
        self.app.add_url_rule('/login', 'login_page', self.login_page)
        self.app.add_url_rule('/login', 'login', self.login, methods=['POST'])

        # Register Page
        self.app.add_url_rule('/register', 'register_page', self.register_page)
        self.app.add_url_rule('/register', 'register', self.register, methods=['POST'])

        # User Dashboard Page
        self.app.add_url_rule('/dashboard', 'dashboard_page', self.dashboard_page)

        # Sell Book
        self.app.add_url_rule('/sell_book', 'sell_book', self.sell_book, methods=['POST'])

        # Remove Book
        self.app.add_url_rule('/remove_book', 'remove_book', self.remove_book, methods=['POST'])

        # Update Book Price
        self.app.add_url_rule('/update_price', 'update_price', self.update_price, methods=['POST'])

        # Cart Page
        self.app.add_url_rule('/cart', 'cart_page', self.cart_page)
        self.app.add_url_rule('/add_to_cart', '/add_to_cart', self.add_to_cart, methods=['POST'])
        self.app.add_url_rule('/remove_from_cart', 'remove_from_cart', self.remove_from_cart, methods=['POST'])

        # Orders Page
        self.app.add_url_rule('/orders', 'orders_page', self.orders_page)
        self.app.add_url_rule('/give_rate', 'give_rate', self.give_rate, methods=['POST'])

        # Payment Page
        self.app.add_url_rule('/payment', 'payment_page', self.payment_page)

        # Process Order
        self.app.add_url_rule('/process_order', 'process_order', self.process_order, methods=['POST'])

        # Logout
        self.app.add_url_rule('/logout', 'logout', self.logout)

    def index_page(self):
        books = self.manager.fetch_books()

        for book_id, book_data in books.items():
            self.manager.get_image(book_data['filename'])

        return render_template('index.html', books=books, user=self.user)

    def login_page(self):
        return render_template('login.html')

    def register_page(self):
        return render_template('register.html')

    def dashboard_page(self):
        if self.user is not None:
            return render_template('dashboard.html', buyers=[])
        else:
            return render_template('login.html')

    def login(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        self.user = self.manager.login_user(email, password)

        if self.user is not None:
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'})
        
    def register(self):
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        pincode = data.get('pincode')
        password = data.get('password')

        state = data.get('state')
        city = data.get('city')

        temp_user = self.manager.register_user(email, password, name, address, phone, pincode, state, city)

        if temp_user is not None:
            return jsonify({'success': True, 'message': 'User registered successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Error registering/User alredy exists!'}) 
        
    def sell_book(self):
        # Get form data
        title = request.form.get('title')
        author = request.form.get('author')
        price = request.form.get('price')
        location = request.form.get('location')
        category = request.form.get('book_category')
        description = request.form.get('book_description')

        cover_img = request.files['coverImg']  # Uploaded cover image file

        # print(book)
        if self.manager.add_book(self.user, title, author, price, location, description, category, cover_img):
            print(f'[*] Book added to firebase')
            return jsonify({'message': 'Book successfully listed for sale!'})
        else:
            return jsonify({'message': 'Failed to add Book!'})

    def remove_book(self):
        if self.user is not None:
            data = request.json
            book_id = data.get('book_id')
            print(f'[*] Remove from List {book_id}')

            self.manager.delete_node(f'Users/{self.user.uid}/Books/{book_id}')
            self.manager.delete_node(f'Books/{book_id}')

            return jsonify({'message': 'Book removed from sale!'})
        else:
            return jsonify({'message': 'Book not exists!'})

    def update_price(self):
        if self.user is not None:
            data = request.json
            book_id = data.get('book_id')
            book_price = data.get('new_price')
            self.manager.update_book_price(self.user, book_id, book_price)
            return jsonify({'message': 'Price of book updated!'})
        else:
            return jsonify({'message': 'Book not exists!'})
        
    def cart_page(self):
        if self.user is not None:
            books = self.manager.fetch_cart_books(self.user)
            new_data = {}
            if books:
                for key, value in books.items():
                    print(f'[*] Getting Books : {key}')
                    data = self.manager.fetch_specific_books(key)
                    new_data[key] = data
            return render_template('cart.html', books=new_data)
        else:
            return render_template('login.html')
        
    def add_to_cart(self):
        if self.user is not None:
            data = request.json
            book_id = data.get('book_id')

            if self.manager.is_node_present(f'Users/{self.user.uid}/Books/{book_id}'):
                return jsonify({'message': 'Error: You cant add your own book to cart!'})

            self.manager.add_to_users_cart(self.user, book_id)
            return jsonify({'message': 'Book added to cart successfully'})
        else:
            return jsonify({'message': 'Error to add Book'})
        
    def remove_from_cart(self):
        if self.user is not None:
            data = request.json
            book_id = data.get('book_id')
            print(f'[*] Remove from cart {book_id}')
            self.manager.delete_node(f'Users/{ self.user.uid }/Cart/{ book_id }')
            return jsonify({'message': 'Book removed from cart!'})
        else:
            return jsonify({'message': 'Failed to remove book!'})
        
    def orders_page(self):
        if self.user is not None:
            orders = self.manager.fetch_orders(self.user)
            return render_template('orders.html', orders=orders)
        else:
            return render_template('login.html')
        
    def payment_page(self):
        if self.user is not None:
            books = self.manager.fetch_cart_books(self.user)
            user = self.manager.get_user_data(self.user)
            new_data = {}
            if books:
                for key, value in books.items():
                    print(f'[*] Getting Books : {key}')
                    data = self.manager.fetch_specific_books(key)
                    new_data[key] = data
            return render_template('payment.html', books=new_data, user=user)
        else:
            return render_template('login.html')

    def give_rate(self):
        data = request.json
        bookId = data.get('bookId')
        bookRating = data.get('bookRating')

        print(f'[*] Rating {bookRating} for Book ID: {bookId}')
        self.manager.give_rate(self.user, bookId, bookRating)
        return jsonify({'message': 'Rating given!'})

    def process_order(self):
        data = request.json
        book_ids = data.get('bookIds')
        total_price = data.get('totalPrice')

        timestamp = datetime.datetime.now().strftime("%Y/%m/%d_%H-%M-%S")

        node = self.manager.generate_sha(str(book_ids) + timestamp)

        self.manager.purchase_transaction(self.user, node, book_ids, total_price, timestamp)
        self.manager.delete_node(f'Users/{self.user.uid}/Cart')

        # Process the book data here
        return 'Book data received successfully!', 200
    
    def logout(self):
        if self.user is not None:
            self.user = None

        return render_template('login.html')

    def run(self):
        self.app.run(port="8080", debug=True)

if __name__ == '__main__':
    server = BookHarmonyServer()
    server.run()
