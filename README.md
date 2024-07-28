# Library-API
Welcome to the Library-API repository. This project features a digital library system that allows users to manage their own library by overseeing books and loan transactions.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#API-Endpoints)
- [License](#license)

## Description

Library Management System is a comprehensive web application designed to manage a library efficiently. It allows users to add, view, update, and delete books and loans with ease. The system is built using Flask, Flask-RESTful, and MongoDB, and it includes a robust Docker setup for easy deployment.

## Features

- Add new books and loans
- View existing books and loans
- Update book details
- Delete books and loans
- Multi-container Docker setup
- Nginx reverse proxy for load balancing and request routing

## Technologies Used

- Python
- Flask
- Flask-RESTful
- MongoDB
- Docker
- Docker Compose
- Nginx (for reverse proxy)

## Installation

To get a local copy up and running, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/gg2711/Library-API.git
   ```
2. Navigate to the project directory:
    ```bash
    cd Library
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Running the Docker Containers

1. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```
2. The books application will be accessible at http://5001.
3. The loans application will be accessible at http://5002.
4. The reverse proxy will be accessible at http://80.

## API Endpoints

- GET /books: Retrieve all books
- GET /books/<book_id>: Retrieve a specific book by ID
- GET /books/<field>=<value>: Retrieve specific books by a specific field
- POST /books: Add a new book
- PUT /books/<book_id>: Update a specific book by ID
- DELETE /books/<book_id>: Delete a specific book by ID
- GET /loans: Retrieve all loans
- GET /loans/<loan_id>: Retrieve a specific loan by ID
- GET /books/<field>=<value>: Retrieve specific loans by a specific field
- POST /loans: Add a new loan
- DELETE /loans/<loan_id>: Delete a specific loan by ID

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
