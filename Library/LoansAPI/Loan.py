# Loan.py
from flask import jsonify
from LoanExceptions import *
  


class Loan:
    def __init__(self, memberName, ISBN, loanDate, title, bookID):
        self.memberName = memberName
        self.ISBN = ISBN
        self.title = title
        self.bookID = bookID
        self.loanDate = loanDate
        self.loanID = None
        
    def json(self):
        return {
            'memberName': self.memberName,
            'ISBN': self.ISBN,
            'title': self.title,
            'bookID': self.bookID,
            'loanDate': self.loanDate,
            'loanID': self.loanID
        }
    