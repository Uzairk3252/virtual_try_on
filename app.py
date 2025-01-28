from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session handling

# Mock user database
users = {
    "admin": {"password": "admin", "email": "admin@example.com", "phone": "1234567890"}
}

# Temporary storage for OTPs
otp_storage = {}

# Route: Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate user
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

# Route: Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']

        # Check if user exists
        if username in users:
            return render_template('signup.html', error="Username already exists.")
        
        # Save user details
        users[username] = {
            "password": password,
            "email": email,
            "phone": phone
        }
        return redirect(url_for('login'))
    return render_template('signup.html')

# Route: Home Page
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

# Route: Forgot Password
@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']

        # Check if user exists
        if username in users:
            otp = random.randint(1000, 9999)
            otp_storage[username] = otp
            # Simulate sending OTP (in real scenarios, use SMS/Email API)
            print(f"OTP for {username}: {otp}")
            return redirect(url_for('reset_password', username=username))
        else:
            return render_template('forgot.html', error="User does not exist.")
    return render_template('forgot.html')

# Route: Reset Password
@app.route('/reset/<username>', methods=['GET', 'POST'])
def reset_password(username):
    if request.method == 'POST':
        otp = request.form['otp']
        new_password = request.form['password']

        # Validate OTP
        if username in otp_storage and otp_storage[username] == int(otp):
            users[username]['password'] = new_password
            del otp_storage[username]  # Clear OTP after use
            return redirect(url_for('login'))
        else:
            return render_template('reset.html', username=username, error="Invalid OTP.")
    return render_template('reset.html', username=username)

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
