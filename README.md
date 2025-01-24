## Overview

The **Library Management System** is a robust application developed using Python. 
It provides functionalities for managing book borrowing, returning, and tracking availability. 
The system includes a user-friendly Graphical User Interface (GUI),
  and employs various design patterns to ensure maintainability and scalability.

## Features

- **Book Management**:
  - 📖 Borrowing and returning books
  - 📚 Tracking book availability
  - 🔍 Viewing all books, available books, loaned books, and popular books

- **Data Handling**:
  - 🗃️ Efficient data manipulation and CSV file handling using `pandas`
  - 💾 User and book data persistence through CSV files

- **User Authentication**:
  - 🔒 User authentication and password encryption using SHA-256

- **Notifications**:
  - 📬 Notification system for users on the waiting list when books become available

- **Logging**:
  - 📝 Comprehensive logging system using the `logging` module to:
    - Track application events
    - Record errors and warnings
    - Log successful operations for auditing and debugging purposes

- **Design Patterns**:
  - 🏗️ **Decorator**: The `log_execution` decorator is used to log the execution of methods. It logs the method name, arguments, and the return value.
  - 🗂️ **Singleton**: Manages the single instance of the data manager
  - 🔄 **Strategy**: Defines and encapsulates various book search algorithms
  - 🔍 **Iterator**: Traverses and filters book collections efficiently
  - 📡 **Observer**: Manages notifications and waiting list updates

- **Graphical User Interface (GUI)**:
  - 🖥️ Developed using `Tkinter` for easy interaction
  - **Buttons and their placements**:
    - **Borrow Book**: Allows users to borrow a book, placed at the top left
    - **Return Book**: Allows users to return a book, placed next to the Borrow Book button
    - **View All Books**: Displays all books in the library, placed below the Borrow Book button
    - **View Available Books**: Displays only available books, placed next to the View All Books button
    - **View Loaned Books**: Displays loaned books, placed below the Return Book button
    - **View Popular Books**: Displays the most popular books, placed next to the View Loaned Books button

## Usage

1. **Navigate to the project directory:**
    ```sh
    cd library-management-system
    ```

2. **Install the required dependencies:**
    ```sh
    pip install pandas
    ```

3. **Run the application:**
    ```sh
    python main.py
    ```

4. **Use the GUI to interact with the library management system.**

## Project Structure

- `main.py`: Entry point of the application
- `User.py`: Contains user-related functionalities
- `DataManager.py`: Manages book and user data
- `Book.py`: Defines the Book class
- `books.csv`: Stores book data
- `users.csv`: Stores user data
- `waitingList.csv`: Stores waiting list data

## Code Capabilities

- **Data Management:** Efficiently handles book and user data using `pandas` and CSV files.
- **User Interaction:** Provides a user-friendly GUI for easy interaction with the system.
- **Authentication:** Ensures secure user authentication with SHA-256 encryption.
- **Notifications:** Notifies users when books become available.
- **Logging:** Tracks application events, errors, and successful operations for debugging and auditing.

## SOLID Principles Implementation

- **Single Responsibility Principle (SRP):** Each class in the project has a single responsibility. For example, `User.py` handles user-related functionalities, while `DataManager.py` manages book and user data.
- **Open/Closed Principle (OCP):** The system is designed to be easily extendable without modifying existing code. For example, new book search algorithms can be added using the Strategy pattern.
- **Liskov Substitution Principle (LSP):** Subclasses can replace their base classes without affecting the functionality. For example, different types of books can be managed using the same interface.
- **Interface Segregation Principle (ISP):** The system uses specific interfaces for different functionalities, ensuring that classes do not depend on methods they do not use.
- **Dependency Inversion Principle (DIP):** High-level modules do not depend on low-level modules. Both depend on abstractions. For example, the GUI interacts with the data manager through defined interfaces.

## Tests

- **Unit Tests**:
  - The project includes comprehensive unit tests using the `unittest` framework.
  - Tests cover various scenarios for the `User` class methods, including adding, removing, loaning, and returning books.