import logging
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from DataManager import DataManager
from User import User
from SearchStrategy import SearchStrategy, SearchByAuthor, SearchByGenre, SearchByTitle, LibrarySearch
from decorators import log_execution



class LibraryGUI:
    def __init__(self):
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'background': '#ECF0F1',
            'text': '#2C3E50',
            'button': '#2980B9',
            'button_hover': '#3498DB'
        }
        self.current_user = None


    # Helper methods for creating styled elements
    def create_styled_window(self, title, size):
        window = tk.Tk()
        window.title(title)
        window.geometry(size)
        window.configure(bg=self.colors['background'])
        default_font = tkfont.Font(family="Helvetica", size=10)
        window.option_add("*Font", default_font)
        return window

    def create_styled_button(self, parent, text, command):
        button = tk.Button(parent,
                           text=text,
                           font=('Helvetica', 10),
                           bg=self.colors['button'],
                           fg='white',
                           command=command,
                           relief='flat',
                           padx=10,
                           pady=5)
        return button

    def create_styled_entry(self, parent):
        entry = tk.Entry(parent,
                         font=('Helvetica', 10),
                         bg='white',
                         relief='solid')
        return entry

    def create_styled_label(self, parent, text):
        return tk.Label(parent,
                        text=text,
                        font=('Helvetica', 10),
                        bg=self.colors['background'],
                        fg=self.colors['text'])

    def check_authentication(self, window=None):
        """בודק אם יש משתמש מחובר למערכת"""
        if not self.current_user:
            messagebox.showerror("Error", "You must be logged in to perform this action")
            if window:
                window.destroy()
            self.entry_window()
            return False
        return True
    # Event handling
    def on_button_click(self, def_name, entries, window):
        if def_name == "submit_register":
            user_name = entries['User name'].get()
            password = entries['Password'].get()
            confirm_password = entries['Confirm Password'].get()

            try:
                if not user_name:
                    logging.warning('registered fail')
                    raise ValueError ("Please fill the user name field")
                if not password or not confirm_password:
                    logging.warning('registered fail')
                    raise ValueError("Please fill in both password fields")
                if User.user_exists(user_name):
                    logging.error('registered fail')
                    messagebox.showerror("Error", "Username already exists")
                    entries['User name'].delete(0, tk.END)
                    entries['User name'].focus()
                    return
                if password != confirm_password:
                    entries['Password'].delete(0, tk.END)
                    entries['Confirm Password'].delete(0, tk.END)
                    entries['Password'].focus()
                    logging.error('registered fail')
                    messagebox.showwarning("Password Mismatch",
                                           "Passwords do not match. Please enter your password again.")
                    return
                # יצירת משתמש חדש רק בהרשמה
                self.current_user = User(user_name, password, confirm_password)
                logging.info('registered successfully')
                messagebox.showinfo("Success", "Registration successful! Please login.")
                window.destroy()
                self.login_window()

            except ValueError as e:
                    logging.error('registered fail')
                    messagebox.showerror("Error", str(e))

        elif def_name == "the_login_window":
            user_name = entries['User name'].get()
            password = entries['Password'].get()
            user = User.authenticate_user(user_name, password)

            if user:
                self.current_user = user  # שמירת מצביע למשתמש הקיים
                logging.info('logged in successfully')
                window.destroy()
                self.menu_window()
            else:
                logging.error('logged in fail')
                messagebox.showerror("Error", "Invalid username or password")
                # ניקוי שדות בלוגין שגוי
                entries['Password'].delete(0, tk.END)
                entries['Password'].focus()

        elif not self.check_authentication(window):
            logging.error('logged in fail')
            return

        elif def_name == "the_menu_window":
            window.destroy()
            if entries == "Search Book":
                self.search_book_window()
            elif entries == "View Book":
                self.view_book_window()
            elif entries == "Lend Book":
                self.lend_book_window()
            elif entries == "Return Book":
                self.return_book_window()
            elif entries == "Add Book":
                self.add_book_window()
            elif entries == "Remove Book":
                self.remove_book_window()
            elif entries == "Logout":
                self.logout()
            elif entries == "Messages":
                self.messages_window()


        elif def_name == "add_book_action":
            try:
                self.current_user.add_book(
                    entries['Title'].get(),
                    entries['Author'].get(),
                    entries['How Many Copies'].get(),
                    entries['Genre'].get(),
                    entries['Year'].get()
                )
                messagebox.showinfo("Success", "Book added successfully")
                window.destroy()
                self.menu_window()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        elif def_name == "remove_book_action":
            try:
                result = self.current_user.remove_book(
                    entries['Title:'].get(),
                    entries['Author:'].get(),
                    entries['How Many Copies to remove:'].get(),
                    entries['Genre:'].get(),
                    entries['Year:'].get()
                )
                if result == 4:
                    messagebox.showinfo("Success", "Book removed successfully")
                    window.destroy()
                    self.menu_window()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        elif def_name == "view_action":
            try:
                if entries == "all":
                    result = self.current_user.view_all_book()
                elif entries == "available":
                    result = self.current_user.view_available()
                elif entries == "loaned":
                    result = self.current_user.view_loaned()
                elif entries == "popular":
                    result = self.current_user.view_popular()


                if result:
                    result_window = self.create_styled_window("Results", "1200x400")
                    text_widget = tk.Text(result_window, wrap=tk.WORD)
                    text_widget.pack(expand=True, fill='both', padx=20, pady=20)
                    for item in result:
                        text_widget.insert(tk.END, str(item) + '\n')
                    text_widget.configure(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", str(e))

        elif def_name == "lend_book_action":
            try:
                result = self.current_user.lone_book(entries['Title'].get())
                if result not in [1, 2]:
                    messagebox.showinfo("Success", "Book loaned successfully")
                    window.destroy()
                    self.menu_window()
                elif result == 1:
                    messagebox.showinfo("Failed", "There isn't any book named like that in the library")
                elif result == 2:
                    messagebox.showinfo("Failed", "This book is already loaned, the system is adding you to the waiting list")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        elif def_name == "return_book_action":
            try:
                result = self.current_user.return_book(entries['Title'].get())
                if result != 1 and result != 6:
                    messagebox.showinfo("Success", "Book returned successfully")
                    window.destroy()
                    self.menu_window()
                elif result == 1:
                    messagebox.showinfo("There is no this book in the library")
                elif result == 6:
                    messagebox.showinfo("Impossible to insert the book, all the books are in the library")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        elif def_name == "search_action":
            try:
                # קבלת סוג החיפוש שנבחר
                search_type = entries['search_type']
                if search_type == 'title':
                    result = self.search_books('title', entries['text'].get(),DataManager.all_books)
                elif search_type == 'genre':
                    result = self.search_books('genre', entries['text'].get(), DataManager.all_books)
                elif search_type == 'author':
                    result = self.search_books('author', entries['text'].get(), DataManager.all_books)

                if result:
                    # הצגת התוצאות בחלון חדש
                    result_window = self.create_styled_window("Search Results", "1200x400")
                    text_widget = tk.Text(result_window, wrap=tk.WORD)
                    text_widget.pack(expand=True, fill='both', padx=20, pady=20)
                    for item in result:
                        text_widget.insert(tk.END, str(item) + '\n')
                    text_widget.configure(state='disabled')
                else:
                    messagebox.showinfo("No Results", "No books matched the search criteria.")

            except Exception as e:
                messagebox.showerror("Error", str(e))
    @log_execution
    def messages_window(self):
        """Display messages for the current user."""
        if not self.check_authentication():  # Ensure the user is authenticated
            return

        # Create the messages window
        messages_window = self.create_styled_window("Messages", "800x600")

        # Add a label for the title
        self.create_styled_label(messages_window, "Your Messages").pack(pady=10)

        # Text widget to display the messages
        messages_text = tk.Text(messages_window, wrap=tk.WORD, state='normal')
        messages_text.pack(expand=True, fill='both', padx=10, pady=10)

        # Fetch and display user messages
        try:
            user_messages = self.current_user.library_messages  # Assume `get_messages` fetches messages for the user
            if user_messages:
                unique_messages = list(set(user_messages))
                for message in unique_messages:
                    messages_text.insert(tk.END, f"{message}\n\n")
            else:
                messages_text.insert(tk.END, "You have no messages.")
            messages_text.configure(state='disabled')  # Make the text widget read-only
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch messages: {str(e)}")

        # Add a close button to exit the messages window
        close_button = self.create_styled_button(messages_window, "Close", messages_window.destroy)
        close_button.pack(pady=10)
        self.menu_window()
    @log_execution
    def entry_window(self):
        window = self.create_styled_window("Welcome", "400x200")

        frame = ttk.Frame(window, padding="20")
        frame.pack(expand=True, fill='both')

        title_label = tk.Label(frame,
                               text="Welcome to Library System",
                               font=('Helvetica', 16, 'bold'),
                               fg=self.colors['primary'])
        title_label.pack(pady=(0, 20))

        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(expand=True)

        register_button = self.create_styled_button(
            buttons_frame,
            "Register",
            lambda: (window.destroy(), self.register_window())
        )
        register_button.grid(row=0, column=0, padx=10)

        login_button = self.create_styled_button(
            buttons_frame,
            "Login",
            lambda: (window.destroy(), self.login_window())
        )
        login_button.grid(row=0, column=1, padx=10)

        window.mainloop()
    @log_execution
    def register_window(self):
        window = self.create_styled_window("Register", "400x400")

        frame = ttk.Frame(window, padding="20")
        frame.pack(expand=True, fill='both')

        title_label = self.create_styled_label(frame, "Register New Account")
        title_label.configure(font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))

        fields = [
            ('User name', 1),
            ('Password', 2),
            ('Confirm Password', 3)
        ]

        entries = {}

        back_button = self.create_styled_button(
            frame,
            "Back",
            lambda: (window.destroy(), self.entry_window())
        )
        back_button.pack(anchor='w', pady=(0, 20))

        for text, row in fields:
            label = self.create_styled_label(frame, text)
            label.pack(anchor='w')

            entry = self.create_styled_entry(frame)
            if 'Password' in text:
                entry.configure(show='*')
            entry.pack(fill='x', pady=(0, 10))
            entries[text] = entry

        submit_button = self.create_styled_button(
            frame,
            "Submit",
            lambda: self.on_button_click('submit_register', entries, window)
        )
        submit_button.pack(pady=20)

        window.mainloop()
    @log_execution
    def login_window(self):
        window = self.create_styled_window("Login", "400x400")

        frame = ttk.Frame(window, padding="20")
        frame.pack(expand=True, fill='both')

        title_label = self.create_styled_label(frame, "Login to Your Account")
        title_label.configure(font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))

        back_button = self.create_styled_button(
            frame,
            "Back",
            lambda: (window.destroy(), self.entry_window())
        )
        back_button.pack(anchor='w', pady=(0, 20))

        fields = [('User name', 1), ('Password', 2)]
        entries = {}

        for text, row in fields:
            label = self.create_styled_label(frame, text)
            label.pack(anchor='w')

            entry = self.create_styled_entry(frame)
            if text == 'Password':
                entry.configure(show='*')
            entry.pack(fill='x', pady=(0, 10))
            entries[text] = entry

        login_button = self.create_styled_button(
            frame,
            "Login",
            lambda: self.on_button_click("the_login_window", entries, window)
        )
        login_button.pack(pady=20)

        window.mainloop()
    @log_execution
    def menu_window(self):
        if not self.check_authentication():
            return

        window = self.create_styled_window("Menu", "600x500")

        frame = ttk.Frame(window, padding="20")
        frame.pack(expand=True, fill='both')

        title_label = tk.Label(
            frame,
            text="Library Management System",
            font=('Helvetica', 18, 'bold'),
            fg=self.colors['primary']
        )
        title_label.pack(pady=(0, 20))

        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(expand=True)

        buttons = [
            ("Add Book", 0, 0),
            ("Remove Book", 0, 1),
            ("Search Book", 1, 0),
            ("View Book", 1, 1),
            ("Lend Book", 2, 0),
            ("Return Book", 2, 1),
            ("Messages", 3, 0)
        ]

        for text, row, col in buttons:
            button = self.create_styled_button(
                buttons_frame,
                text,
                lambda t=text: self.on_button_click("the_menu_window", t, window)
            )
            button.grid(row=row, column=col, pady=10, padx=10, sticky="nsew")

        logout_button = self.create_styled_button(
            buttons_frame,
            "Logout",
            lambda: self.on_button_click("the_menu_window", "Logout", window)
        )
        logout_button.grid(row=4, column=0, columnspan=2, pady=20, sticky="ew")

        for i in range(4):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            buttons_frame.grid_columnconfigure(i, weight=1)

        window.mainloop()
    @log_execution
    def add_book_window(self):
        if not self.check_authentication():
            return
        window = self.create_styled_window("Add Book", "400x500")

        frame = ttk.Frame(window, padding="20")
        frame.pack(expand=True, fill='both')

        title_label = self.create_styled_label(frame, "Add New Book")
        title_label.configure(font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))

        fields = [
            ('Title', 0),
            ('Author', 1),
            ('Genre', 2),
            ('Year', 3),
            ('How Many Copies', 4)
        ]

        entries = {}

        for text, row in fields:
            label = self.create_styled_label(frame, text)
            label.pack(anchor='w')

            entry = self.create_styled_entry(frame)
            entry.pack(fill='x', pady=(0, 10))
            entries[text] = entry

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=20)

        back_button = self.create_styled_button(
            button_frame,
            "Back",
            lambda: (window.destroy(), self.menu_window())
        )
        back_button.pack(side='left', padx=5)

        submit_button = self.create_styled_button(
            button_frame,
            "Add to library",
            lambda: self.on_button_click("add_book_action", entries, window)
        )
        submit_button.pack(side='right', padx=5)

        window.mainloop()
    @log_execution
    def remove_book_window(self):
        if not self.check_authentication():
            return
        window = self.create_styled_window("Remove Book", "400x500")

        frame = ttk.Frame(window, padding="20")
        frame.pack(expand=True, fill='both')

        title_label = self.create_styled_label(frame, "Remove Book")
        title_label.configure(font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))

        fields = [
            ('Title:', 0),
            ('Author:', 1),
            ('Genre:', 2),
            ('Year:', 3),
            ('How Many Copies to remove:', 4)
        ]

        entries = {}

        for text, row in fields:
            label = self.create_styled_label(frame, text)
            label.pack(anchor='w')

            entry = self.create_styled_entry(frame)
            entry.pack(fill='x', pady=(0, 10))
            entries[text] = entry

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=20)

        back_button = self.create_styled_button(
            button_frame,
            "Back",
            lambda: (window.destroy(), self.menu_window())
        )
        back_button.pack(side='left', padx=5)

        submit_button = self.create_styled_button(
            button_frame,
            "Remove Book",
            lambda: self.on_button_click("remove_book_action", entries, window)
        )
        submit_button.pack(side='right', padx=5)

        window.mainloop()
    @log_execution
    def search_book_window(self):
        if not self.check_authentication():
            return
        window = self.create_styled_window("Search Book", "400x400")

        frame = ttk.Frame(window, padding="20")
        frame.pack(expand=True, fill='both')

        title_label = self.create_styled_label(frame, "Search Books")
        title_label.configure(font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))

        search_frame = ttk.Frame(frame)
        search_frame.pack(fill='x', pady=(0, 20))

        search_label = self.create_styled_label(search_frame, "Search text:")
        search_label.pack(side='left', padx=5)

        search_entry = self.create_styled_entry(search_frame)
        search_entry.pack(side='right', expand=True, fill='x', padx=5)

        entries = {'text': search_entry, 'search_type': None}

        buttons = [
            ("Search by title", "title"),
            ("Search by author", "author"),
            ("Search by genre", "genre")
        ]

        for text, search_type in buttons:
            button = self.create_styled_button(
                frame,
                text,
                lambda t=search_type: (
                    entries.update({'search_type': t}),
                    self.on_button_click("search_action", entries, window)
                )
            )
            button.pack(fill='x', pady=5)

        back_button = self.create_styled_button(
            frame,
            "Back to Menu",
            lambda: (window.destroy(), self.menu_window())
        )
        back_button.pack(pady=20)

        window.mainloop()
    @log_execution
    def search_books(self,search_type, query, data):
        """
        פונקציית עזר לביצוע חיפושי ספרים
        search_type: סוג החיפוש ('genre', 'author', או 'title')
        query: מחרוזת החיפוש
        data: מילון הספרים
        """
        library_search = LibrarySearch()

        search_strategies = {
            'genre': SearchByGenre,
            'author': SearchByAuthor,
            'title': SearchByTitle
        }

        strategy_class = search_strategies.get(search_type.lower())
        if not strategy_class:
            raise ValueError("סוג חיפוש לא חוקי. השתמש ב-'genre', 'author', או 'title'")

        library_search.strategy = strategy_class()
        return library_search.search(data, query)
    @log_execution
    def view_book_window(self):
        if not self.check_authentication():
            return
        window = self.create_styled_window("View Books", "400x400")
        frame = ttk.Frame(window, padding="20")
        frame.pack(expand=True, fill='both')

        title_label = self.create_styled_label(frame, "View Books")
        title_label.configure(font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))

        buttons = [
            ("List of all books", "all"),
            ("List of available books", "available"),
            ("List of loaned books", "loaned"),
            ("Popular books", "popular")
        ]

        for text, view_type in buttons:
            button = self.create_styled_button(
                frame,
                text,
                lambda t=view_type: self.on_button_click("view_action", t, window)
            )
            button.pack(fill='x', pady=5)

        back_button = self.create_styled_button(
            frame,
            "Back to Menu",
            lambda: (window.destroy(), self.menu_window())
        )
        back_button.pack(pady=20)

        window.mainloop()
    @log_execution
    def lend_book_window(self):
        if not self.check_authentication():
            return
        window = self.create_styled_window("Lend Book", "400x500")
        frame = ttk.Frame(window, padding="20")
        frame.pack(expand=True, fill='both')

        title_label = self.create_styled_label(frame, "Lend Book")
        title_label.configure(font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))

        fields = [
            ('Title', 0),
        ]

        entries = {}

        for text, row in fields:
            label = self.create_styled_label(frame, text)
            label.pack(anchor='w')

            entry = self.create_styled_entry(frame)
            entry.pack(fill='x', pady=(0, 10))
            entries[text] = entry

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=20)

        back_button = self.create_styled_button(
            button_frame,
            "Back",
            lambda: (window.destroy(), self.menu_window())
        )
        back_button.pack(side='left', padx=5)

        submit_button = self.create_styled_button(
            button_frame,
            "Loan Book",
            lambda: self.on_button_click("lend_book_action", entries, window)
        )
        submit_button.pack(side='right', padx=5)

        window.mainloop()
    @log_execution
    def return_book_window(self):
        if not self.check_authentication():
            return
        window = self.create_styled_window("Return Book", "400x500")
        frame = ttk.Frame(window, padding="20")
        frame.pack(expand=True, fill='both')

        title_label = self.create_styled_label(frame, "Return Book")
        title_label.configure(font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))

        fields = [
            ('Title', 0),
        ]

        entries = {}

        for text, row in fields:
            label = self.create_styled_label(frame, text)
            label.pack(anchor='w')

            entry = self.create_styled_entry(frame)
            entry.pack(fill='x', pady=(0, 10))
            entries[text] = entry

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=20)

        back_button = self.create_styled_button(
            button_frame,
            "Back",
            lambda: (window.destroy(), self.menu_window())
        )
        back_button.pack(side='left', padx=5)

        submit_button = self.create_styled_button(
            button_frame,
            "Return Book",
            lambda: self.on_button_click("return_book_action", entries, window)
        )
        submit_button.pack(side='right', padx=5)

        window.mainloop()
    @log_execution
    def logout(self):
        """מנתק את המשתמש הנוכחי ומחזיר למסך הכניסה"""
        self.current_user = None
        messagebox.showinfo("Logout", "You have been logged out successfully")
        logging.info('log out successful')
        User.initialize_users()
        self.entry_window()


