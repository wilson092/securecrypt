import os
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def get_key_from_password(password: str, salt: bytes, key_length: int = 32) -> bytes:
    """Derive a key from a password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_file_aes(input_file: str, output_file: str, password: str):
    """Encrypts a file using AES-GCM."""
    salt = os.urandom(16)
    key = get_key_from_password(password, salt)
    
    nonce = os.urandom(12)  # GCM nonce
    aesgcm = algorithms.AES(key)
    cipher = Cipher(aesgcm, modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    try:
        logging.info(f"AES: Attempting to write encrypted file to {output_file}")
        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            # Write salt and nonce to the output file first
            f_out.write(salt)
            f_out.write(nonce)
            
            # Encrypt the file content
            while chunk := f_in.read(4096):
                encrypted_chunk = encryptor.update(chunk)
                f_out.write(encrypted_chunk)
                
            # Finalize the encryption and write the tag
            f_out.write(encryptor.finalize() + encryptor.tag)
        logging.info(f"AES: Successfully wrote encrypted file to {output_file}")
    except Exception as e:
        logging.error(f"AES: Failed to write file to {output_file}. Error: {e}")
        # Re-raise the exception to be caught by the Flask route
        raise

def decrypt_file_aes(input_file: str, output_file: str, password: str) -> bool:
    """Decrypts a file using AES-GCM. Returns True on success, False on failure."""
    try:
        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            # Read salt and nonce from the encrypted file
            salt = f_in.read(16)
            nonce = f_in.read(12)
            
            # The last 16 bytes are the GCM tag
            tag_and_ciphertext = f_in.read()
            tag = tag_and_ciphertext[-16:]
            ciphertext = tag_and_ciphertext[:-16]

            key = get_key_from_password(password, salt)
            
            aesgcm = algorithms.AES(key)
            cipher = Cipher(aesgcm, modes.GCM(nonce, tag), backend=default_backend())
            decryptor = cipher.decryptor()

            # Decrypt the ciphertext
            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
            f_out.write(decrypted_data)
            return True
    except Exception:
        # If decryption fails (e.g., wrong password leading to tag mismatch), clean up and return False
        if os.path.exists(output_file):
            os.remove(output_file)
        return False