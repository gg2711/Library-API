# main.py
from flask import Flask, request, jsonify
from flask_restful import Api
from Loans import *
from LoanExceptions import *
from pymongo import MongoClient
import os

app = Flask(__name__)
api =Api(app)
loans = Loans()

mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')  # Use 'mongodb' as the hostname
client = MongoClient(mongo_uri)
db = client['library_db']
loansCollection = db['loans']

@app.route('/loans', methods=['POST'])
def create_loan():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported media type"}), 415
    response = request.get_json()
    memberName = response.get('memberName')
    isbn_num = response.get('ISBN')
    loanDate = response.get('loanDate')
    
    try:
        loan_id = loans.add_loan(memberName, isbn_num, loanDate)
        return jsonify({"loanID": str(loan_id)}), 201
    except BookNotInLoans as e:
        return jsonify({"error": str(e)}), 422
    except BookAlreadyLoaned as e:
        return jsonify({"error": str(e)}), 422
    except RequiredFieldMissingError as e:
        return jsonify({"error": str(e)}), 422
    except MemberAlreadyLoaned as e:
        return jsonify({"error": str(e)}), 422
    except DateNotInFormat as e:
        return jsonify({"error": str(e)}), 422
        
@app.route('/loans', methods=['GET'])
def get_allLoans():
    query_params = request.args  # Get the query string parameters
    filterloans = loans.loansCollection.find()
    all_loans = []
    for loan in filterloans:
        loan['loanID'] = str(loan['_id'])
        del loan['_id']
        all_loans.append(loan)
    if query_params:
        for field, value in query_params.items():
            all_loans = [loan for loan in all_loans if loan.get(field) == value]
    return jsonify(all_loans), 200

@app.route('/loans/<loan_id>', methods=['GET'])
def get_loan(loan_id):
    try:
        loan = loans.get_loan(loan_id)
        return jsonify(loan), 200
    except IdNotInFormat as e:
        return jsonify({"error": str(e)}), 400
    except LoanNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/loans/<loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    try:
        loans.delete_loan(loan_id)
        return jsonify({"loanID": str(loan_id)}), 200
    except LoanNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except IdNotInFormat as e:
        return jsonify({"error": str(e)}), 400

port = int(os.getenv('PORT', 5002))
if __name__ == '__main__':
    print("running rest-bookClub-svr-v1.py")
    app.run(host = '0.0.0.0', port=port, debug=True)