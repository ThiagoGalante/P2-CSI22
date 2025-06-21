class CatalogError(Exception):
    """Base class for all custom exceptions in the project."""
    pass

class ValidationError(CatalogError):
    """Raised when a book's data fails validation."""
    def __init__(self, errors):
        self.errors = errors
        super().__init__("Validation errors found:\n" + "\n".join(errors))

class BookNotFoundError(CatalogError):
    """Raised when a book with a specific ISBN is not found."""
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"The book with ISBN '{isbn}' was not found.")

class BookAlreadyExistsError(CatalogError):
    """Raised when trying to add a book with an ISBN that already exists."""
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"The book with ISBN '{isbn}' already exists in the catalog.")
