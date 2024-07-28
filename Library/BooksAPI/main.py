# main.py
from flask import Flask, request, jsonify
from flask_restful import Api
from BookClub import BookClub
from BookExceptions import *
import os

app = Flask(__name__)
api =Api(app)
book_club = BookClub()

@app.route('/books', methods=['POST'])
def create_book():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported media type"}), 415
    response = request.get_json()
    isbn_num = response.get('ISBN')
    title = response.get('title')
    genre = response.get('genre')

    try:
        book_id = book_club.add_book(isbn_num, title, genre)
        return jsonify({"id": str(book_id)}), 201
    except DuplicateBookError as e:
        return jsonify({"error": str(e)}), 422
    except GenreNotValidError as e:
        return jsonify({"error": str(e)}), 422
    except RequiredFieldMissingError as e:
        return jsonify({"error": str(e)}), 422
    except ExternalAPIServiceError as e:
        return jsonify({"error": str(e)}), 500
    except APIBookNotFoundError as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported media type"}), 415
    update_data = request.get_json()
    try:
        book_id = book_club.update_book(book_id, update_data)
        return jsonify({"id": str(book_id)}), 200
    except BookNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except GenreNotValidError as e:
        return jsonify({"error": str(e)}), 422
    except RequiredFieldMissingError as e:
        return jsonify({"error": str(e)}), 422
        
    
@app.route('/books', methods=['GET'])
def get_all_books():
    query_params = request.args  # Get the query string parameters
    books = book_club.books.find()
    all_books = []
    for book in books:
        book["id"] = str(book["_id"])
        del book["_id"]
        all_books.append(book)
    if query_params:
        for field, value in query_params.items():
            all_books = [book for book in all_books if book.get(field) == value]
    return jsonify(all_books), 200

@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = book_club.get_book(book_id)
        return jsonify(book), 200
    except BookNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        book_club.delete_book(book_id)
        return jsonify({"id": str(book_id)}), 200
    except BookNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/ratings', methods=['GET'])
def get_ratings():
    allRatings = list(book_club.ratings.find())
    ratings = [{
        'id': str(rating['book_id']),
        'title': rating['title'],
        'values': rating['values'],
        'average': rating['average']
    } for rating in ratings]
    return jsonify(allRatings)

@app.route('/ratings/<book_id>', methods=['GET'])
def get_rating(book_id):
    try:
        rating = book_club.get_ratings(book_id)
        return rating, 200
    except BookNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/ratings/<book_id>/values', methods=['POST'])
def add_book_rating(book_id):
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported media type"}), 415
    
    response = request.get_json()
    value = response.get('value')
    if not value:
        if value == 0:
            return jsonify({"error": "The rating is not in the range of 1-5."}), 422
        return jsonify({"error": "Missing required fields."}), 422
    else:
        try:
            value = int(value)
            average = book_club.add_rating(book_id, value)
            return jsonify({"new average": average}), 201
        except UnvalidRating as e:
            return jsonify({"error": str(e)}), 422
        except BookNotFoundError as e:
            return jsonify({"error": str(e)}), 404

    

@app.route('/top', methods=['GET'])
def get_top_ratings():
    top3 = book_club.get_top()
    ratings = [{'id': str(rating['book_id']),
                'title': rating['title'],
                'average': rating['average']
    } for rating in top3]
    return jsonify(ratings), 200

port = int(os.getenv('PORT', 5001))
if __name__ == '__main__':
    print("running rest-bookClub-svr-v1.py")
    app.run(host = '0.0.0.0', port=port, debug=True)