import os
import base64
import logging
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def get_key_from_password_for_fernet(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode('utf-8'))
    return base64.urlsafe_b64encode(key)

def encrypt_file_fernet(input_file: str, output_file: str, password: str):
    """Encrypts a file using Fernet."""
    salt = os.urandom(16)
    key = get_key_from_password_for_fernet(password, salt)
    f = Fernet(key)

    try:
        logging.info(f"Fernet: Attempting to write encrypted file to {output_file}")
        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            # Write salt to the output file first
            f_out.write(salt)
            
            # Encrypt the file content
            data = f_in.read()
            encrypted_data = f.encrypt(data)
            f_out.write(encrypted_data)
        logging.info(f"Fernet: Successfully wrote encrypted file to {output_file}")
    except Exception as e:
        logging.error(f"Fernet: Failed to write file to {output_file}. Error: {e}")
        # Re-raise the exception to be caught by the Flask route
        raise

def decrypt_file_fernet(input_file: str, output_file: str, password: str) -> bool:
    """Decrypts a file using Fernet. Returns True on success, False on failure."""
    try:
        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            # Read salt and encrypted data
            salt = f_in.read(16)
            encrypted_data = f_in.read()

            key = get_key_from_password_for_fernet(password, salt)
            f = Fernet(key)
            
            # Decrypt the data
            decrypted_data = f.decrypt(encrypted_data)
            f_out.write(decrypted_data)
            return True
    except (InvalidToken, ValueError):
        # If decryption fails (e.g., wrong password), clean up and return False
        if os.path.exists(output_file):
            os.remove(output_file)
        return False