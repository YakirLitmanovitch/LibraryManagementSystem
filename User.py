import hashlib
from decorators import log_execution
from Book import Book
import pandas as pd
import logging
from BookIterator import BookIterator
from DataManager import DataManager

logging.basicConfig(
    filename='logFile.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class User:
    users = []
    flag = True
    @classmethod
    def get_user(cls, username, password):
        """
                Returns a string representation of the book object.
        """
        for user in cls.users:
            if user.name == username and str(user.password) == password:
                return user
        return None
    @classmethod
    def user_exists(cls, username):
        """
        Returns a string representation of the book object.
        """
        return any(user.name == username for user in cls.users)
    @classmethod
    def authenticate_user(cls, username, password):
        """
        Returns a string representation of the book object.
        """
        hashed_password = cls.hash_password(password)
        for user in cls.users:
            if user.name == username and user.password == hashed_password:

                return user
        return None
    @log_execution
    def __init__(self, name, password, confirm_password):
        """
        Initializes a new user with a name and a password.
        Raises a ValueError if the password and the confirmation password do not match,
         or if the username already exists.
        """
        if not password == confirm_password:
            logging.error('registered fail')
            raise ValueError("Unmatched passwords")
        if self.user_exists(name):
            logging.error('registered fail')
            raise ValueError("Username already exists")

        self.library_messages = [""]
        self.name = name
        if len(password) == 64 and all(c in '0123456789abcdef' for c in password):
            self.password = password
        else:
            self.password = User.hash_password(password)
        if User.flag:
            self.add_to_users()
            self.save_users()
    @log_execution
    def add_to_users (self):
        self.users.append(self)
    @log_execution
    def notifications (self,update_list, mess):
        """
        Sends notifications to users in the update list.

        Parameters:
        update_list (list): The list of users to notify.
        mess (str): The message to send.
        """
        df = pd.read_csv('users.csv')

        for user in update_list:
            username = user.name
            self.library_messages.append(mess)
            current_messages = df.loc[df['username'] == username, 'messages'].values
            if current_messages.size > 0:  # אם המשתמש נמצא בקובץ
                current_messages = current_messages[0]
                updated_messages = f"{current_messages}; {mess}" if pd.notna(current_messages) else mess
                df.loc[df['username'] == username, 'messages'] = updated_messages
        logging.info('notifications successfully')
        df.to_csv('users.csv', index=False)
    @log_execution
    def add_book(self,name, author, _copies, genre, year):
        """
        Adds a new book to the library.
        If the book already exists, the number of copies is increased.
        If the book is loaned, it is marked as available.

        """
        df = pd.read_csv('books.csv')
        if int(_copies) <= 0:
            #print("Impossible to add 0 or fewer copies")
            logging.error("book added fail")

            return 5
        if name in DataManager.all_books:
            book_ptr = DataManager.get_book_as_object(name)
            available_book_ptr = DataManager.all_books[name][1] + int(_copies)
            popularity =  DataManager.all_books[name][2]
            book_ptr.copies += int(_copies)
            DataManager.all_books[name] = book_ptr, available_book_ptr, popularity
            if book_ptr.is_loaned == "Yes":
                book_ptr.is_loaned = "No"
            df.loc[df['title'] == name, ['is_loaned', 'copies', 'Available books']] = \
                [book_ptr.is_loaned, book_ptr.copies, available_book_ptr]
            df.to_csv('books.csv', index=False)
            logging.info("book added successfully")
            return 0
        else:
            DataManager.all_books[name] = []
            book = Book(name, author, "No", _copies, genre, year)
            DataManager.all_books[name] = book, _copies,0
            new_row = {'title': name, 'author': author, 'is_loaned': "No",
                       'copies': _copies, 'genre': genre, 'year': year, 'Available books': _copies, 'popularity': 0}
            new_row_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_row_df], ignore_index=True)
            df.to_csv('books.csv', index=False)
            logging.info("book added successfully")
            self.notifications(self.users,
                               f"There is a new book in the library,"
                               f" his name is: {name}.")
            return 0
    @log_execution
    def remove_book(self,name, author, _copies, genre, year):
        """
        Removes a book from the library.
        If the book is loaned, it cannot be removed.
        If the number of copies to remove is greater than the number of available copies,
         the book is not removed.
        If the number of copies to remove is equal to the number of copies in the library,
            the book is removed from the library.
        If the number of copies to remove is equal to the number of available copies,
            the book is marked as loaned.
        Otherwise, the number of available copies is updated.

        """
        if int(_copies) <= 0:
            #print("Impossible to remove 0 or fewer copies")
            logging.error("book removed fail")
            return 5
        df = pd.read_csv('books.csv')
        if name not in DataManager.all_books:
            #print("this book is not exist")
            logging.warning("book removed fail")
            return 5

        else:
            book_ptr = DataManager.get_book_as_object(name)
            available_book_ptr = DataManager.get_available_books(name)# עדכון הספרים הזמינים מתוך המילון

            if book_ptr.is_loaned == "Yes":
                print("You tried to remove loan books")
                logging.error("book removed fail")
                return 1
            if int(_copies) > int(book_ptr.copies):
                print(f"To many copies to remove, there is : {book_ptr.copies} in the all library,"
                      f" And the available to remove are: {available_book_ptr}")
                logging.error("book removed fail")
                return 2
            if int(_copies) > int(available_book_ptr):
                print(f"To many copies to remove, there are {available_book_ptr} available to remove: ")
                logging.info("book removed fail")
                return 3
            else:
                if int(_copies) == int(available_book_ptr) == int(book_ptr.copies):
                    del DataManager.all_books[name]
                    df = df[df['title'] != name]
                    df.to_csv('books.csv', index=False)
                    self.notifications(self.users,
                                       f"The book: {name} by {author} is not exist anymore")
                    logging.info("book removed successfully")
                    return 4
                elif int(_copies) == int(available_book_ptr):
                    available_book_ptr = 0
                    book_ptr.copies = int(book_ptr.copies) - int(_copies)

                    book_ptr.is_loaned = "Yes"
                    df.loc[df['title'] == name, ['is_loaned', 'copies', 'Available books']] = \
                        [book_ptr.is_loaned, book_ptr.copies, available_book_ptr]
                    df.to_csv('books.csv', index=False)
                    logging.info("book removed successfully")

                    DataManager.initialize_books()
                    return 4
                else:
                    available_book_ptr = int(available_book_ptr) - int(_copies)
                    book_ptr.copies = int(book_ptr.copies) - int(_copies)
                    df.loc[df['title'] == name, ['copies', 'Available books']] = \
                        [book_ptr.copies, available_book_ptr]
                    df.to_csv('books.csv', index=False)
                    logging.info("book removed successfully")

                    DataManager.initialize_books()
                    return 4
    @log_execution
    def update_waiting_list_csv(self, name):
        """
        Updates the waiting list CSV file with the new users waiting for a book.

        """
        try:
            waiting_df = pd.read_csv('waitingList.csv')
        except FileNotFoundError:
            waiting_df = pd.DataFrame(columns=['name', 'username'])

        if name in DataManager.waiting_list:
            usernames = ';'.join([user.name for user in DataManager.waiting_list[name]])

            if name in waiting_df['name'].values:
                waiting_df.loc[waiting_df['name'] == name, 'username'] = usernames
            else:
                new_row = pd.DataFrame({
                    'name': [name],
                    'username': [usernames]
                })
                waiting_df = pd.concat([waiting_df, new_row], ignore_index=True)

            waiting_df.to_csv('waitingList.csv', index=False)
            logging.info(f'Updated waiting list for book: {name}')
    @log_execution
    def lone_book(self,name):
        """
        Borrows a book from the library.
        If the book is already loaned, the user is added to the waiting list.
        If the book is available, the number of available copies is updated.

        """

        if name not in DataManager.all_books:
            #print("There is no this book in the library")
            logging.warning('book borrowed fail')
            return 1
        book_ptr = DataManager.get_book_as_object(str(name))

        if book_ptr.is_loaned == "Yes":
            df = pd.read_csv('books.csv')
            #print("This book is already loaned")
            logging.error('book borrowed fail')
            try:
                waiting_df = pd.read_csv('waiting_list.csv')
            except FileNotFoundError:
                waiting_df = pd.DataFrame(columns=['book_name', 'user_ids'])

            if name in DataManager.waiting_list:
                DataManager.waiting_list[name].append(self)

            else:
                DataManager.waiting_list[name]=[self]

            self.update_waiting_list_csv(name)

            book_info = DataManager.all_books[name]
            book_ptr, available_books, popularity = book_info
            popularity += 1
            DataManager.all_books[name] = (book_ptr, available_books, popularity)
            df.loc[df['title'] == name, ['popularity']] = [popularity]
            df.to_csv('books.csv', index=False)
            return 2
        else:
            df = pd.read_csv('books.csv')
            book_ptr, available_books, popularity = DataManager.all_books[name]
            available_book_ptr = int(available_books) - 1
            popularity += 1

            DataManager.all_books[name] = (book_ptr, available_book_ptr, popularity)
            if available_book_ptr == 0:
                book_ptr.is_loaned = "Yes"
            logging.info('book borrowed successfully')

            df.loc[df['title'] == name, ['is_loaned', 'Available books', 'popularity']] = \
                [book_ptr.is_loaned, available_book_ptr, popularity]
            df.to_csv('books.csv', index=False)
            return 0
    @log_execution
    def return_book(self,name):
        """
        Returns a book to the library.
        If the book is not exist in the library, the return will be impossible.
        Otherwise, the number of available copies is updated.

        """
        if name not in DataManager.all_books:
            #print("There is no this book in the library")
            logging.warning('book returned fail')
            return 1
        else:
            book_ptr = DataManager.get_book_as_object(name)
            available_book_ptr = DataManager.get_available_books(name)
            #print(DataManager.get_available_books(name))
            if int(book_ptr.copies) == available_book_ptr:
                #print("Impossible to insert the book, all the books are in the library")
                logging.warning('book returned fail')
                return 6
            else:
                df = pd.read_csv('books.csv')
                available_book_ptr = DataManager.all_books[name][1] + 1
                popularity = DataManager.all_books[name][2] - 1
                if available_book_ptr - 1 == 0:
                    if name in DataManager.waiting_list:
                        self.notifications(DataManager.waiting_list[name],
                                           f"The book: {name} is back available")
                DataManager.all_books[name] = book_ptr, available_book_ptr, popularity
                print(DataManager.get_available_books(name)) #
                if book_ptr.is_loaned == "Yes":
                    book_ptr.is_loaned = "No"
                logging.info('book returned successfully')
                df.loc[df['title'] == name, ['is_loaned', 'Available books']] = \
                    [book_ptr.is_loaned, available_book_ptr]
                df.to_csv('books.csv', index=False)
                return 0
    @log_execution
    def view_all_book(self):
        """
        Displays all the books in the library.
        """
        if not DataManager.all_books:
            #print("There isn't any books in the library")
            logging.warning("Displayed all books fail")

        else:
            #print(DataManager.all_books)
            logging.info("Displayed all books successfully")
            return DataManager.all_books
    @log_execution
    def view_available(self):
        """
        Displays all the available books in the library.
        Using a filter function and iterator to display only books with available copies.

        """
        available_books = []
        for book_id, book_info in BookIterator(lambda book_id, book_info: int(book_info[1]) > 0):
            available_books.append(f"The book is: {book_info[0]} and there are {book_info[1]} available books")

        if not available_books:
            #print("There aren't any available books")
            logging.warning("Displayed all available books fail")
            return 9
        print(available_books)
        logging.info("Displayed all available books successfully")
        return available_books
    @log_execution
    def view_loaned(self):
        """
        Displays all the loaned books in the library.
        Using a filter function and iterator to display only books with loaned copies.

        """
        loaned_books = []

        for book_id, book_info in BookIterator(
                lambda book_id, book_info: DataManager.get_book_as_object(book_id).is_loaned == "Yes"):
            book_obj = DataManager.get_book_as_object(book_id)
            loaned_books.append(
                f"The book is: {book_info[0]} and there are {int(book_obj.copies) - book_info[1]} loaned books")

        if not loaned_books:
            #print("There aren't any loaned books")
            logging.warning("Displayed all borrowed books fail")
            return 10
        #print(loaned_books)
        logging.info("Displayed all borrowed books successfully")
        return loaned_books
    @log_execution
    def view_popular(self):
        """
        Displays the top 10 popular books in the library.
        Using a filter function and iterator to display only books with popularity greater than 0.

        """
        popular_books = [
            (book_info[0], book_info[2])  # שמירת שם הספר והפופולריות
            for _, book_info in BookIterator(lambda book_id, book_info: book_info[2] > 0)
        ]

        if not popular_books:
            #print("There are no popular books available.")
            logging.warning("displayed fail")
            return []

        top_popular_books = sorted(popular_books, key=lambda x: x[1], reverse=True)[:10]

        print("Top popular books:")
        for book, popularity in top_popular_books:
            print(f"The book is: {book} and the popularity is {popularity}")
        logging.info("displayed successfully")
        return top_popular_books
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(str(password).encode()).hexdigest()
    @classmethod
    def initialize_users(cls):
        """Initialize users from a CSV file.
        This method reads the 'users.csv' file and populates the `users` list.
        If the file does not exist, an empty DataFrame is created and saved as 'users.csv'.
        """
        cls.users.clear()

        try:
            df = pd.read_csv('users.csv')
            for _, row in df.iterrows():
                User.flag = False
                user = User(row['username'], row['password'],row['password'])
                messages = row['messages'] if isinstance(row['messages'], str) else ""
                user.library_messages =messages.split(';') if row['messages'] else [""]
                cls.users.append(user)
            User.flag = True
        except FileNotFoundError:
            df = pd.DataFrame(columns=['username', 'password', 'messages'])
            df.to_csv('users.csv', index=False)
    @classmethod
    def initialize_waitingList(cls):
        """
        Initialize the waiting list from a CSV file.
        This method reads the 'waitingList.csv' file and populates the `waiting_list` dictionary.
        If the file does not exist, an empty DataFrame is created and saved as 'waitingList.csv'.
        """
        DataManager.waiting_list.clear()
        try:
            df= pd.read_csv('waitingList.csv')
            for _, row in df.iterrows():
                book_name = row['name']
                DataManager.waiting_list[book_name]=[]
                if isinstance(row['username'], str) and row['username']:
                    usernames = row['username'].split(';')
                    for username in usernames:
                        for user in cls.users:
                            if user.name== username:
                                DataManager.waiting_list[book_name].append(user)
                                break
        except FileNotFoundError:
            df = pd.DataFrame(columns=['name', 'username'])
            df.to_csv('waitingList.csv', index=False)
    @classmethod
    def save_users(cls):
        """
        Save the users to a CSV file.
        This method writes the `users` list to the 'users.csv' file.

        """
        data = []
        for user in cls.users:
            data.append({
                'username': user.name,
                'password': user.password,
                'messages': ';'.join(user.library_messages)
            })

        df = pd.DataFrame(data)
        df.to_csv('users.csv', index=False)

