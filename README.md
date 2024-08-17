# Flask Input Validation Demo

This project demonstrates best practices for input validation in a Flask REST API. It includes a user signup route with detailed request filtering and input validation.

## Features

- User signup endpoint with input validation
- SQLite database for data storage
- Dockerized application
- Runs on port 8880

## Prerequisites

- Docker

## Getting Started

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/flask_input_validation_demo.git
   cd flask_input_validation_demo
   ```

2. Build the Docker image:
   ```
   docker build -t flask-input-validation-demo .
   ```

3. Run the container:
   ```
   docker run -p 8880:8880 flask-input-validation-demo
   ```

The API will now be accessible at `http://localhost:8880`.

## API Endpoints

### User Signup

- **URL**: `/signup`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body

```json
{
  "firstname": "John",
  "lastname": "Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "password": "SecurePass1!"
}
```

#### Successful Response

- **Code**: 201 Created
- **Content**:
  ```json
  {
    "message": "User created successfully"
  }
  ```

#### Error Response

- **Code**: 400 Bad Request
- **Content**:
  ```json
  {
    "errors": {
      "field_name": ["Error message"]
    }
  }
  ```

## Input Validation

The application uses Marshmallow for input validation. Here's the code snippet for the input validation schema:

```python
class UserSchema(Schema):
    firstname = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    lastname = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    email = fields.Email(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=18, max=120))
    password = fields.Str(required=True, validate=validate.Length(min=8))

    @validate.validator_for('password')
    def validate_password(self, value):
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one digit')
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError('Password must contain at least one special character')
```

## Testing

You can use tools like cURL or Postman to test the API. Here are some examples using cURL:

### Successful Request

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "firstname": "John",
  "lastname": "Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "password": "SecurePass1!"
}' http://localhost:8880/signup
```

### Negative Test Cases

1. Missing required field:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
     "lastname": "Doe",
     "email": "john.doe@example.com",
     "age": 30,
     "password": "SecurePass1!"
   }' http://localhost:8880/signup
   ```

2. Invalid email format:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
     "firstname": "John",
     "lastname": "Doe",
     "email": "invalid-email",
     "age": 30,
     "password": "SecurePass1!"
   }' http://localhost:8880/signup
   ```

3. Age out of range:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
     "firstname": "John",
     "lastname": "Doe",
     "email": "john.doe@example.com",
     "age": 15,
     "password": "SecurePass1!"
   }' http://localhost:8880/signup
   ```

4. Weak password:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
     "firstname": "John",
     "lastname": "Doe",
     "email": "john.doe@example.com",
     "age": 30,
     "password": "weakpass"
   }' http://localhost:8880/signup
   ```

5. Duplicate email (run this twice):
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
     "firstname": "John",
     "lastname": "Doe",
     "email": "john.doe@example.com",
     "age": 30,
     "password": "SecurePass1!"
   }' http://localhost:8880/signup
   ```

Each of these negative test cases should return a 400 Bad Request status code with specific error messages indicating the validation failures.

## Security Considerations

- This demo uses SQLite for simplicity. In a production environment, consider using a more robust database system.
- Ensure to use HTTPS in production to encrypt data in transit.
- Consider implementing rate limiting to prevent abuse of the API.
- Regularly update dependencies to patch any security vulnerabilities.