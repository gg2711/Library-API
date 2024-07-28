# Book.py
from flask import jsonify
import requests
from BookExceptions import *

class Book:
    def __init__(self, ISBN, title, genre):
        self.title = title
        self.authors = ""
        self.ISBN = ISBN
        self.genre = genre
        self.publisher = ""
        self.publishedDate = ""
        self.id = None
        
        self.post()
         
    def post(self):
        google_books_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{self.ISBN}'
        try:
            response = requests.get(google_books_url)
            response.raise_for_status()  # Raise an exception for unsuccessful status codes
            google_books_data = response.json()['items'][0]['volumeInfo']
        except requests.exceptions.RequestException:
            raise ExternalAPIServiceError("Error occurred while calling the Google Books API.")
        except (KeyError, IndexError):
            raise APIBookNotFoundError(f"Book with ISBN {self.ISBN} not found in the Google Books API.")
        
        self.authors = " and ".join(google_books_data.get("authors", [])) if google_books_data.get("authors") else "missing"
        self.publisher = google_books_data.get("publisher", "missing")
        self.publishedDate = google_books_data.get("publishedDate", "missing")
        
    def json(self):
        return {
            'title': self.title,
            'authors': self.authors,
            'ISBN': self.ISBN,
            'genre': self.genre,
            'publisher': self.publisher,
            'publishedDate': self.publishedDate,
            'id': self.id
        }
    