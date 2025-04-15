# Bluestock IPO API

A RESTful API for accessing IPO (Initial Public Offering) data for stock markets.

## Overview

Bluestock IPO API provides comprehensive data about upcoming, open, closed, and listed IPOs. It allows users to access company information, IPO details, pricing data, and more through a simple REST API.

## Features

- Detailed IPO information (dates, price bands, issue sizes, etc.)
- Company data and profiles
- Filtering by IPO status (upcoming, open, closed, listed)
- Search capabilities
- Authenticated API access

## Technologies

- Python 3.13+
- Django 5.0.6+
- Django REST Framework
- SQLite (development) / Postgres (recommended for production)

## Setup and Installation

### Prerequisites

- Python 3.13+
- pip (Python package manager)

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/bluestock.git
   cd bluestock/bluestock_project
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Access the API at http://127.0.0.1:8000/api/
   Access the admin interface at http://127.0.0.1:8000/admin/
   Access API documentation at http://127.0.0.1:8000/swagger/ or http://127.0.0.1:8000/redoc/

## API Authentication

The API supports multiple authentication methods:

1. **Session Authentication**: For web browser access (includes login/logout forms)
2. **Basic Authentication**: For simple username/password authentication
3. **API Key Authentication**: For programmatic access

### API Key Authentication

To use API key authentication:

1. Create a user and mark their profile as a client
2. Get the API key from the user profile
3. Include the API key in request headers:
   ```
   X-API-KEY: your-api-key-here
   ```

## API Endpoints

### Companies

#### List All Companies

- **URL**: `/api/companies/`
- **Method**: GET
- **Authentication**: Not required
- **Description**: Retrieve a list of all companies
- **Query Parameters**:
  - `search`: Search companies by name
  - `page`: Page number for pagination
- **Response Example**:
  ```json
  {
    "count": 100,
    "next": "http://127.0.0.1:8000/api/companies/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Example Company",
        "logo": "http://127.0.0.1:8000/media/company_logos/example.png",
        "created_at": "2025-04-01T12:00:00Z"
      },
      ...
    ]
  }
  ```

#### Get Company Details

- **URL**: `/api/companies/{id}/`
- **Method**: GET
- **Authentication**: Not required
- **Description**: Retrieve details of a specific company
- **Response Example**:
  ```json
  {
    "id": 1,
    "name": "Example Company",
    "logo": "http://127.0.0.1:8000/media/company_logos/example.png",
    "created_at": "2025-04-01T12:00:00Z"
  }
  ```

#### Create Company

- **URL**: `/api/companies/`
- **Method**: POST
- **Authentication**: Required
- **Content-Type**: `multipart/form-data` (for logo upload)
- **Description**: Create a new company
- **Request Body**:
  ```json
  {
    "name": "New Company",
    "logo": [file upload]
  }
  ```
- **Response**: The created company object

#### Update Company

- **URL**: `/api/companies/{id}/`
- **Method**: PUT/PATCH
- **Authentication**: Required
- **Description**: Update an existing company
- **Request Body**: Same as Create Company
- **Response**: The updated company object

#### Delete Company

- **URL**: `/api/companies/{id}/`
- **Method**: DELETE
- **Authentication**: Required
- **Description**: Delete a company
- **Response**: 204 No Content

### IPOs

#### List All IPOs

- **URL**: `/api/ipos/`
- **Method**: GET
- **Authentication**: Not required
- **Description**: Retrieve a list of all IPOs
- **Query Parameters**:
  - `status`: Filter by status (upcoming, open, closed, listed)
  - `company`: Filter by company ID
  - `upcoming`: Set to any value to get only upcoming IPOs
  - `open_now`: Set to any value to get only currently open IPOs
  - `search`: Search by company name or issue type
  - `ordering`: Order results (e.g., open_date, -open_date, -issue_size)
  - `page`: Page number for pagination
- **Response Example**:
  ```json
  {
    "count": 50,
    "next": "http://127.0.0.1:8000/api/ipos/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "company": 1,
        "company_name": "Example Company",
        "company_logo": "http://127.0.0.1:8000/media/company_logos/example.png",
        "price_band": "₹100 - ₹120",
        "price_band_min": "100.00",
        "price_band_max": "120.00",
        "open_date": "2025-04-20",
        "close_date": "2025-04-22",
        "issue_size": "10000000.00",
        "issue_type": "Fresh Issue",
        "listing_date": "2025-04-25",
        "status": "upcoming",
        "ipo_price": null,
        "listing_price": null,
        "listing_gain": null,
        "current_market_price": null,
        "current_return": null,
        "rhp_document": "http://127.0.0.1:8000/media/ipo_documents/rhp/example_rhp.pdf",
        "drhp_document": "http://127.0.0.1:8000/media/ipo_documents/drhp/example_drhp.pdf",
        "created_at": "2025-04-01T12:00:00Z"
      },
      ...
    ]
  }
  ```

#### Get IPO Details

- **URL**: `/api/ipos/{id}/`
- **Method**: GET
- **Authentication**: Not required
- **Description**: Retrieve details of a specific IPO
- **Response Example**: Same as single result in List All IPOs

#### Create IPO

- **URL**: `/api/ipos/`
- **Method**: POST
- **Authentication**: Required
- **Content-Type**: `multipart/form-data` (for document uploads)
- **Description**: Create a new IPO
- **Request Body**:
  ```json
  {
    "company": 1,
    "price_band_min": "100.00",
    "price_band_max": "120.00",
    "open_date": "2025-05-15",
    "close_date": "2025-05-17",
    "issue_size": "1000000.00",
    "issue_type": "Fresh Issue",
    "listing_date": "2025-05-24",
    "status": "upcoming",
    "ipo_price": null,
    "listing_price": null,
    "current_market_price": null,
    "rhp_document": [file upload],
    "drhp_document": [file upload]
  }
  ```
- **Response**: The created IPO object

#### Update IPO

- **URL**: `/api/ipos/{id}/`
- **Method**: PUT/PATCH
- **Authentication**: Required
- **Description**: Update an existing IPO
- **Request Body**: Same as Create IPO
- **Response**: The updated IPO object

#### Delete IPO

- **URL**: `/api/ipos/{id}/`
- **Method**: DELETE
- **Authentication**: Required
- **Description**: Delete an IPO
- **Response**: 204 No Content

### User Profiles

#### List User Profiles

- **URL**: `/api/profiles/`
- **Method**: GET
- **Authentication**: Required
- **Description**: Retrieve user profiles (admin users can see all profiles, regular users can only see their own)
- **Response Example**:
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "user": {
          "id": 1,
          "username": "exampleuser",
          "email": "user@example.com",
          "first_name": "Example",
          "last_name": "User"
        },
        "phone": "1234567890",
        "is_client": true,
        "api_key": "abcdef1234567890"
      }
    ]
  }
  ```

#### Get User Profile Details

- **URL**: `/api/profiles/{id}/`
- **Method**: GET
- **Authentication**: Required
- **Description**: Retrieve details of a specific user profile
- **Response Example**: Same as single result in List User Profiles

## API Response Codes

- `200 OK`: The request was successful
- `201 Created`: The resource was successfully created
- `204 No Content`: The request was successful (for DELETE operations)
- `400 Bad Request`: The request was invalid
- `401 Unauthorized`: Authentication is required or failed
- `403 Forbidden`: The authenticated user doesn't have permission to access the resource
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

## Error Responses

Error responses will follow this format:

```json
{
  "detail": "Error message goes here"
}
```

For validation errors:

```json
{
  "field_name": ["Error message for this field"]
}
```

## Tips for API Usage

1. Use filtering and search parameters to narrow down results
2. For listing IPOs, consider using the specialized filters:
   - `upcoming=true` for upcoming IPOs
   - `open_now=true` for currently open IPOs
3. Paginate results to improve performance

## Development and Production Notes

### For Development

- The development server uses SQLite by default
- Debug mode is enabled
- Media files are served by Django

### For Production

- Use a production-grade database like PostgreSQL
- Set `DEBUG = False` in settings
- Configure a proper media file serving solution
- Set up proper security measures (HTTPS, secure cookies, etc.)
- Configure allowed hosts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
