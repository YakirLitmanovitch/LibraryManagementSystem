import pandas as pd
from Book import Book

class DataManager:
    all_books = {}
    waiting_list = {}

    @classmethod
    def initialize_books(cls):
        """
        Initialize the library state from the CSV file.
        This method reads the 'books.csv' file and populates the `all_books` dictionary.
        It also ensures that the CSV file has the necessary columns ('Available books' and 'popularity').
        If these columns are missing, they are added and the file is updated.
        """
        cls.all_books.clear()

        try:
            df = pd.read_csv('books.csv')

            update_required = False

            if 'Available books' not in df.columns:
                df['Available books'] = 0
                update_required = True

            if 'popularity' not in df.columns:
                df['popularity'] = 0
                update_required = True

            if update_required:
                # Update the new columns based on the initial conditions
                df['popularity'] = df.apply(
                    lambda row: int(row['copies']) if row['is_loaned'] == 'Yes' else row['popularity'], axis=1)
                df['Available books'] = df.apply(
                    lambda row: int(row['copies']) if row['is_loaned'] == 'No' else row['Available books'], axis=1)
                df.to_csv('books.csv', index=False)

            rows_as_arrays = df.astype(str).values.tolist()

            for element in rows_as_arrays:
                book = Book(element[0], element[1], element[2], element[3], element[4], element[5])
                available_books = int(element[6])
                popularity = int(element[7])
                cls.all_books[element[0]] = (book, available_books, popularity)

        except FileNotFoundError:
            df = pd.DataFrame(columns=['title', 'author', 'is_loaned', 'copies', 'genre', 'year', 'Available books','popularity'])
            df.to_csv('books.csv', index=False)
    @classmethod
    def get_available_books(cls, book_name):
        return cls.all_books.get(book_name, (None, 0))[1]
    @classmethod
    def get_book_as_object(cls, book_name):
        return cls.all_books.get(book_name, (None, 0))[0]
    @classmethod
    def get_book_popularity(cls, book_name):
        return cls.all_books.get(book_name, (None, 0, 0))[2]



