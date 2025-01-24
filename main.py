from DataManager import DataManager
from User import User
from libraryGui import LibraryGUI

if __name__ == "__main__":
    DataManager.initialize_books()
    User.initialize_users()
    User.initialize_waitingList()
    app = LibraryGUI()
    app.entry_window()