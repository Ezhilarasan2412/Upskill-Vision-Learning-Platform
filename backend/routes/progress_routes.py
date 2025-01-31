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


progress_blueprint = Blueprint("progress", __name__)


# User Progress Overview
@progress_blueprint.route('/api/progress', methods=['GET'])
def user_progress_overview():
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
                    'pass_fail_status':p.pass_fail_status,
                    'correct_answers': p.correct_answers,  
                    'incorrect_answers': p.incorrect_answers, 
                    'skipped_answers': p.skipped_answers  
                })

    return jsonify(progress_data), 200


# User Progress for Individual User
@progress_blueprint.route('/api/progress/user/<int:user_id>', methods=['GET'])
def user_progress(user_id):
    # Fetch progress for the specified user
    progress = Progress.query.filter_by(user_id=user_id).all()
    if not progress:
        return jsonify({'message': 'No progress found for this user.'}), 404

    progress_data = []
    for p in progress:
        module = Module.query.get(p.module_id)
        if module:
            progress_data.append({
                'module_title': module.module_title,
                'completion_status': p.completion_status,
                'quiz_score': p.quiz_score,
                'resources_completed': p.resources_completed,
                'pass_fail_status': p.pass_fail_status,
                'correct_answers': p.correct_answers,
                'incorrect_answers': p.incorrect_answers,
                'skipped_answers': p.skipped_answers
            })

    return jsonify(progress_data), 200


@progress_blueprint.route('/api/performance', methods=['GET'])
def get_filtered_performance():
    # Get the filter parameters from the query string
    course_name = request.args.get('course')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = db.session.query(Course)  # Querying the Course model

    # Apply filters based on the provided query parameters
    if course_name:
        query = query.filter(Course.course_name.ilike(f'%{course_name}%'))  # Use ilike for case-insensitive search
    if start_date:
        query = query.filter(Course.start_date >= datetime.strptime(start_date, '%Y-%m-%d').date())  # Convert string to date
    if end_date:
        query = query.filter(Course.end_date <= datetime.strptime(end_date, '%Y-%m-%d').date())  # Convert string to date

    filtered_data = query.all()

    # Manually create a dictionary for each course
    courses_list = []
    for course in filtered_data:
        courses_list.append({
            'course_id': course.course_id,
            'course_name': course.course_name,
            'description': course.description,
            'start_date': course.start_date.strftime('%Y-%m-%d'),
            'end_date': course.end_date.strftime('%Y-%m-%d'),
            'enrollment_count': course.enrollment_count,
            'instructor_id': course.instructor_id
        })

    # Return the filtered data as JSON
    return jsonify(courses_list)


@progress_blueprint.route('/api/participants/course-status', methods=['GET'])
def get_course_status():
    participants = User.query.filter_by(role_id=4).all()  # Fetch participants only
    participant_data = []

    for participant in participants:
        user_id = participant.user_id

        # Fetch enrolled (active) courses
        active_courses = db.session.query(Course.course_name).join(UserCourse).filter(
            UserCourse.user_id == user_id,
            UserCourse.status == 'enrolled'
        ).all()

        # Fetch completed courses
        completed_courses = db.session.query(Course.course_name).join(UserCourse).filter(
            UserCourse.user_id == user_id,
            UserCourse.status == 'completed'
        ).all()

        # Convert list of tuples to list of strings
        active_courses_list = [course[0] for course in active_courses]
        completed_courses_list = [course[0] for course in completed_courses]

        participant_data.append({
            "user_id": user_id,
            "name": f"{participant.first_name} {participant.last_name}",
            "active_courses": active_courses_list,  
            "completed_courses": completed_courses_list  
        })

    return jsonify(participant_data)