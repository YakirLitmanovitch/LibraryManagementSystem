from DataManager import DataManager


class BookIterator:
    def __init__(self, filter_func=None):
        self.books = list(DataManager.all_books.items())  # הפיכת המילון לרשימה
        self.index = 0
        self.filter_func = filter_func  # פונקציית סינון (אם קיימת)

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.books):
            book_id, book_info = self.books[self.index]
            self.index += 1
            # אם יש פונקציית סינון, נבדוק אם הספר עובר את הקריטריונים
            if self.filter_func is None or self.filter_func(book_id, book_info):
                return book_id, book_info
        raise StopIteration  # כשנגמרים הספרים
