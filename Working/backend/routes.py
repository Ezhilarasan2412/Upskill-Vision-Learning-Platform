from flask import Blueprint, render_template, request, jsonify, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import User, Role, db
from flask import session
from datetime import datetime
from hashlib import sha256
from flask import request, make_response
from models import *


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


routes_blueprint = Blueprint('routes', __name__)


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


@routes_blueprint.route('/')
def home():
    return render_template('index.html')


@routes_blueprint.route('/api/login', methods=['POST'])
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



@routes_blueprint.route('/api/verify-otp', methods=['POST'])
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


@routes_blueprint.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


@routes_blueprint.route('/api/generate-otp', methods=['POST'])
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


@routes_blueprint.route('/api/password-reset/request', methods=['POST'])
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


@routes_blueprint.route('/api/roles', methods=['POST'])
def create_role():
    data = request.get_json()
    role_name = data.get('role_name')
    description = data.get('description')

    role = Role(role_name=role_name, description=description)
    db.session.add(role)
    db.session.commit()

    return jsonify({'message': 'Role created successfully'}), 201

@routes_blueprint.route('/api/get_user_role', methods=['GET'])
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



@routes_blueprint.route('/api/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    roles_list = [{'role_id': role.role_id, 'role_name': role.role_name, 'description': role.description} for role in roles]
    return jsonify(roles_list), 200


@routes_blueprint.route('/api/users', methods=['POST'])
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


@routes_blueprint.route('/api/users/approve/<int:user_id>', methods=['PUT'])
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


@routes_blueprint.route('/api/users/pending', methods=['GET'])
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


@routes_blueprint.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'user_id': user.user_id, 'username': user.username, 'email': user.email, 'role_id': user.role_id} for user in users]
    return jsonify(users_list), 200


@routes_blueprint.route('/api/users/<int:user_id>/assign-role', methods=['PUT'])
def assign_role(user_id):
    data = request.get_json()
    role_id = data.get('role_id')

    user = User.query.get(user_id)
    if not user:
        return make_response('User not found', 404)

    user.role_id = role_id
    db.session.commit()

    return jsonify({'message': 'Role assigned to user'}), 200


@routes_blueprint.route('/api/courses', methods=['POST'])
def create_course():
    """
    Create a new course with validation and error handling.
    """
    data = request.get_json()

    # Validation
    required_fields = ['course_name', 'description', 'start_date', 'end_date', 'instructor_id']
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    # Extract data
    course_name = data.get('course_name')
    description = data.get('description')
    instructor_id = data.get('instructor_id')

    try:
        # Parse dates
        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d")
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d")
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Validate instructor
    instructor = User.query.filter_by(user_id=instructor_id, role_id=3).first()
    if not instructor:
        return jsonify({'error': 'Invalid instructor ID or the user is not an instructor'}), 400

    try:
        # Create a new course
        new_course = Course(
            course_name=course_name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            instructor_id=instructor_id
        )
        db.session.add(new_course)
        db.session.commit()

        return jsonify({
            "course_id": new_course.course_id,  # Assuming course_id is the primary key
            "message": "Course created successfully"
        }), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"error": f"Failed to create course: {str(e)}"}), 500


from datetime import datetime

@routes_blueprint.route('/api/courses', methods=['GET'])
def get_courses():
    user_id = request.args.get('user_id')  # Get the user ID from the request
    
    courses = Course.query.all()
    
    if not courses:
        return jsonify({'message': 'No courses available.'}), 200
    
    # Fetch the user's enrollment status for all courses
    user_courses = {}
    if user_id:
        user_courses_query = UserCourse.query.filter_by(user_id=user_id).all()
        user_courses = {uc.course_id: uc.status for uc in user_courses_query}
    
    courses_list = []
    for course in courses:
        # Fetch the instructor based on the instructor_id in the course table
        instructor = User.query.get(course.instructor_id)
        
        # If the instructor exists, include their first and last name in the response
        instructor_name = f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown Instructor"
        
        # Format the start_date and end_date to display only the date part (YYYY-MM-DD)
        start_date = course.start_date.strftime('%Y-%m-%d') if course.start_date else "Unknown"
        end_date = course.end_date.strftime('%Y-%m-%d') if course.end_date else "Unknown"
        
        # Get enrollment and completion statuses
        user_status = user_courses.get(course.course_id, {})
        enrollment_status = user_status.get('status', "Not Enrolled")
        
        # # Determine enrollment status for the current user
        # enrollment_status = user_courses.get(course.course_id, "Not Enrolled")
        # if enrollment_status == "completed":
        #     enrollment_status = "Completed"
        # elif enrollment_status == "enrolled":
        #     enrollment_status = "Enrolled"
        
        # Append the course data with instructor information and formatted dates
        courses_list.append({
            'course_id': course.course_id,
            'course_name': course.course_name,
            'description': course.description,
            'start_date': start_date,
            'end_date': end_date,
            'instructor_name': instructor_name,  # Add the instructor's name
            'enrollment_status': enrollment_status  # Add enrollment status
        })
    
    return jsonify(courses_list), 200




@routes_blueprint.route('/api/user_courses', methods=['GET'])
def get_user_courses():
    user_id = request.args.get('user_id')  # Get user_id from request parameters

    # Fetch user courses and all courses in one go
    user_courses = {uc.course_id: uc.status for uc in UserCourse.query.filter_by(user_id=user_id).all()}
    all_courses = Course.query.all()

    courses_list = []
    for course in all_courses:
        enrollment_status = user_courses.get(course.course_id, "Not Enrolled")
        if enrollment_status == "completed":
            enrollment_status = "Completed"
        elif enrollment_status == "enrolled":
            enrollment_status = "Enrolled"

        instructor = User.query.get(course.instructor_id)
        instructor_name = f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown Instructor"

        courses_list.append({
            'course_id': course.course_id,
            'course_name': course.course_name,
            'description': course.description,
            'start_date': course.start_date.strftime('%Y-%m-%d'),
            'end_date': course.end_date.strftime('%Y-%m-%d'),
            'instructor_name': instructor_name,
            'enrollment_status': enrollment_status
        })

    return jsonify(courses_list), 200


@routes_blueprint.route('/api/enroll', methods=['POST'])
def enroll_course():
    data = request.json
    user_id = data.get('user_id')
    course_id = data.get('course_id')

    # Validate user_id
    if not user_id or not isinstance(user_id, int):
        return jsonify({'message': 'Invalid user_id provided.'}), 400
    
    # Validate course_id
    if not course_id or not isinstance(course_id, int):
        return jsonify({'message': 'Invalid course_id provided.'}), 400
    
    # Check if the user is already enrolled
    existing_enrollment = UserCourse.query.filter_by(user_id=user_id, course_id=course_id).first()
    if existing_enrollment:
        return jsonify({'message': 'User is already enrolled in this course.'}), 400

    # Enroll the user in the course
    new_enrollment = UserCourse(user_id=user_id, course_id=course_id, status='enrolled')
    db.session.add(new_enrollment)
    
    user = User.query.get(user_id)
    user.enrollment_count += 1
    
    course = Course.query.get(course_id)
    course.enrollment_count += 1
    
    # Create an entry in the Progress table to track the user's progress in the course
    modules = Module.query.filter_by(course_id=course_id).all()
    for module in modules:
        new_progress = Progress(user_id=user_id, module_id=module.module_id, completion_status='not started')
        db.session.add(new_progress)
    
    db.session.commit()
    
    return jsonify({'message': 'User successfully enrolled in the course and progress is initialized.'}), 200


@routes_blueprint.route('/api/enroll', methods=['GET'])
def get_enrolled_courses():
    user_id = request.args.get('user_id', type=int)

    # Validate user_id
    if not user_id:
        return jsonify({'message': 'User ID is required.'}), 400

    # Fetch enrolled courses for the user
    enrolled_courses = db.session.query(Course).join(UserCourse).filter(
        UserCourse.user_id == user_id, UserCourse.status == 'enrolled'
    ).all()
    
    print(enrolled_courses)  # Log the output to confirm


    if not enrolled_courses:
        return jsonify([]), 200

    # Serialize the courses
    serialized_courses = []
    for course in enrolled_courses:
        # Fetch the instructor's name
        instructor = User.query.get(course.instructor_id)
        instructor_name = f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown Instructor"

        # Add the serialized course
        serialized_courses.append({
            'course_id': course.course_id,
            'course_name': course.course_name,
            'description': course.description,
            'start_date': course.start_date.strftime('%Y-%m-%d') if course.start_date else 'TBD',
            'end_date': course.end_date.strftime('%Y-%m-%d') if course.end_date else 'TBD',
            'instructor_name': instructor_name,
            'enrollment_status': 'enrolled',  # Always 'Enrolled' since we're filtering enrolled courses
        })

    return jsonify(serialized_courses), 200



@routes_blueprint.route('/api/unenroll', methods=['POST'])
def unenroll_course():
    data = request.json
    user_id = data.get('user_id')
    course_id = data.get('course_id')

    # Check if the user is enrolled in the course
    enrollment = UserCourse.query.filter_by(user_id=user_id, course_id=course_id).first()
    if not enrollment:
        return jsonify({'message': 'User is not enrolled in this course.'}), 404

    # Remove the enrollment
    db.session.delete(enrollment)
    
    user = User.query.get(user_id)
    user.enrollment_count -= 1
    
    course = Course.query.get(course_id)
    course.enrollment_count -= 1
    
    db.session.commit()

    return jsonify({'message': 'User successfully unenrolled from the course.'}), 200


@routes_blueprint.route('/api/unenrolled', methods=['GET'])
def get_unenrolled_courses():
    user_id = request.args.get('user_id', type=int)

    # Validate user_id
    if not user_id:
        return jsonify({'message': 'User ID is required.'}), 400

    # Get all courses where the user is not enrolled
    enrolled_courses = db.session.query(Course).join(UserCourse).filter(
        UserCourse.user_id == user_id, UserCourse.status == 'enrolled'
    ).all()

    completed_courses = db.session.query(Course).join(UserCourse).filter(
        UserCourse.user_id == user_id, UserCourse.status == 'completed'
    ).all()

    # Get a list of course IDs that the user is enrolled in or completed
    enrolled_course_ids = {course.course_id for course in enrolled_courses}
    completed_course_ids = {course.course_id for course in completed_courses}

    # Combine both lists to exclude all courses that are either enrolled or completed
    excluded_course_ids = enrolled_course_ids.union(completed_course_ids)

    # Fetch courses that the user is not enrolled in or completed
    unenrolled_courses = db.session.query(Course).filter(Course.course_id.notin_(excluded_course_ids)).all()

    # If no unenrolled courses are found
    if not unenrolled_courses:
        return jsonify([]), 200

    user_courses = {uc.course_id: uc.status for uc in UserCourse.query.filter_by(user_id=user_id).all()}

    courses_list = []
    for course in unenrolled_courses:
        enrollment_status = user_courses.get(course.course_id, "Not Enrolled")
        if enrollment_status == "completed":
            enrollment_status = "Completed"
        elif enrollment_status == "enrolled":
            enrollment_status = "Enrolled"

        instructor = User.query.get(course.instructor_id)
        instructor_name = f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown Instructor"

        # Serialize the courses
        courses_list.append({
            'course_id': course.course_id,
            'course_name': course.course_name,
            'description': course.description,
            'start_date': course.start_date.strftime('%Y-%m-%d'),
            'end_date': course.end_date.strftime('%Y-%m-%d'),
            'instructor_name': instructor_name,
            'enrollment_status': enrollment_status
        })

    return jsonify(courses_list), 200


@routes_blueprint.route('/api/complete', methods=['POST'])
def complete_course():
    data = request.json
    user_id = data.get('user_id')
    course_id = data.get('course_id')

    # Check if the user is enrolled in the course
    enrollment = UserCourse.query.filter_by(user_id=user_id, course_id=course_id).first()
    if not enrollment or enrollment.status != 'enrolled':
        return jsonify({'message': 'User is not currently enrolled in this course.'}), 400

    # Update the status to 'completed'
    enrollment.status = 'completed'
    enrollment.completion_date = db.func.current_timestamp()
    
    user = User.query.get(user_id)
    user.courses_completed += 1
    
    
    db.session.commit()

    return jsonify({'message': 'Course successfully marked as completed.'}), 200


@routes_blueprint.route('/api/completed', methods=['GET'])
def get_completed_courses():
    user_id = request.args.get('user_id', type=int)

    # Validate user_id
    if not user_id:
        return jsonify({'message': 'User ID is required.'}), 400

    # Fetch completed courses for the user
    completed_courses = db.session.query(Course).join(UserCourse).filter(
        UserCourse.user_id == user_id, UserCourse.status == 'completed'
    ).all()

    if not completed_courses:
        return jsonify([]), 200

    # Serialize the courses
    serialized_courses = []
    for course in completed_courses:
        # Fetch the instructor's name
        instructor = User.query.get(course.instructor_id)
        instructor_name = f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown Instructor"

        # Add the serialized course
        serialized_courses.append({
            'course_id': course.course_id,
            'course_name': course.course_name,
            'description': course.description,
            'start_date': course.start_date.strftime('%Y-%m-%d') if course.start_date else 'TBD',
            'end_date': course.end_date.strftime('%Y-%m-%d') if course.end_date else 'TBD',
            'instructor_name': instructor_name,
            'enrollment_status': 'Completed'  # Mark as "Completed"
        })

    return jsonify(serialized_courses), 200


from datetime import datetime

@routes_blueprint.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return make_response('Course not found', 404)

    # Calculate duration in weeks if both dates are available
    duration_weeks = None
    if course.start_date and course.end_date:
        start_date = course.start_date
        end_date = course.end_date
        duration_weeks = (end_date - start_date).days // 7
        
    # Debug the date formats
    print("Start Date:", course.start_date)  # Check actual format
    print("End Date:", course.end_date)      # Check actual format
        
    course_data = {
        'course_id': course.course_id,
        'course_name': course.course_name,
        'description': course.description,
        'start_date': course.start_date.strftime("%Y-%m-%d") if course.start_date else None,
        'end_date': course.end_date.strftime("%Y-%m-%d") if course.end_date else None,
        'duration_weeks': duration_weeks,
        'instructor_id': course.instructor_id
    }

    return jsonify(course_data), 200



@routes_blueprint.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json()
    course = Course.query.get(course_id)
    
    if not course:
        return make_response('Course not found', 404)

    course.course_name = data.get('course_name', course.course_name)
    course.description = data.get('description', course.description)
    course.start_date = data.get('start_date', course.start_date)
    course.end_date = data.get('end_date', course.end_date)
    course.instructor_id = data.get('instructor_id', course.instructor_id)

    db.session.commit()

    return jsonify({'message': 'Course updated successfully'}), 200


@routes_blueprint.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        return make_response('Course not found', 404)

    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': 'Course deleted successfully'}), 200


@routes_blueprint.route('/api/instructors', methods=['GET'])
def get_instructors():
    try:
        instructors = User.query.filter_by(role_id=3).all()
        instructors_data = [
            {
                "user_id": instructor.user_id,
                "first_name": instructor.first_name,
                "last_name": instructor.last_name,
            }
            for instructor in instructors
        ]
        return jsonify(instructors_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@routes_blueprint.route('/api/courses/notify', methods=['POST'])
def send_course_notification():
    # Extract course_id from the request body
    course_id = request.json.get('course_id')
    if not course_id:
        return jsonify({"message": "Course ID is required"}), 400

    # Retrieve the course from the database
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    # Prepare the email content
    subject = f"New Course Available: {course.course_name}"
    body = f"""Dear team,

A new course has been created:

Title: {course.course_name}
Description: {course.description}
Start Date: {course.start_date}
End Date: {course.end_date}
Instructor: {course.instructor.username}

Enroll now to take part in this learning opportunity.
"""
    # Fetch all users to notify
    users = User.query.all()  # Adjust filtering as necessary
    for user in users:
        send_email(user.email, subject, body)

    return jsonify({"message": "Notification sent successfully"}), 200


@routes_blueprint.route('/api/courses/update-notify', methods=['POST'])
def send_course_update_notification():
    # Extract course_id from the request body
    course_id = request.json.get('course_id')
    if not course_id:
        return jsonify({"message": "Course ID is required"}), 400

    # Retrieve the course from the database
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    # Prepare the email content
    subject = f"Course Updated: {course.course_name}"
    body = f"""Dear team,

The following course has been updated:

Title: {course.course_name}
Description: {course.description}
Start Date: {course.start_date}
End Date: {course.end_date}
Instructor: {course.instructor.username}

Enroll now to take part in this learning opportunity.
"""
    # Fetch all users to notify
    users = User.query.all()  # Adjust filtering as necessary
    for user in users:
        send_email(user.email, subject, body)

    return jsonify({"message": "Notification sent successfully"}), 200


@routes_blueprint.route('/api/courses/delete-notify', methods=['POST'])
def send_delete_course_notification():
    # Extract course_id from the request body
    course_id = request.json.get('course_id')
    if not course_id:
        return jsonify({"message": "Course ID is required"}), 400

    # Retrieve the course from the database
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    # Prepare the email content
    subject = f"Course Deleted: {course.course_name}"
    body = f"""Dear team,

The following course has been deleted:

Title: {course.course_name}
Description: {course.description}
Start Date: {course.start_date}
End Date: {course.end_date}
Instructor: {course.instructor.username}

"""
    # Fetch all users to notify
    users = User.query.all()  # Adjust filtering as necessary
    for user in users:
        send_email(user.email, subject, body)

    return jsonify({"message": "Notification sent successfully"}), 200


# -------------------------------------------------------------------------------------------------------------


@routes_blueprint.route('/api/course-details/<int:course_id>', methods=['GET'])
def fetch_detailed_course(course_id):
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'message': 'User ID is required.'}), 400

    enrollment = Progress.query.filter_by(user_id=user_id).join(Module).filter(Module.course_id == course_id).first()
    if not enrollment:
        return jsonify({'message': 'User is not enrolled in this course.'}), 403

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found.'}), 404

    modules = Module.query.filter_by(course_id=course_id).order_by(Module.order_no).all()

    module_data = []
    for module in modules:
        progress = Progress.query.filter_by(user_id=user_id, module_id=module.module_id).first()

        resources = Resource.query.filter_by(module_id=module.module_id).all()
        resource_data = []
        completed_resources = 0
        
        for res in resources:
            resource_completed = (
        progress.resources_completed and isinstance(progress.resources_completed, (list, set)) and res.resource_id in progress.resources_completed
    ) if progress else False


            if resource_completed:
                completed_resources_count += 1

            resource_data.append({
                'resource_id': res.resource_id,
                'resource_title': res.resource_title,
                'resource_type': res.resource_type,
                'resource_content': res.resource_content,
                'completed': resource_completed  
            })

        # Determine the module's completion status based on resource completion
        all_resources_completed = len(resources) == completed_resources
        module_completion_status = 'completed' if all_resources_completed else progress.completion_status if progress else 'not started'

        # Fetch quiz 
        quiz = Quiz.query.filter_by(module_id=module.module_id).first()
        
        module_data.append({
            'module_id': module.module_id,
            'module_title': module.module_title,
            'learning_points': module.learning_points,
            'completion_status': module_completion_status,
            'resources': resource_data,
            'quiz_id': quiz.quiz_id if quiz else None 
        })

    return jsonify({
        'course_name': course.course_name,
        'description': course.description,
        'modules': module_data
    }), 200


@routes_blueprint.route('/api/complete-module', methods=['POST'])
def complete_module():
    data = request.json
    user_id = data.get('user_id')
    module_id = data.get('module_id')

    if not user_id or not module_id:
        return jsonify({'message': 'Missing user_id or module_id'}), 400

    progress = Progress.query.filter_by(user_id=user_id, module_id=module_id).first()
    if not progress:
        return jsonify({'message': 'No progress record found for this user and module.'}), 404

    progress.completion_status = 'completed'
    db.session.commit()

    return jsonify({'message': 'Module completed successfully.'}), 200


@routes_blueprint.route('/api/complete-resource', methods=['POST'])
def complete_resource():
    data = request.json
    user_id = data.get('user_id')
    resource_id = data.get('resource_id')

    if not user_id or not resource_id:
        return jsonify({'message': 'Missing user_id or resource_id'}), 400

    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({'message': 'Resource not found.'}), 404

    user_progress_for_resource = Progress.query.filter_by(user_id=user_id, module_id=resource.module_id).first()
    if not user_progress_for_resource:
        return jsonify({'message': 'No progress record found for this user and module.'}), 404

    if user_progress_for_resource.resources_completed >= Resource.query.filter_by(module_id=resource.module_id).count():
        return jsonify({'message': 'All resources for this module are already completed.'}), 400

    module_resources = Resource.query.filter_by(module_id=resource.module_id).count()
    completed_resources = user_progress_for_resource.resources_completed + 1
    user_progress_for_resource.resources_completed = completed_resources

    if completed_resources == module_resources:
        user_progress_for_resource.completion_status = 'completed'

    db.session.commit()

    return jsonify({
        'message': 'Resource marked as completed.',
        'resources_completed': completed_resources,
        'completion_status': user_progress_for_resource.completion_status
    }), 200


# Add Module to a Course
@routes_blueprint.route('/api/add-module', methods=['POST'])
def add_module():
    data = request.json
    course_id = int(data.get('course_id'))
    module_title = data.get('module_title')
    learning_points = data.get('learning_points', '')  
    order_no = int(data.get('order_no'))

    # Validate input
    if not course_id or not isinstance(course_id, int):
        return jsonify({'message': 'Invalid course_id provided.'}), 400
    if not module_title:
        return jsonify({'message': 'Module title is required.'}), 400
    if order_no is None or not isinstance(order_no, int):
        return jsonify({'message': 'Invalid order_no provided.'}), 400

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found.'}), 404

    # Add the new module to the course
    new_module = Module(course_id=course_id, 
                        module_title=module_title, 
                        learning_points=learning_points, 
                        order_no=order_no)
    db.session.add(new_module)
    db.session.commit()

    return jsonify({'message': 'Module added successfully to the course.'}), 200


@routes_blueprint.route('/api/courses/<int:course_id>/next-order', methods=['GET'])
def get_next_order_number(course_id):
    max_order = db.session.query(db.func.max(Module.order_no)).filter_by(course_id=course_id).scalar() or 0
    return jsonify({'next_order': max_order + 1})


@routes_blueprint.route('/api/course-modules/<int:course_id>', methods=['GET'])
def get_course_modules(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found.'}), 404

    modules = Module.query.filter_by(course_id=course_id).order_by(Module.order_no).all()
    if not modules:
        return jsonify({'message': 'No modules found for this course.'}), 404

    module_list = [{
        'module_id': module.module_id,
        'module_title': module.module_title,
        'learning_points': module.learning_points,
        'order_no': module.order_no
    } for module in modules]

    return jsonify({'modules': module_list}), 200


@routes_blueprint.route('/api/add-resource', methods=['POST'])
def add_resource():
    data = request.json
    module_id = data.get('module_id')
    resource_title = data.get('resource_title')
    resource_type = data.get('resource_type')  
    resource_content = data.get('resource_content')  

    # Validate module_id
    module = Module.query.get(module_id)
    if not module:
        return jsonify({'message': 'Module not found.'}), 404

    # Validate other fields
    if not resource_title or not resource_type or not resource_content:
        return jsonify({'message': 'Invalid input fields.'}), 400

    # Validate resource_type
    if resource_type not in ['link', 'file', 'text']:
        return jsonify({'message': "Invalid resource_type. Must be 'link', 'file', or 'text'."}), 400

    # For 'link' and 'file', validate URL format
    if resource_type in ['link', 'file']:
        if not resource_content.startswith(('http://', 'https://')):
            return jsonify({'message': 'Invalid URL. Must start with http:// or https://'}), 400

    new_resource = Resource(
        module_id=module_id,
        resource_title=resource_title,
        resource_type=resource_type,
        resource_content=resource_content
    )
    db.session.add(new_resource)
    db.session.commit()

    return jsonify({'message': 'Resource added successfully.', 'resource_id': new_resource.resource_id}), 200


# Update Module
@routes_blueprint.route('/api/modules/<int:module_id>', methods=['PUT'])
def update_module(module_id):
    data = request.json
    module = Module.query.get(module_id)

    if not module:
        return jsonify({'message': 'Module not found.'}), 404

    module.module_title = data.get('module_title', module.module_title)
    module.learning_points = data.get('learning_points', module.learning_points)
    module.order_no = data.get('order_no', module.order_no)

    db.session.commit()
    return jsonify({'message': 'Module updated successfully.'}), 200


# Update Resource
@routes_blueprint.route('/api/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    data = request.json
    resource = Resource.query.get(resource_id)

    if not resource:
        return jsonify({'message': 'Resource not found.'}), 404

    resource.resource_title = data.get('resource_title', resource.resource_title)
    resource.resource_content = data.get('resource_content', resource.resource_content)

    db.session.commit()
    return jsonify({'message': 'Resource updated successfully.'}), 200




@routes_blueprint.route('/api/quizzes', methods=['POST'])
def add_quiz():
    data = request.json
    module_id = data.get('module_id')
    quiz_title = data.get('quiz_title')
    total_score = data.get('total_score')
    passing_score = data.get('passing_score')

    quiz = Quiz(module_id=module_id, quiz_title=quiz_title, total_score=total_score, passing_score=passing_score)
    db.session.add(quiz)
    db.session.commit()

    return jsonify({'message': 'Quiz added successfully.','quiz_id': quiz.quiz_id}), 200


@routes_blueprint.route('/api/get-quizzes/<int:quiz_id>/<int:module_id>', methods=['GET'])
def get_quiz(quiz_id, module_id):
    # Validate quiz existence
    quiz = Quiz.query.filter_by(quiz_id=quiz_id, module_id=module_id).join(Module).filter(
        Module.module_id == module_id
    ).first()

    if not quiz:
        return jsonify({'message': 'Quiz not found or does not belong to the specified module/course.'}), 404

    # Fetch questions and answers for the quiz
    questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
    questions_data = []

    for question in questions:
        # Fetch answers for the question
        answers = QuizAnswer.query.filter_by(question_id=question.question_id).all()
        # Prepare answers data (exclude 'is_correct' to prevent revealing correct answers)
        answers_data = [{'answer_id': ans.answer_id, 'answer_text': ans.answer_text} for ans in answers]
        questions_data.append({
            'question_id': question.question_id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'answers': answers_data
        })

    # Construct response
    return jsonify({
        'quiz_title': quiz.quiz_title,
        'questions': questions_data,
        'module_id': module_id
    }), 200


@routes_blueprint.route('/api/modules/<int:module_id>/quizzes', methods=['GET'])
def get_quizzes_by_module(module_id):
    quizzes = Quiz.query.filter_by(module_id=module_id).all()
    if not quizzes:
        return jsonify({'message': 'No quizzes found for this module.'}), 404

    quizzes_data = [{'quiz_id': quiz.quiz_id, 'quiz_title': quiz.quiz_title, 'total_score': quiz.total_score, 'passing_score': quiz.passing_score} for quiz in quizzes]
    return jsonify({'quizzes': quizzes_data}), 200


@routes_blueprint.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
def quiz_submission(quiz_id):
    data = request.json
    user_id = data.get('user_id')
    answers = data.get('answers')

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'message': 'Quiz not found.'}), 404

    score = 0
    for question_id, answer_text in answers.items():
        correct_answers = QuizAnswer.query.filter_by(question_id=question_id, is_correct=True).all()
        correct_answer_texts = [ans.answer_text for ans in correct_answers]
        if answer_text in correct_answer_texts:
            score += 1

    progress = Progress.query.filter_by(user_id=user_id, module_id=quiz.module_id).first()
    if not progress:
        return jsonify({'message': 'Module progress not found.'}), 404

    # Determine pass/fail status
    pass_fail_status = 'Pass' if score >= quiz.passing_score else 'Fail'

    progress.quiz_score = score
    progress.pass_fail_status = pass_fail_status  # Ensure this column exists in Progress model
    db.session.commit()

    return jsonify({
        'message': 'Quiz submitted successfully.',
        'score': score,
        'status': pass_fail_status
    }), 200


@routes_blueprint.route('/api/quiz-performance', methods=['GET'])
def get_quiz_performance():
    user_id = request.args.get('user_id')
    module_id = request.args.get('module_id')

    progress = Progress.query.filter_by(user_id=user_id, module_id=module_id).first()
    if not progress:
        return jsonify({'message': 'User progress not found for this module.'}), 404

    return jsonify({
        'user_id': user_id,
        'module_id': module_id,
        'quiz_score': progress.quiz_score,
        'completion_status': progress.completion_status,
        'pass_fail_status': progress.pass_fail_status  # Added pass/fail status
    }), 200


@routes_blueprint.route('/api/quizzes/<int:quiz_id>/questions', methods=['POST'])
def add_question(quiz_id):
    data = request.json
    question_text = data.get('question_text')
    question_type = data.get('question_type')  # For example: "mcq"
    
    # Make sure the quiz exists before adding questions
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'message': 'Quiz not found.'}), 404
    
    # Create a new question
    question = QuizQuestion(quiz_id=quiz_id, question_text=question_text, question_type=question_type)
    db.session.add(question)
    db.session.commit()
    
    return jsonify({'message': 'Question added successfully.', 'question_id' : question.question_id}), 200

@routes_blueprint.route('/api/questions/<int:question_id>/answers', methods=['POST'])
def add_answer(question_id):
    data = request.json
    answer_text = data.get('answer_text')
    is_correct = data.get('is_correct')  # True/False
    
    # Make sure the question exists before adding answers
    question = QuizQuestion.query.get(question_id)
    if not question:
        return jsonify({'message': 'Question not found.'}), 404
    
    # Create a new answer
    answer = QuizAnswer(question_id=question_id, answer_text=answer_text, is_correct=is_correct)
    db.session.add(answer)
    db.session.commit()
    
    return jsonify({'message': 'Answer added successfully.'}), 200



# User Progress Overview
@routes_blueprint.route('/api/progress', methods=['GET'])
def user_progress_overview():
    # Fetch all users with role = 3 (participant)
    participants = User.query.filter_by(role_id=4).all()
    progress_data = []

    for participant in participants:
        progress = Progress.query.filter_by(user_id=participant.user_id).all()
        for p in progress:
            module = Module.query.get(p.module_id)
            if module:
                progress_data.append({
                    'user_id': participant.user_id,
                    'username': participant.username,
                    'module_title': module.module_title,
                    'completion_status': p.completion_status,
                    'quiz_score': p.quiz_score,
                    'resources_completed': p.resources_completed,
                    'pass_fail_status':p.pass_fail_status
                })

    return jsonify(progress_data), 200
