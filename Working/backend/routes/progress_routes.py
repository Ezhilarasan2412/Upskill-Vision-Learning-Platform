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

