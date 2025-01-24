import logging


class SearchStrategy:
    """אסטרטגיית חיפוש בסיסית"""
    def search(self, data, query):
        """
        מתודת חיפוש בסיסית
        data: מילון של ספרים
        query: מחרוזת חיפוש
        """
        pass

class SearchByGenre(SearchStrategy):
    def search(self, data, query):
        genre_list = []
        query = query.lower()

        for book_data in data.values():
            book = book_data[0]
            if query in book.genre.lower():
                genre_list.append(book)
        if not genre_list:
            logging.warning(f'Search book {query} by genre completed fail')
        else:
            logging.info(f'Search book {query} by genre completed successfully')
        return genre_list


class SearchByAuthor(SearchStrategy):
    def search(self, data, query):
        author_list = []
        query = query.lower()

        for book_data in data.values():
            book = book_data[0]
            if query in book.author.lower():
                author_list.append(book)
        if not author_list:
            logging.warning(f'Search book {query} by author  completed fail')
        else:
            logging.info(f'Search book {query} by author completed successfully')
        return author_list


class SearchByTitle(SearchStrategy):
    def search(self, data, query):
        title_list = []
        query = query.lower()

        for title, book_data in data.items():
            if query in title.lower():
                title_list.append(book_data[0])
        if not title_list:
            logging.warning(f'Search book {query} by name completed fail')
        else:
            logging.info(f'Search book {query} by name completed successfully')
        return title_list
class LibrarySearch:
    """מחלקה שמנהלת את החיפושים בספרייה"""
    def __init__(self):
        self._strategy = None

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: SearchStrategy):
        self._strategy = strategy

    def search(self, data, query):
        if self._strategy is None:
            raise ValueError("לא נבחרה אסטרטגיית חיפוש")
        return self._strategy.search(data, query)