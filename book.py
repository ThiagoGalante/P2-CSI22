from dataclasses import dataclass

class Book():
    """Represents a book in the repository."""
    isbn: int
    title: str
    author: str
    genre: str
    publisher: str
    published_year: int

    def __init__(self, title: str, author: str, genre: str, isbn: int, publisher: str, published_year: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.publisher = publisher
        self.published_year = published_year

class BookBuilder():
    """Builder class for creating Book objects."""
    def __init__(self):
        self._title = None
        self._author = None
        self._genre = None
        self._isbn = None
        self._publisher = None
        self._published_year = None

    def with_title(self, title: str):
        self._title = title
        return self

    def with_author(self, author: str):
        self._author = author
        return self

    def with_genre(self, genre: str):
        self._genre = genre
        return self

    def with_isbn(self, isbn: str):
        self._isbn = isbn
        return self

    def with_publisher(self, publisher: str):
        self._publisher = publisher
        return self

    def with_published_year(self, published_year: str):
        self._published_year = published_year
        return self

    def build(self) -> Book:
        """
        Validates all fields, collects all errors, and returns a Book object if all data is valid.
        """
        errors = []

        try:
            if not (self._isbn and len(self._isbn) == 13 and self._isbn.isdigit()):
                raise ValueError()
            self._isbn = int(self._isbn)
        except (ValueError, TypeError):
            errors.append("- ISBN must be a valid 13 digits number.")

        if not self._title:
            errors.append("- Title cannot be empty.")
        if not self._author:
            errors.append("- Author cannot be empty.")
        if not self._genre:
            errors.append("- Genre cannot be empty.")
        if not self._publisher:
            errors.append("- Publisher cannot be empty.")
    
        try:
            if not (self._published_year and self._published_year.isdigit()):
                raise ValueError()
            self._published_year = int(self._published_year)
        except (ValueError, TypeError):
            errors.append("- Published year must be a valid number.")

        if errors:
            error_message = "Please correct the following issues:\n" + "\n".join(errors)
            raise ValueError(error_message)

        return Book(
            title=self._title,
            author=self._author,
            genre=self._genre,
            isbn=self._isbn,
            publisher=self._publisher,
            published_year=self._published_year
        )