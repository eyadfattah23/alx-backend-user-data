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
- `GET /users/me`: retrieve the authenticated User object.

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
---

Sure! Here’s an explanation of each concept:

### 1. What Authentication Means
Authentication is the process of verifying the identity of a user, device, or system before granting access to resources. It ensures that users are who they claim to be, typically by requiring them to provide credentials, such as a username and password, or through other methods like tokens, biometrics, or multi-factor authentication. In web applications, authentication is a core component to restrict access to private data and protect user accounts.

### 2. What Session Authentication Means
Session authentication is a form of authentication where a user’s login credentials are verified, and a session is created to maintain the user's authenticated state. Once authenticated, the server creates a session for the user, storing the session ID on both the server (to identify the user) and the client (in a cookie). On subsequent requests, the server uses this session ID to identify and authorize the user without requiring them to log in again. This is common in traditional web applications where stateful sessions are managed on the server.

### 3. What Cookies Are
Cookies are small pieces of data stored on the client’s device by the web browser. They are used to remember information about the user, such as their preferences, shopping cart contents, or authentication session. Cookies are sent by the server to the browser and are stored locally on the client’s side. Each time the client makes a request to the same server, the browser automatically includes these cookies, allowing the server to maintain continuity of the user’s session.

### 4. How to Send Cookies
Cookies can be sent from the server to the client in the HTTP response headers. In web applications, they’re commonly set using the `Set-Cookie` header in an HTTP response, like this:

```http
HTTP/1.1 200 OK
Set-Cookie: sessionId=abc123; HttpOnly; Path=/
```

In a JavaScript-based client, you can also set cookies using the `document.cookie` property:

```javascript
document.cookie = "sessionId=abc123; path=/; HttpOnly";
```

When sending a request with cookies, the browser automatically includes cookies that match the domain and path in the `Cookie` header:

```http
GET /user HTTP/1.1
Host: example.com
Cookie: sessionId=abc123
```

### 5. How to Parse Cookies
To parse cookies, you need to read the `Cookie` header from the incoming HTTP request and extract the key-value pairs. Each cookie is separated by a semicolon (`;`), and each key-value pair is separated by an equals sign (`=`).

For example, in Python’s Flask:

```python
from flask import request

@app.route('/some_route')
def some_route():
    cookies = request.cookies  # returns a dictionary of cookies
    session_id = cookies.get("sessionId")  # get specific cookie by name
    return "Session ID: " + session_id
```

In JavaScript, you can parse cookies like this:

```javascript
const cookies = document.cookie.split('; ').reduce((acc, cookie) => {
  const [name, value] = cookie.split('=');
  acc[name] = value;
  return acc;
}, {});

console.log(cookies["sessionId"]);  // Access a specific cookie
```

### Summary
- **Authentication** verifies user identity.
- **Session Authentication** maintains an authenticated session via server-side session storage and a session ID cookie.
- **Cookies** are small data pieces stored on the client’s browser.
- **Sending Cookies** can be done with the `Set-Cookie` header.
- **Parsing Cookies** involves reading the `Cookie` header or using JavaScript to access `document.cookie`.

---


In Flask, the `request` object is an instance of the `Request` class and provides all the details about the incoming HTTP request. Here’s a comprehensive list of the primary attributes and methods available in `flask.request`:

### 1. Request Metadata and Context
- **`request.method`**: The HTTP method (e.g., `GET`, `POST`) used for the request.
- **`request.url`**: The complete URL of the request.
- **`request.base_url`**: The base URL, excluding any query string.
- **`request.path`**: The URL path of the request, e.g., `/api/v1/status`.
- **`request.full_path`**: The full URL path, including the query string.
- **`request.script_root`**: The root path of the application.
- **`request.url_root`**: The root URL, including the script root and a trailing slash.
- **`request.host`**: The host name of the server.
- **`request.host_url`**: The URL of the host.
- **`request.remote_addr`**: The IP address of the client.
- **`request.scheme`**: The scheme of the URL, like `http` or `https`.
- **`request.is_secure`**: Boolean indicating whether the request was sent over HTTPS.

### 2. Headers and Cookies
- **`request.headers`**: A dictionary-like object containing HTTP headers.
- **`request.cookies`**: A dictionary of cookies sent by the client.
- **`request.content_type`**: The MIME type of the request data.
- **`request.content_length`**: The length of the request body, in bytes.

### 3. Query Parameters and Form Data
- **`request.args`**: The parsed query string arguments, a `MultiDict` object (e.g., for `?key=value`).
- **`request.form`**: The parsed form data from a POST or PUT request, a `MultiDict` object.
- **`request.values`**: A combined `MultiDict` containing both `args` and `form`.
- **`request.data`**: The raw data of the request as bytes.
- **`request.json`**: The JSON payload parsed into a Python dictionary, if the request has JSON content.
- **`request.files`**: A `MultiDict` object of file uploads, if any.

### 4. Session and User-Related Information
- **`request.authorization`**: Contains an `Authorization` object, with `username` and `password` attributes if HTTP Basic Auth is used.
- **`request.remote_user`**: The `REMOTE_USER` of the request if set by an authentication mechanism.

### 5. Request-Specific Information
- **`request.endpoint`**: The endpoint for the matched route.
- **`request.view_args`**: The arguments passed to the view function.
- **`request.blueprint`**: The blueprint handling the request, if any.
- **`request.mimetype`**: The media type of the request, like `application/json`.
- **`request.mimetype_params`**: Parameters of the MIME type, if any (e.g., charset).

### 6. File and Input Stream
- **`request.stream`**: A file-like object for reading the request body.
- **`request.get_data()`**: Reads the raw data of the request as bytes.
- **`request.get_json(force=False, silent=False, cache=True)`**: Parses the request data as JSON.
  
### 7. Utility Methods
- **`request.get_cookie(key)`**: Retrieves a cookie by key.
- **`request.get_data(parse_form_data=False, as_text=False)`**: Returns the raw request data; optionally decodes it to text.
- **`request.get_host()`**: Returns the host including the port, if specified.

### 8. Environment and Context Variables
- **`request.environ`**: The WSGI environment dictionary for the request.
- **`request.blueprint`**: Returns the blueprint name if the request is served by a blueprint.

### Example Usage

In practice, here’s how you might use some of these attributes and methods:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/example', methods=['GET', 'POST'])
def example():
    # Accessing query parameters
    param = request.args.get('param', default="default value")

    # Accessing form data
    form_value = request.form.get('form_key')

    # Checking the request method
    method = request.method

    # Accessing JSON data
    if request.is_json:
        json_data = request.get_json()
    
    # Accessing headers
    user_agent = request.headers.get('User-Agent')
    
    # Accessing cookies
    session_cookie = request.cookies.get('session_id')

    # Full request info as JSON
    return jsonify({
        "method": method,
        "param": param,
        "form_value": form_value,
        "json_data": json_data,
        "user_agent": user_agent,
        "session_cookie": session_cookie
    })
```
