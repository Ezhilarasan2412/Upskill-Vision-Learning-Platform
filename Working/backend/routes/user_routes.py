from flask import Blueprint, render_template, request, jsonify, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from hashlib import sha256
from routes.user_routes import *
from routes.course_routes import *
from routes.module_routes import *
from routes.progress_routes import *
from routes.quiz_routes import *
from routes.resource_routes import *
from models.user_models import *
from models.course_models import *
from models.module_models import *
from models.progress_models import *
from models.quiz_models import *
from models.resource_models import *


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route('/')
def home():
    return render_template('index.html')


@user_blueprint.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user_id = data.get('user_id')
    role_id = data.get('role_id')  

    # Verify the user
    user = User.query.filter_by(email=email).first()

    if not user:
        return make_response('User does not exist', 401)
    
    # Check if the user's role matches the requested role
    if user.role_id != int(role_id):
        return make_response('Invalid role for the requested access.', 400)
    
    # Check if the user is approved
    if not user.is_approved:
        return make_response('Your account is pending approval. Please wait for HR to approve your account.', 403)

    stored_salt = user.salt
    entered_password_hash = sha256((password + stored_salt).encode('utf-8')).hexdigest()

    if entered_password_hash != user.password_hash:
        return make_response('Invalid email or password', 401)
    
    otp = generate_otp()
    global otp_storage
    otp_storage[user.email] = otp
    send_otp_email(user.email, otp)

    session['otp'] = otp
    session['email'] = user.email  
    session['role_id'] = user.role_id
    session['user_id'] = user.user_id  
    
    print(session)

    return jsonify({
    'message': 'Login successful. Please enter the OTP sent to your email for verification.',
    'user_id': user.user_id,
    'role_id': user.role_id
})
    

@user_blueprint.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


otp_storage = {}
def generate_otp():
    return random.randint(100000, 999999)


def send_otp_email(user_email, otp):
    sender_email = "tanayshah9045@gmail.com"  
    sender_password = "swju lauj yhlj gpji"
    recipient_email = user_email

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Your OTP for Login"

    body = f"Your OTP for login is: {otp}"
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
        print("OTP sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def send_email(to_email, subject, body):
    sender_email = "tanayshah9045@gmail.com"  
    sender_password = "swju lauj yhlj gpji"   

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")


@user_blueprint.route('/api/generate-otp', methods=['POST'])
def generate_otp1():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()

    if not user:
        return make_response('Email not found', 400)

    # Generate OTP
    otp = generate_otp()
    otp_storage[email] = otp

    # Send OTP to user's email
    send_otp_email(user.email, otp)

    return jsonify({'message': 'OTP sent to your email!'}), 200



@user_blueprint.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    otp_entered = data.get('otp')
    email = data.get('email')

    # Check if the OTP and email are provided
    if otp_entered is None or email is None:
        return make_response('OTP and email are required', 400)

    # Retrieve the stored OTP
    global otp_storage
    stored_otp = otp_storage.get(email)

    # Print the stored OTP and the entered OTP
    print(f"Stored OTP: {stored_otp}, Entered OTP: {otp_entered}")

    # Ensure the entered OTP is an integer for comparison
    try:
        otp_entered = int(otp_entered)  
    except ValueError:
        return make_response('OTP must be a valid integer', 400)

    # Check if OTP matches
    if stored_otp is None or stored_otp != otp_entered:
        return make_response('Invalid OTP', 401)

    # Clear OTP from storage after verification
    del otp_storage[email]

    return jsonify({'message': 'OTP verified successfully, you are logged in!'})


@user_blueprint.route('/api/password-reset/request', methods=['POST'])
def password_reset_request():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return make_response('Email not found', 400)

    # Hash the new password before saving it
    hashed_password = generate_password_hash(new_password)

    # Update the user's password in the database
    user.password_hash = hashed_password
    db.session.commit()

    return jsonify({'message': 'Password reset successful'}), 200


@user_blueprint.route('/api/roles', methods=['POST'])
def create_role():
    data = request.get_json()
    role_name = data.get('role_name')
    description = data.get('description')

    role = Role(role_name=role_name, description=description)
    db.session.add(role)
    db.session.commit()

    return jsonify({'message': 'Role created successfully'}), 201

@user_blueprint.route('/api/get_user_role', methods=['GET'])
def get_user_role():
    data = request.json
    email = data.get('email')
    if not email:
        print("No email in session") 
        return make_response(jsonify({'message': 'User not logged in.'}), 401)

    user = User.query.filter_by(email=email).first()
    if not user:
        print(f"User with email {email} not found.") 
        return make_response(jsonify({'message': 'User does not exist.'}), 404)

    print(f"User found: {user.username}, Role: {user.role_id}, User ID: {user.user_id}") 
    return jsonify({
        'role': user.role_id,
        'user_id': user.user_id
    }), 200



@user_blueprint.route('/api/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    roles_list = [{'role_id': role.role_id, 'role_name': role.role_name, 'description': role.description} for role in roles]
    return jsonify(roles_list), 200


@user_blueprint.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')
    first_name = data.get('first_name') 
    last_name = data.get('last_name')   
    

    # Validate data
    if not all([username, email, password, role_id, first_name, last_name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Password hashing
    salt = 'random_salt'
    password_hash = sha256((password + salt).encode('utf-8')).hexdigest()
    
    # Create a new user
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        salt=salt,
        role_id=role_id,
        first_name=first_name,  
        last_name=last_name,     
        is_approved=False
    )

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Registration successful. Awaiting approval.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 500


@user_blueprint.route('/api/users/approve/<int:user_id>', methods=['PUT'])
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_approved:
        return jsonify({'message': 'User is already approved.'}), 400
    
    user.is_approved = True
    db.session.commit()
    
    send_approval_email(user.email)
    
    return jsonify({'message': 'User approved successfully.'}), 200


def send_approval_email(user_email):
    sender_email = "tanayshah9045@gmail.com"  
    sender_password = "swju lauj yhlj gpji" 
    recipient_email = user_email

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Your Account Has Been Approved"

    body = "Congratulations! Your account has been approved. You can now log in to the system."
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
        print("Approval email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


@user_blueprint.route('/api/users/pending', methods=['GET'])
def get_pending_users():
    pending_users = User.query.filter_by(is_approved=False).all()
    if not pending_users:
        return jsonify({'message': 'No users pending approval.'}), 200
    
    users_data = [
        {
            'id': user.user_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role_id': user.role_id
        }
        for user in pending_users
    ]
    
    return jsonify({'pending_users': users_data}), 200


@user_blueprint.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'user_id': user.user_id, 'username': user.username, 'email': user.email, 'role_id': user.role_id} for user in users]
    return jsonify(users_list), 200


@user_blueprint.route('/api/users/<int:user_id>/assign-role', methods=['PUT'])
def assign_role(user_id):
    data = request.get_json()
    role_id = data.get('role_id')

    user = User.query.get(user_id)
    if not user:
        return make_response('User not found', 404)

    user.role_id = role_id
    db.session.commit()

    return jsonify({'message': 'Role assigned to user'}), 200