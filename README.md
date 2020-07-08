# FSND Capstone Project: Book Shop API
### Full Stack Book Shop App
This is my capstone project for the Udacity Full stack Nanodegree. It is an flask backend api for a Bookshop that

contains books and book signing events.

Included in this project:
- Database modeling using PostgreSQL and SQLAlchemy
- Endpoints to perform CRUD operations on the database
- Automated Unit tests
- Third party authorization using Autho0
- Web deployment on Heroku<

### Getting Started
#### Installing Dependencies

##### Python 3.8

Follow instructions to install the latest version of python for your platform in the python docs

##### PIP Dependencies

In a virtual environment install dependencies by running:

`pip install -r requirements.txt`


### Running the server

#### Locally

Setup the database using the following command in the terminal

`create database fsndcapstone`

You can choose to populate the database with dummy data by uncommenting db.dummy_data() in app.py

Each time you open a new terminal session the environment variables need to be set. To do this run:

`source setup.sh`

To run the server run the command:

`flask run`

#### Production

The server is running on:

`https://fsndcapstonebooks.herokuapp.com/`

### Running Tests

Setup the test database using the following command in the terminal:

`create database fsndcapstone_test`

To run tests uncomment db.drop_all() from the setup_db function in models.py

Again each time you open a new terminal window you will need to load the env variables using:

`source setup.sh`

To run the tests run the command:

`python test_app.py`

### Endpoints

| Endpoints | Description | Required Permissions |
| ----------- | ----------- | ---------- |
| GET '/home' | Public endpoint to view all books | `None` |
| GET '/books/booksignings' | Returns a list of upcoming book signings.  | `None` |
| POST '/books/author' | Returns a list of books with authors who match a search string.  | `search:books` |
| POST '/books/title' | Returns a list of books with titles who match a search string. | `search:books` |
| POST '/books/new' | Posts a new book to the database  | `post:new_book` |
| PATCH '/books/<int:book_id>' | Edit the selected book.  | `patch:books` |
| DELETE '/books/<int:book_id>' | Delete the selected book.  | `delete:book` |

### Roles and their permissions

| Role | Permissions | 
| ----------- | ----------- |
| User | `search:books` |
| Admin | `search:books` `post:new_book` `patch:books` `delete:book` |
