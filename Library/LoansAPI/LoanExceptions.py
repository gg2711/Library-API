class Error(Exception):
    """Base class for other exceptions"""
    pass

class LoanNotFoundError(Error):
    """Occurs when a Loan's ID is not found in the database"""
    pass

class IdNotInFormat(Error):
    """Occurs when the Loan's ID is not in mongos format"""

class BookNotInLoans(Error):
    """Occurs when the book is not present in the collection"""
    pass

class BookAlreadyLoaned(Error):
    """Occurs when the book is already loaned by someone"""
    pass

class RequiredFieldMissingError(Error):
    """Occurs when a necessary field is absent"""
    pass

class MemberAlreadyLoaned(Error):
    """Occurs when the member already loaned a book"""
    pass

class DateNotInFormat(Error):
    """Occurs when the date is not in the right format"""
    pass
