from flask import Flask, request, render_template, jsonify

class BookHarmonyServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

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
        self.app.add_url_rule('/dashboard', 'dashboard', self.dashboard, methods=['POST'])



if __name__ == '__main__':
    server = BookHarmonyServer()
    server.run()
