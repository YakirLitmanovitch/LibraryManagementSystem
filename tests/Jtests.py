import unittest
from unittest.mock import patch

import pandas as pd
from DataManager import DataManager
from User import User

class TestUser(unittest.TestCase):
    @patch.object(User, 'user_exists', return_value=False)
    def setUp(self,mock_user_exists):
        self.dummy_user = User("DummyUser", "password", "password")
        DataManager.all_books = {}
        pd.DataFrame(columns=['title', 'author', 'is_loaned', 'copies', 'genre', 'year', 'Available books', 'popularity']) \
            .to_csv('books.csv', index=False)

    def tearDown(self):
        DataManager.all_books = {}
        pd.DataFrame(columns=['title', 'author', 'is_loaned', 'copies', 'genre', 'year', 'Available books', 'popularity']) \
            .to_csv('books.csv', index=False)

    def test_add_book_with_invalid_copies(self):
        result = self.dummy_user.add_book("Book4", "Author4", -1, "Drama", 2022)
        self.assertEqual(result, 5)
        self.assertNotIn("Book4", DataManager.all_books)

        df = pd.read_csv('books.csv')
        self.assertNotIn("Book4", df['title'].values)

    def test_add_book_with_existing_name_different_author(self):
        self.dummy_user.add_book("Book5", "Author5", 2, "Horror", 2020)
        self.dummy_user.add_book("Book5", "Author6", 3, "Horror", 2020)
        self.assertEqual(DataManager.all_books["Book5"][0].author, "Author5")
        self.assertEqual(DataManager.all_books["Book5"][0].copies, 5)

        df = pd.read_csv('books.csv')
        updated_row = df[df['title'] == "Book5"]
        self.assertEqual(updated_row['author'].iloc[0], "Author5")
        self.assertEqual(updated_row['copies'].iloc[0], 5)

    def test_remove_book_not_in_library(self):
        result = self.dummy_user.remove_book("NonExistentBook", "Author", 1, "Genre", 2020)
        self.assertEqual(result, 5)
        self.assertNotIn("NonExistentBook", DataManager.all_books)

        df = pd.read_csv('books.csv')
        self.assertNotIn("NonExistentBook", df['title'].values)

    def test_remove_book_with_invalid_copies(self):
        self.dummy_user.add_book("Book6", "Author6", 2, "Sci-Fi", 2021)
        result = self.dummy_user.remove_book("Book6", "Author6", -1, "Sci-Fi", 2021)
        self.assertEqual(result, 5)
        self.assertEqual(DataManager.all_books["Book6"][0].copies, 2)

        df = pd.read_csv('books.csv')
        updated_row = df[df['title'] == "Book6"]
        self.assertEqual(updated_row['copies'].iloc[0], 2)

    def test_lone_book_not_in_library(self):
        result = self.dummy_user.lone_book("NonExistentBook")
        self.assertEqual(result, 1)

    def test_return_book_not_in_library(self):
        result = self.dummy_user.return_book("NonExistentBook")
        self.assertEqual(result, 1)

    def test_view_all_books_empty_library(self):
        result = self.dummy_user.view_all_book()
        self.assertIsNone(result)

    def test_view_available_books_empty_library(self):
        result = self.dummy_user.view_available()
        self.assertEqual(result, 9)

    def test_view_loaned_books_empty_library(self):
        result = self.dummy_user.view_loaned()
        self.assertEqual(result, 10)

    def test_view_popular_books_empty_library(self):
        result = self.dummy_user.view_popular()
        self.assertEqual(result, [])

    def test_add_book_with_valid_data(self):
        result = self.dummy_user.add_book("Book7", "Author7", 3, "Fantasy", 2023)
        self.assertEqual(result, 0)
        self.assertIn("Book7", DataManager.all_books)
        self.assertEqual(DataManager.all_books["Book7"][0].author, "Author7")
        self.assertEqual(DataManager.all_books["Book7"][0].copies, 3)

        df = pd.read_csv('books.csv')
        self.assertIn("Book7", df['title'].values)
        added_row = df[df['title'] == "Book7"]
        self.assertEqual(added_row['author'].iloc[0], "Author7")
        self.assertEqual(added_row['copies'].iloc[0], 3)

    def test_remove_book_with_valid_data(self):
        self.dummy_user.add_book("Book8", "Author8", 4, "Mystery", 2022)
        result = self.dummy_user.remove_book("Book8", "Author8", 2, "Mystery", 2022)
        self.assertEqual(result, 4)
        self.assertEqual(DataManager.all_books["Book8"][0].copies, 2)

        df = pd.read_csv('books.csv')
        updated_row = df[df['title'] == "Book8"]
        self.assertEqual(updated_row['copies'].iloc[0], 2)

    def test_lone_book_with_valid_data(self):
        self.dummy_user.add_book("Book9", "Author9", 1, "Thriller", 2021)
        result = self.dummy_user.lone_book("Book9")
        self.assertEqual(result, 0)
        self.assertTrue(DataManager.all_books["Book9"][0].is_loaned)

        df = pd.read_csv('books.csv')
        updated_row = df[df['title'] == "Book9"]
        self.assertTrue(updated_row['is_loaned'].iloc[0])

    def test_return_book_with_valid_data(self):
        self.dummy_user.add_book("Book10", "Author10", 1, "Romance", 2020)
        self.dummy_user.lone_book("Book10")
        result = self.dummy_user.return_book("Book10")
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()