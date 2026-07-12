import os
import sqlite3
import uuid
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, g, after_this_request, send_file
from werkzeug.utils import secure_filename
from io import BytesIO
# Import crypto modules
from crypto.password_hasher import hash_password, verify_password
from crypto.aes_cipher import encrypt_file_aes, decrypt_file_aes
from crypto.fernet_cipher import encrypt_file_fernet, decrypt_file_fernet

# --- App Configuration ---
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG) # Set logging level to DEBUG
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

DATABASE = 'database.db'

# --- Database Setup ---
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        ''')
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(Flask, '_database', None)
    if db is not None:
        db.close()

# Initialize the database
init_db()

# --- Authentication Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        
        user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user:
            flash('Username already exists. Please choose another one.', 'danger')
            return redirect(url_for('register'))
            
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('register'))

        password_hash_val = hash_password(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash_val))
        db.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('login.html', is_register=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        
        user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user and verify_password(password, user['password_hash']):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html', is_register=False)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# --- Main Application Routes ---
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    print("=== ENCRYPT ROUTE HIT ===") # Force print to ensure route is called
    app.logger.debug("--- ENCRYPT ROUTE HIT ---") # Use logger as well
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        password = request.form.get('password')
        method = request.form.get('method')

        if not password or not method:
            flash('Password and encryption method are required.', 'danger')
            return redirect(request.url)

        if file:
            original_filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{original_filename}")
            output_filename = f"encrypted_{unique_id}_{original_filename}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            file.save(input_path)
            
            try:
                if method == 'aes':
                    encrypt_file_aes(input_path, output_path, password)
                elif method == 'fernet':
                    encrypt_file_fernet(input_path, output_path, password)
                else:
                    flash('Invalid encryption method selected.', 'danger')
                    return redirect(request.url)
                
                app.logger.info(f"File encrypted to: {output_path}")
                if os.path.exists(output_path):
                    app.logger.info(f"Encrypted file exists at {output_path}")
                    flash('File encrypted successfully!', 'success')
                    return redirect(url_for('download', filename=output_filename))
                else:
                    app.logger.error(f"Encrypted file NOT found at {output_path}")
                    flash('Error: Encrypted file not generated.', 'danger')
                    return redirect(request.url)
            except Exception as e:
                flash(f'An error occurred during encryption: {e}', 'danger')
                app.logger.error(f"Encryption error: {e}")
                # Clean up uploaded file on error
                if os.path.exists(input_path):
                    os.remove(input_path)
                return redirect(request.url) # Stop execution and reload page with error
            finally:
                # The cleanup of the input file is now handled in the main flow or the except block
                if 'output_path' in locals() and os.path.exists(input_path):
                     os.remove(input_path) # Clean up uploaded file only on success

    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        password = request.form.get('password')
        method = request.form.get('method')

        if not password or not method:
            flash('Password and decryption method are required.', 'danger')
            return redirect(request.url)

        if file:
            original_filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{original_filename}")
            
            # Adjust output filename to remove 'encrypted_' prefix if present
            if original_filename.startswith('encrypted_'):
                decrypted_filename = original_filename.replace('encrypted_', 'decrypted_', 1)
            else:
                decrypted_filename = f"decrypted_{unique_id}_{original_filename}"

            output_path = os.path.join(app.config['OUTPUT_FOLDER'], decrypted_filename)
            
            file.save(input_path)
            
            success = False
            try:
                if method == 'aes':
                    success = decrypt_file_aes(input_path, output_path, password)
                elif method == 'fernet':
                    success = decrypt_file_fernet(input_path, output_path, password)
                else:
                    flash('Invalid decryption method selected.', 'danger')
                    return redirect(request.url)

                if success:
                    flash('File decrypted successfully!', 'success')
                    return redirect(url_for('download', filename=decrypted_filename))
                else:
                    flash('Decryption failed. Please check your password and method.', 'danger')
                    if os.path.exists(output_path):
                        os.remove(output_path) # Clean up failed decryption attempt
            except Exception as e:
                flash(f'An error occurred during decryption: {e}', 'danger')
            finally:
                if os.path.exists(input_path):
                    os.remove(input_path) # Clean up uploaded file
    
    return render_template('decrypt.html')

@app.route('/download/<filename>')
def download(filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    app.logger.info(f"Attempting to provide file for download: {file_path}")

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        app.logger.error(f"File NOT found for download: {file_path}")
        flash('File not found or has already been downloaded.', 'danger')
        return redirect(url_for('index'))

    # Baca seluruh isi file ke memory dulu, baru hapus dari disk.
    # Ini menghindari race condition di Windows saat file masih
    # "dipegang" proses pengiriman tapi coba dihapus bersamaan.
    with open(file_path, 'rb') as f:
        file_data = f.read()

    try:
        os.remove(file_path)
        app.logger.info(f"Successfully cleaned up downloaded file: {file_path}")
    except Exception as e:
        app.logger.error(f"Error cleaning up file {file_path}: {e}")

    return send_file(
        BytesIO(file_data),
        as_attachment=True,
        download_name=filename,
        mimetype='application/octet-stream'
    )

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.makedirs(app.config['OUTPUT_FOLDER'])
    app.run(debug=True)