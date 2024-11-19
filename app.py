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

    def logout(self):
        if self.user is not None:
            self.user = None

        return render_template('login.html')


if __name__ == '__main__':
    server = BookHarmonyServer()
    server.run()
