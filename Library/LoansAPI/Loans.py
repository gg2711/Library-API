# BookClub.py
from bson import ObjectId
from Loan import Loan
from LoanExceptions import *
import requests
from pymongo import MongoClient
import os
import re

class Loans:
    
    def __init__(self):
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
        self.client = MongoClient(mongo_uri)
        self.db = self.client['library_db']
        self.loansCollection = self.db['loans']
        self.loans = {}
       
        
    def add_loan(self, memberName, ISBN, loanDate):
        if not ISBN or not memberName or not loanDate:
            raise RequiredFieldMissingError("Missing required fields.")
        
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if not date_pattern.match(loanDate):
            raise DateNotInFormat("Date not in format.")
        
        book_response = requests.get(f'http://books:5001/books')
        
        if book_response.status_code != 200:
            raise BookNotInLoans("Failed to retrieve books from the book club.") 
        books = book_response.json()
        book = next((b for b in books if b['ISBN'] == ISBN), None)

        if book is None:
            raise BookNotInLoans("This book is not in the book club.")
          
        if self.loansCollection.find_one({"ISBN": ISBN}) is not None:
            raise BookAlreadyLoaned("This book is already loaned.")
        
        if self.loansCollection.count_documents({"memberName": memberName}) >= 2:
            raise MemberAlreadyLoaned("This member already loaned 2 or more books.")
        else:
            title = book['title']
            book_id = book['id']
            new_loan = Loan(memberName, ISBN, loanDate, title, book_id)
            mongo_id = self.loansCollection.insert_one(new_loan.json())
            loan_id = str(mongo_id.inserted_id)
            new_loan.loanID = loan_id
            self.loans[loan_id] = new_loan
            return loan_id
    
    def get_loan(self, loan_id):
        try:
            loan_object_id = ObjectId(loan_id)
        except Exception as e:
            raise IdNotInFormat("Invalid loan ID Format")
        if loan_id in self.loans:
            return self.loans[loan_id].json()
        loan = self.loansCollection.find_one({"_id": loan_object_id})
        if loan: 
            if isinstance(loan, dict):
                loan['loanID'] = str(loan['_id'])
                del loan['_id']
                return loan
        else:
            raise LoanNotFoundError(f"Loan with ID {loan_id} not found.")

    def delete_loan(self, loan_id):
        try:
            loan_object_id = ObjectId(loan_id)
        except Exception as e:
            raise IdNotInFormat("Invalid loan ID Format")
        if loan_id in self.loans:
            self.loansCollection.delete_one({"_id":ObjectId(loan_object_id)})
            del self.loans[loan_id]
            return True
        else:
            delete = self.loansCollection.delete_one({"_id":ObjectId(loan_object_id)})
            if delete.deleted_count == 1:
                return True
            else:
                raise LoanNotFoundError(f"Loan with ID {loan_id} not found.")
