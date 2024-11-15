# Simple API

Simple HTTP API for playing with `User` model.


## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)


----------------------------------------------------------------

### 1. What Authentication Means
**Authentication** is the process of verifying the identity of a user, device, or system to ensure that they are who they claim to be. In web applications, authentication typically involves checking credentials (such as a username and password) to grant access to specific resources or information. Common authentication methods include:

- **Basic Authentication** (using usernames and passwords)
- **Token-Based Authentication** (e.g., JWT tokens)
- **Multi-Factor Authentication (MFA)** (requiring additional verification methods, like a code sent to a phone)
- **OAuth** (often used for social logins and third-party apps)

The goal of authentication is to secure systems by ensuring that only authorized users can access sensitive data.

### 2. What Base64 Is
**Base64** is an encoding scheme that converts binary data into a text format using a set of 64 characters: A-Z, a-z, 0-9, `+`, and `/`. This encoding is commonly used for data transmission over media designed to handle text, ensuring data is not altered during transit.

In web contexts, Base64 is often used for:
- Encoding binary data, like images, into strings to be embedded in HTML or CSS
- Encoding credentials for HTTP Basic Authentication
- Encoding data in JSON Web Tokens (JWTs)

### 3. How to Encode a String in Base64
Encoding a string in Base64 depends on the programming language you are using. Here are examples in two popular languages:

- **JavaScript**:
  ```js
  const str = "Hello, World!";
  const base64Encoded = Buffer.from(str).toString('base64');
  console.log(base64Encoded); // Outputs: SGVsbG8sIFdvcmxkIQ==
  ```

- **Python**:
  ```python
  import base64
  str = "Hello, World!"
  base64_encoded = base64.b64encode(str.encode()).decode()
  print(base64_encoded)  # Outputs: SGVsbG8sIFdvcmxkIQ==
  ```

### 4. What Basic Authentication Means
**Basic Authentication** is an HTTP authentication scheme that sends the user's credentials (username and password) as a Base64-encoded string in the `Authorization` header of an HTTP request. It is called "basic" because of its simplicity but is generally insecure unless used over HTTPS, as credentials are easily decoded.

Here’s how Basic Authentication works:
1. The client sends a request for a protected resource.
2. The server responds with a `401 Unauthorized` status and a `WWW-Authenticate: Basic` header, indicating that authentication is required.
3. The client then resends the request with an `Authorization` header containing the word "Basic" followed by the Base64-encoded string of `username:password`.

### 5. How to Send the Authorization Header
To send the `Authorization` header in a request, you need to set the header properly. Here’s how it’s typically done:

- **JavaScript (using fetch)**:
  ```js
  const username = "yourUsername";
  const password = "yourPassword";
  const credentials = btoa(`${username}:${password}`);

  fetch('https://example.com/protected-resource', {
    method: 'GET',
    headers: {
      'Authorization': `Basic ${credentials}`
    }
  }).then(response => {
    // Handle response
  });
  ```

- **Python (using requests library)**:
  ```python
  import requests
  from requests.auth import HTTPBasicAuth

  url = "https://example.com/protected-resource"
  response = requests.get(url, auth=HTTPBasicAuth('yourUsername', 'yourPassword'))
  ```

In both examples, the `Authorization` header includes the keyword "Basic" followed by the Base64-encoded credentials. This enables the server to decode and verify the credentials to authenticate the client.

### 6. What are authentication and authorization?

In simple terms, authentication is the process of verifying who a user is, while authorization is the process of verifying what they have access to.

Comparing these processes to a real-world example, when you go through security in an airport, you show your ID to authenticate your identity. Then, when you arrive at the gate, you present your boarding pass to the flight attendant, so they can authorize you to board your flight and allow access to the plane.
