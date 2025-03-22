# EN4720 - Security in Cyber-Physical Systems

## Overview

This project provides a set of APIs for handling cryptographic operations and hashing functions in the context of Cyber-Physical Systems. The API allows secure key generation, encryption, decryption, hashing, and verification, along with a database for storing and retrieving cryptographic keys using key-id.

## Project Structure

```
/EN4720-Security-in-Cyber-Physical-Systems/
    │── API/
        |── SQL_Database/
            |── 
        │── api.py                      # Main Python script handling all API requests
        │── crypto_api.py               # Handles cryptographic API requests
        │── hashing_api.py              # Handles hashing API requests
        │── cryptographic_functions.py  # Functions for key generation, encryption, and decryption
        │── hashing_functions.py        # Functions for hashing and verification
        │── api_database.py             # Manages key storage and retrieval using key ID
        │── requirements.txt            # Required dependencies
```

## How to run

### **Method 1 (hosted URL)**

The API is already hosted online and can be accessed directly. Sending an HTTP request using the POST method, with the required variables included in the request body, is sufficient.

1. _However, response times may be approximately six seconds due to the application being hosted on a free platform, where both the API and database reside online with limited resources, resulting in potential latency._
2. _The SQL database is hosted on the FreeSQL platform, while the API is deployed on Vercel and Railway._

   - FreeSQL platform - https://www.freesqldatabase.com/
   - Vecel platform - https://vercel.com/
   - Railway.app platform - https://railway.com/

3. Hosted API URLs

   - To ensure the proper functionality of the hosted API URL, follow these steps:
     1. Open the URL in your browser before executing it in Postman.
     2. If the URL is running successfully, you should receive the following response:
        ```json
        {
          "message": "API Launched Successfully",
          "Team": "The Infected Crew",
          "Author": "Malanban"
        }
        ```
   - _URLs_

     ```
     https://vercel.com/anbus-projects-c25d417f/en4720-the-infected-crew
     ```

     ```
     https://en4720theinfectedcrew-production.up.railway.app/
     ```

### **Method 2 (localhost)**

Running the API script locally on your personal computer.

#### Database

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repository/EN4720-Security-in-Cyber-Physical-Systems.git
   ```

2. Install mysql

   - For **Windows**

     - Download MySQL from the [official MySQL website](https://dev.mysql.com/downloads/).
     - Run the installer and follow the setup wizard.

   - For **Linux**
     ```bash
     sudo apt update
     sudo apt install mysql-server
     ```

3. Verify Installation

   ```bash
   mysql --version
   ```

4. Import and execute the SQL query from `./API/SQL_Database/cyber_security_database.sql` to create the required database.

#### Run Python Script

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repository/EN4720-Security-in-Cyber-Physical-Systems.git
   ```

2. Installing Depedencies

   ```bash
   pip install -r requirements.txt
   ```

3. Navigate to the API directory:
   ```bash
   cd EN4720-Security-in-Cyber-Physical-Systems/API
   ```
4. Open api_database.py file:

   - _Update your username and password to the respective fields_

   ```python
       DB_CONFIG = {
        "host": "localhost",
        "user": "root",                #update with your SQL user
        "password": "Concy@280200",    #update with your SQL password
        "database": "cyber_security"
      }
   ```

5. Run the main API script:
   ```bash
   python api.py
   ```
   _This will start the API server and make the cryptographic and hashing functionalities accessible via HTTP requests._
6. Generated localhost URL
   ```
   http://127.0.0.1:5000
   ```

#### After Successfull Launch API Response

- Upon successful initialization, the API URL returns the following JSON response:

  ```json
  {
    "message": "API Launched Successfully",
    "Team": "The Infected Crew"
  }
  ```

## API Endpoints

### Cryptographic API

- **`/generate-key`**: Generates and stores a cryptographic key.
- **`/encrypt`**: Encrypts a given plaintext using a key-id and algorithm.
- **`/decrypt`**: Decrypts a given ciphertext using a key-id and algorithm.

### Hashing API

- **`/hash`**: Hashes a given input message.
- **`/verify-hash`**: Verifies a given hash against input data.

## Sample Request and Response

1. `REQUEST`: `\generate-key` method = ['POST']
   ```
   http://127.0.0.1:5000/generate-key
   ```
   Body:
   ```json
   {
     "key_type": "AES",
     "key_size": 256
   }
   ```
   `RESPONSE`:
   ```json
   {
     "key_id": 49,
     "key_value": "F+udBK1/qOd5MGOkhpm/ZHPg4XuL/YzR7lJhPfvi1cI="
   }
   ```

## Error Handling

The API follows structured error handling to ensure clarity and ease of debugging.

### 1. Database Connection Failure

Occurs when the database connection fails or does not exist.

```json
{
  "Database Connection Error": "{err}"
}
```

### 2. Unknown HTTP Request

Occurs when an invalid endpoint is accessed.

```json
{
  "error": "Not Found",
  "message": "The requested endpoint does not exist.",
  "status": 404
}
```

### 3. Unsupported HTTP Method

Occurs when an unsupported HTTP method is used (only POST requests are allowed).

```json
{
  "error": "Method Not Allowed",
  "message": "Use a valid HTTP method"
}
```

### 4. Invalid JSON Request Body

Occurs when the request body is not in valid JSON format.

```json
{
  "error": "Invalid request format. Expected JSON input."
}
```

### 5. Key-ID and Algorithm Mismatch

Occurs when there is a mismatch between the key ID and the algorithm.

```json
{
  "error": "KeyID_Type-{query_key_type} and Algorithm-{algorithm} Mismatch"
}
```

### 6. Decryption Algorithm Mismatch

Occurs when the decryption algorithm does not match the encrypted ciphertext algorithm.

```json
{
  "error": "Decryption failed: Invalid input data (Ciphertext with incorrect length.)"
}
```

### 7. Key ID Not Found

Occurs when the requested key ID does not exist.

```json
{
  "error": "Key ID 100 not found"
}
```

### 8. Unsupported Hashing Algorithm

Occurs when an unsupported hashing algorithm is used (only SHA-256 and SHA-512 are supported).

```json
{
  "error": "Unsupported algorithm. Supported: ['SHA-256', 'SHA-512']",
  "hash_value": null
}
```

## Contributers

- Miranda C.M.C.C 200396U
- Malanban K. 200373X
- Manimohan T. 200377M
- Nirushtihan B. 200431B
