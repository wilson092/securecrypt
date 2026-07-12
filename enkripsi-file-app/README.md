# SecureCrypt: Web-Based File Encryption Tool

SecureCrypt is a web application built with Python and Flask that allows users to encrypt and decrypt files securely in their browser. It features user authentication and offers two strong encryption methods: AES and Fernet.

## Features

- **User Authentication**: Secure registration and login system with password hashing (bcrypt).
- **File Encryption**: Upload files and encrypt them using either AES-GCM or Fernet.
- **File Decryption**: Decrypt files by providing the correct password and method.
- **Password-Based Key Derivation**: Encryption keys are derived from user passwords using PBKDF2, ensuring passwords are never used directly as keys.
- **Secure File Handling**: Uploaded files are processed and deleted from the server to ensure privacy. Encrypted files are also removed after being downloaded.

## Tech Stack

- **Backend**: Python 3, Flask
- **Cryptography**: `cryptography` library (for AES & Fernet), `bcrypt` (for password hashing)
- **Database**: SQLite
- **Frontend**: HTML5, Bootstrap 5, CSS, JavaScript

## Project Structure

```
enkripsi-file-app/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── database.db           # SQLite database file
├── crypto/
│   ├── aes_cipher.py       # AES encryption/decryption logic
│   ├── fernet_cipher.py    # Fernet encryption/decryption logic
│   └── password_hasher.py  # Password hashing and verification
├── templates/
│   ├── base.html           # Base layout with navbar
│   ├── index.html          # Home page
│   ├── login.html          # Login and Register page
│   ├── encrypt.html        # Encryption form page
│   └── decrypt.html        # Decryption form page
├── static/
│   ├── css/style.css       # Custom stylesheets
│   └── js/main.js          # Custom JavaScript
├── uploads/              # Temporary storage for uploaded files
├── outputs/              # Temporary storage for encrypted/decrypted files
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd enkripsi-file-app
```

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages using `pip`.

```bash
pip install -r requirements.txt
```

## How to Run

1.  Make sure you are in the `enkripsi-file-app` directory and your virtual environment is activated.
2.  Run the Flask application:

    ```bash
    python app.py
    ```

3.  The application will start in debug mode and will be accessible at `http://127.0.0.1:5000` in your web browser.

4.  The application will automatically create the `database.db` file and the `uploads/` and `outputs/` directories if they don't exist.

## How to Use

1.  **Register**: Create a new account with a unique username and a strong password.
2.  **Login**: Log in with your credentials.
3.  **Encrypt**: Navigate to the "Encrypt" page, choose a file, set an encryption password (this can be different from your login password), and select a method (AES or Fernet).
4.  **Download**: The encrypted file will be automatically downloaded.
5.  **Decrypt**: Navigate to the "Decrypt" page, upload the encrypted file, provide the same password and method you used for encryption.
6.  **Download**: The original, decrypted file will be downloaded.