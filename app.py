from flask import Flask, request, render_template, jsonify
from firebase_manager import FirebaseManager

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

        # Cart Page
        self.app.add_url_rule('/cart', 'cart_page', self.cart_page)

        # Add to Cart
        self.app.add_url_rule('/add_to_cart', '/add_to_cart', self.add_to_cart, methods=['POST'])

        # Remove from Cart
        self.app.add_url_rule('/remove_from_cart', 'remove_from_cart', self.remove_from_cart, methods=['POST'])

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
        

    

    def logout(self):
        if self.user is not None:
            self.user = None

        return render_template('login.html')

    def run(self):
        self.app.run(port="8080", debug=True)

if __name__ == '__main__':
    server = BookHarmonyServer()
    server.run()
