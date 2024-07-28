class Error(Exception):
    """Base class for other exceptions"""
    pass

class ExternalAPIServiceError(Error):
    """Occurs due to an issue with an external API"""
    pass

class APIBookNotFoundError(Error):
    """Occurs when a book's ISBN is not found in the Google Books API"""
    pass

class BookNotFoundError(Error):
    """Occurs when a book's ISBN is not found in the database"""
    pass

class DuplicateBookError(Error):
    """Occurs when the book is already present in the collection"""
    pass

class GenreNotValidError(Error):
    """Occurs when the provided genre is not valid"""
    pass

class RequiredFieldMissingError(Error):
    """Occurs when a necessary field is absent"""
    pass

class UnvalidRating(Error):
    """Occurs when the rating is not in the range of 1-5"""
    pass
