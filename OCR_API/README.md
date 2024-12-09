# OCR API

The OCR API is a Flask-based RESTful API designed to manage applicant data extracted from Optical Character Recognition (OCR) systems. It connects to a Microsoft SQL Server database and provides various endpoints for fetching, filtering, and managing applicant information.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Folder Structure](#folder-structure)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [API Endpoints](#api-endpoints)
8. [Error Handling](#error-handling)
9. [Contributing](#contributing)
10. [License](#license)

---

## Project Overview

This project provides a backend API to:

- Fetch applicant details from a Microsoft SQL Server database.
- Filter and paginate results based on query parameters.
- Provide secure access using token-based authentication.

---

## Features

- **Fetch All Applicants:** Retrieve a complete list of applicants.
- **Filter Applicants:** Filter by Aadhaar number, applicant name, or verification status.
- **Paginate Results:** Paginate the output for large datasets.
- **Authentication:** Secure the API with token-based authentication.

---

## Folder Structure

```text
OCR_API/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── auth.py                  # Authentication module
│   ├── routes/
│   │   ├── __init__.py          # Blueprint setup
│   │   ├── endpoints.py
|   |   |── routes.py
│   │   └── services.py          # Business logic for handling requests
│   ├── database/
│   │   ├── __init__.py          # Initializes database module
│   │   ├── db_connection.py     # Database connection setup
│   │   └── database.py          # SQL commands and data fetching logic
│   └── config/
│       └── config.py            # Configuration for DB settings
├── main.py                      # Entry point to start the Flask app
└── README.md                    # Project documentation
```
