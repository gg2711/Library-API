# BookClub.py
from flask import jsonify
from Book import Book
from BookExceptions import *
from bson import ObjectId
import requests
from pymongo import MongoClient
import os
import re

class BookClub:
    Genres = ["Biography", "Children", 
              "Fantasy", "Fiction", "Other", "Science", "Science Fiction"]


    def __init__(self):
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
        self.client = MongoClient(mongo_uri)
        self.db = self.client['library_db']
        self.books = self.db['books']
        self.ratings = self.db['ratings']
        self.top3 = None
       
        
    def add_book(self, ISBN, title, genre):
        if not ISBN or not title or not genre:
            raise RequiredFieldMissingError("Missing required fields.")
        if self.books.find_one({"ISBN": ISBN}):
            raise DuplicateBookError("This book is already in the book club.")
        if genre not in self.Genres:
            raise GenreNotValidError("Invalid genre.")
        else:
            new_book = Book(ISBN, title, genre)
            mongo_id = self.books.insert_one(new_book.json())
            book_id = str(mongo_id.inserted_id)
            title = new_book.title
            self.ratings.insert_one({'values': [], 'average': 0, 'title': title, 'book_id': ObjectId(book_id)})
            
            return book_id
    
    def update_book(self, book_id, update_data):
        try:
            object_id = ObjectId(book_id)
        except Exception as e:
            raise BookNotFoundError ("Invalid ID Format")
        isbn = update_data.get("ISBN")
        title = update_data.get("title")
        genre = update_data.get("genre")
        authors = update_data.get("authors")
        publisher = update_data.get("publisher")
        publishedDate = update_data.get("publishedDate") 
        if not isbn or not title or not genre or not authors or not publisher or not publishedDate:
            raise RequiredFieldMissingError("Missing required fields.")
        if genre not in self.Genres:
            raise GenreNotValidError("Invalid genre.")
        set = {
            "ISBN": isbn,
            "title": title,
            "genre": genre,
            "authors": authors,
            "publisher": publisher,
            "publishedDate": publishedDate
        }
        updated = self.books.update_one({"_id": object_id}, {"$set": set})
        if updated.matched_count == 0:
            raise BookNotFoundError(f"Book with id: {book_id} not found in book club")
        return book_id
    
    def get_book(self, book_id):
        try:
            object_id = ObjectId(book_id)
        except Exception as e:
            raise BookNotFoundError ("Invalid ID Format")
        book = self.books.find_one({"_id": object_id})
        if not book:
            raise BookNotFoundError(f"Book with ID {book_id} not found.")
        book["id"] = str(book["_id"])
        del book["_id"]
        return book

    def delete_book(self, book_id):
        try:
            object_id = ObjectId(book_id)
        except Exception as e:
            raise BookNotFoundError ("Invalid ID Format")
        count = self.books.delete_one({"_id": object_id})
        if count.deleted_count == 0:
            raise BookNotFoundError(f"Book with ID {book_id} not found.")
        self.ratings.delete_one({"book_id": object_id})
        return True
    
    def add_rating(self, book_id, rating):
        if not book_id or not rating:
            raise RequiredFieldMissingError("Missing required fields.")
        if rating not in range(1, 6):
            raise UnvalidRating(f"The rating is not in the range of 1-5.")
        try:
            object_id = ObjectId(book_id)
        except Exception as e:
            raise BookNotFoundError ("Invalid ID Format")
        add_rating = self.ratings.find_one({"book_id": object_id})
        if not add_rating:
            raise BookNotFoundError (f"Book with id: {book_id} is not in the book club")
        values = add_rating['values']
        values.append(rating)
        new_average = round(sum(values) / len(values), 2)
        self.ratings.update_one({"book_id": object_id}, {"$set": {"values": values, "average": new_average}})
        return new_average
        
    def get_ratings(self, book_id):
        try:
            object_id = ObjectId(book_id)
        except Exception as e:
            raise BookNotFoundError ("Invalid ID Format")
        book_ratings = self.ratings.find_one({"book_id": object_id})
        if not book_ratings:
            raise BookNotFoundError(f"Book with ID {book_id} not found.")
        return {
            "title": str(book_ratings["title"]),
            "values": book_ratings["values"],
            "average": book_ratings["average"],
            "id": str(book_ratings["book_id"])
        }
    
    def update_top(self):
        ratings = list(self.ratings.find())
        ratings.sort(key=lambda x: x['average'], reverse=True)
        self.top3 = ratings[:3]
    
    def get_top(self):
        self.update_top()
        return self.top3