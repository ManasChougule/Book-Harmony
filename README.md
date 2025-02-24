# Book-Harmony: E-Commerce for Exchange of Pre-owned Books

![Project Demo](https://raw.githubusercontent.com/ManasChougule/Book-Harmony/master/Book-Harmony.gif)

**Book-Harmony** is an innovative web platform that revolutionizes the way people buy, sell, and exchange pre-owned books. It allows users to easily list and discover books at discounted prices, manage their personal libraries, and receive personalized book recommendations tailored to their preferences. The platform fosters a community-driven experience by enabling users to connect, chat, negotiate, and share recommendations with fellow book lovers. Unlock new reading opportunities, monetize your old books, and engage with a vibrant community of readers!

---

## 📋 **Features**
- **Authentication**: Secure login and registration for users.
- **Personalized Dashboard**: Users can register books, view registered and sold books.
- **Book Management**:
    - Register books for sale.
    - Update book prices.
    - Remove books from listings.
- **Shopping Cart**:
    - Add or remove books.
    - Proceed to payment and place orders.
- **Orders Management**: View order history, ratings, and transaction details.
- **Recommendation Engine**: Suggests books based on user preferences.
- **Search & Filters**: Easily find books by categories or keywords.
- **Chat Engine**:
    - Communicate with buyers and sellers in real-time.
- **Admin Features**:
    - Delivery management, where admin can check all the transactions
    - Verify and mark orders as delivered.

---

## 🛠️ **Tech Stack**
- **Backend**: Flask
- **Database**: Firebase Realtime Database (via Firebase Admin SDK)
- **Frontend**: HTML, CSS, JavaScript
- **Environment Configuration**: `python-dotenv`

---

## 📚 **API Endpoints**

### Authentication
- **Login**
    - `POST /login`
    - **Body:**
      ```json
      {
        "email": "user@example.com",
        "password": "securepassword"
      }
      ```

- **Register**
    - `POST /register`
    - **Body:**
      ```json
      {
        "name": "John Doe",
        "email": "user@example.com",
        "phone": "1234567890",
        "address": "123 Main St",
        "pincode": "560001",
        "password": "securepassword",
        "state": "State Name",
        "city": "City Name"
      }
      ```

### Book Management
- **Sell Book**
    - `POST /sell_book`
    - **Body:**
      ```json
      {
        "title": "Book Title",
        "author": "Author Name",
        "price": "500",
        "location": "City Name",
        "book_category": "Fiction",
        "book_description": "A brief description of the book."
      }
      ```

- **Remove Book**
    - `POST /remove_book`
    - **Body:**
      ```json
      {
        "book_id": "12345"
      }
      ```

- **Update Book Price**
    - `POST /update_price`
    - **Body:**
      ```json
      {
        "book_id": "12345",
        "new_price": "400"
      }
      ```

### Cart Management
- **Add to Cart**
    - `POST /add_to_cart`
    - **Body:**
      ```json
      {
        "book_id": "12345"
      }
      ```

- **Remove from Cart**
    - `POST /remove_from_cart`
    - **Body:**
      ```json
      {
        "book_id": "12345"
      }
      ```

### Orders Management
- **Process Order**
    - `POST /process_order`
    - **Body:**
      ```json
      {
        "bookIds": ["12345", "67890"],
        "totalPrice": "900"
      }
      ```

- **Give Rating**
    - `POST /give_rate`
    - **Body:**
      ```json
      {
        "bookId": "12345",
        "bookRating": "5"
      }
      ```

### Chat System
- **Chat with Seller**
    - `POST /chat_seller`
    - **Body:**
      ```json
      {
        "seller_id": "seller123"
      }
      ```

- **Chat with Buyer**
    - `POST /chat_buyer`
    - **Body:**
      ```json
      {
        "buyer_id": "buyer123"
      }
      ```

- **Send Message**
    - `POST /send_message`
    - **Body:**
      ```json
      {
        "message": "Hello, I am interested in your book."
      }
      ```

- **Get Messages**
    - `GET /get_messages`

- **Get Data**
    - `GET /get_data`

---

## 🚀 **Getting Started**
Follow these steps to set up and run the project locally.

### Prerequisites
1. Python 3.x
2. Firebase account with a configured Realtime Database.
3. Install necessary Python libraries:
   ```bash
   pip install flask python-dotenv firebase-admin
   ```

### Installation
```bash
git clone https://github.com/your-repo/book-harmony.git
cd book-harmony
```

### Configure environment variables & Set up Firebase
```
FIREBASE_STORAGE_BUCKET
FIREBASE_DATABASE_URL
ADMIN_PASSWORD
```
