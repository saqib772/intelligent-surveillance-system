from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017')
db = client['ivssdb']
collection = db['users']
collection_contacts = db['Contacts']
collection_activity = db['Activity']
collection_logged_in_users = db['logged_in_users']

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if collection.find_one({'email': email}):
        return jsonify({'message': 'User already exists'}), 409

    collection.insert_one({'email': email, 'password': hashed_password})
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    user = collection.find_one({'email': email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        # Fetch user activities from 'Activity' collection
        user_activity = collection_activity.find({'email': email}, {'_id': 0})

        # Convert MongoDB cursor to a list of activities
        activities = list(user_activity)

        # Store user email and activities in 'logged_in_users' collection
        collection_logged_in_users.insert_one({'email': email, 'activities': activities})

        # Return login success message along with user email and activities
        return jsonify({'message': 'Login successful', 'email': email, 'activities': activities}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/', methods=['GET'])  # Define route for the root URL
def index():
    return jsonify({'message': 'Welcome to the backend!'})

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data received'}), 400

    # Extract form data
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    subject = data.get('subject')
    message = data.get('message')

    if not name or not email or not phone or not subject or not message:
        return jsonify({'message': 'Incomplete form data'}), 400

    # Store form data in MongoDB (collection1 for contacts)
    contact_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'subject': subject,
        'message': message
    }
    collection1.insert_one(contact_data)

    return jsonify({'message': 'Form data received and stored successfully'})
if __name__ == '__main__':
    app.run(debug=True)
