import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier

class BookRecommender:
    def __init__(self, book_data):
        self.books_df = self._prepare_data(book_data)
        self.encoder = OneHotEncoder()
        self.category_encoded = self.encoder.fit_transform(self.books_df[['category']])
        self.model = KNeighborsClassifier(n_neighbors=3)
        self.model.fit(self.category_encoded, self.books_df['id'])

    def _prepare_data(self, book_data):
        data = {
            'id': [],
            'title': [],
            'author': [],
            'category': [],
            'rating': []
        }

        for book_id, book_info in book_data.items():
            data['id'].append(book_id)
            data['title'].append(book_info['title'])
            data['author'].append(book_info['author'])
            data['category'].append(book_info['category'].lower())
            data['rating'].append(book_info.get('Book-Rating', 0))

        return pd.DataFrame(data)

    def recommend_books(self, categories, ratings):
        input_features = self.encoder.transform(pd.DataFrame({'category': categories}))
        similar_books = self.model.kneighbors(input_features, n_neighbors=4, return_distance=False)
        recommended_books = []
        for indices in similar_books:
            for index in indices:
                book_id = self.books_df.iloc[index]['id']
                if self.books_df.iloc[index]['rating'] >= min(ratings) and book_id not in recommended_books:
                    recommended_books.append(book_id)
        return recommended_books[:4]

'''# Example usage:
if __name__ == "__main__":
    book_data = {  # Your book data dictionary here 
    }
    recommender = BookRecommender(book_data)
    categories = ['action', 'romance']
    ratings = [4.0]
    recommended_books = recommender.recommend_books(categories, ratings)
    print("Recommended book IDs:", recommended_books)'''