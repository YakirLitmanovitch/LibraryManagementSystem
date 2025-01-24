class Book:
    """
        A class to represent a book in the library.
    """
    def __init__(self,name,  author, is_loaned, copies, genre, year):
        self.name=name
        self.is_loaned=is_loaned
        self.copies=int(copies)
        self.author=author
        self.year=year
        self.genre=genre
    def __repr__(self):
        """
         Returns a string representation of the book object.
        """
        return f"Name: {self.name} | Author: {self.author} | Is loaned: {self.is_loaned} | Copies: {self.copies} | Genre: {self.genre} | Year: {self.year}"
