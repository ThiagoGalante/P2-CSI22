from sqlalchemy import Column, Integer, String

class Book():
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    isbn = Column("isbn", String, unique=True, nullable=False)
    title = Column("name", String, nullable=False)
    author = Column("author", String, nullable=False)
    genre = Column("genre", String, nullable=False)
    publisher = Column("publisher", String, nullable=False)
    publish_year = Column("publish_year", Integer, nullable=False)

    def __init__(self, title: str, author: str, genre: str, isbn: str, publisher: str, publish_year: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.publisher = publisher
        self.publish_year = publish_year