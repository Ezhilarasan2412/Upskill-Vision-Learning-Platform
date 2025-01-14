from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Root!1234@localhost/login_role_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    permissions = db.relationship('Permission', secondary='role_permissions', back_populates='roles')

    def __repr__(self):
        return f"Role('{self.role_name}', '{self.description}')"


class Permission(db.Model):
    __tablename__ = 'permissions'
    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    roles = db.relationship('Role', secondary='role_permissions', back_populates='permissions')

    def __repr__(self):
        return f"Permission('{self.permission_name}', '{self.description}')"


class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id', ondelete='CASCADE'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.permission_id', ondelete='CASCADE'), primary_key=True)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    enrollment_count = db.Column(db.Integer, default=0)
    courses_completed = db.Column(db.Integer, default=0)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.TIMESTAMP)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow())
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow(), onupdate=datetime.utcnow())
    role = db.relationship('Role', backref='users')


class AuthAttempt(db.Model):
    __tablename__ = 'auth_attempts'
    attempt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    attempt_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    is_successful = db.Column(db.Boolean)
    user = db.relationship('User', backref='auth_attempts')


class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    token_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    reset_token = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.TIMESTAMP, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    user = db.relationship('User', backref='password_reset_tokens')


class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    manager = db.relationship('User', backref='departments')


class UserDepartment(db.Model):
    __tablename__ = 'user_departments'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), primary_key=True)


db.Index('idx_username', User.username)
db.Index('idx_email', User.email)
db.Index('idx_role', User.role_id)
db.Index('idx_reset_token', PasswordResetToken.reset_token)


class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    enrollment_count = db.Column(db.Integer, default=0)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    instructor = db.relationship('User', backref='courses')

    def __repr__(self):
        return f"Course('{self.course_name}', '{self.start_date}', '{self.end_date}')"


class UserCourse(db.Model):
    __tablename__ = 'user_courses'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum('enrolled', 'completed', 'dropped'), default='enrolled')




# Modules Model
class Module(db.Model):
    __tablename__ = 'modules'
    module_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id', ondelete='CASCADE'), index=True, nullable=False)
    module_title = db.Column(db.String(100), nullable=False)
    learning_points = db.Column(db.Text, nullable=True)
    order_no = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Resources Model
class Resource(db.Model):
    __tablename__ = 'resources'
    resource_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.module_id', ondelete='CASCADE'), nullable=False)
    resource_title = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.Enum('link', 'file', 'text'), nullable=False)
    resource_content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Quizzes Model
class Quiz(db.Model):
    __tablename__ = 'quizzes'
    quiz_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.module_id', ondelete='CASCADE'), nullable=False)
    quiz_title = db.Column(db.String(100), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    passing_score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Quiz Questions Model
class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id', ondelete='CASCADE'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.Enum('mcq', 'true_false'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Quiz Answers Model
class QuizAnswer(db.Model):
    __tablename__ = 'quiz_answers'
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.question_id', ondelete='CASCADE'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)


# Progress Model
class Progress(db.Model):
    _tablename_ = 'progress'
    progress_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.module_id', ondelete='CASCADE'), nullable=False)
    completion_status = db.Column(db.Enum('not started', 'in progress', 'completed'), default='not started')
    resources_completed = db.Column(db.Integer, default=0)
    quiz_score = db.Column(db.Integer, default=0)
    pass_fail_status = db.Column(db.String(10))  # Add this line to store pass/fail status
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Course Reviews Model
class CourseReview(db.Model):
    __tablename__ = 'course_reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Course Leaderboard Model
class CourseLeaderboard(db.Model):
    __tablename__ = 'course_leaderboard'
    leaderboard_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    user_rank = db.Column(db.Integer, nullable=True)


# Course Tags Model
class CourseTag(db.Model):
    __tablename__ = 'course_tags'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), unique=True, nullable=False)


# Course Tag Mapping Model
class CourseTagMapping(db.Model):
    __tablename__ = 'course_tag_mapping'
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('course_tags.tag_id'), primary_key=True)


# Initialize Database
def create_tables():
    db.create_all()

    if Role.query.count() == 0:
        roles = [
            Role(role_name='HR Admin', description='Human Resources Administrator with full system access'),
            Role(role_name='Instructor', description='Training and course management'),
            Role(role_name='Manager', description='Team and performance monitoring'),
            Role(role_name='Participant', description='Program participant with limited access')
        ]
        db.session.add_all(roles)
        db.session.commit()

        permissions = [
            Permission(permission_name='READ_USER', description='View user information'),
            Permission(permission_name='EDIT_USER', description='Modify user details'),
            Permission(permission_name='CREATE_USER', description='Create new users'),
            Permission(permission_name='DELETE_USER', description='Remove users from system'),
            Permission(permission_name='VIEW_REPORTS', description='Access and generate reports'),
            Permission(permission_name='MANAGE_ROLES', description='Create and modify roles'),
            Permission(permission_name='APPROVE_SIGNUP', description='Approve new user registrations')
        ]
        db.session.add_all(permissions)
        db.session.commit()

        hr_admin = Role.query.filter_by(role_name='HR Admin').first()
        instructor = Role.query.filter_by(role_name='Instructor').first()
        manager = Role.query.filter_by(role_name='Manager').first()
        participant = Role.query.filter_by(role_name='Participant').first()

        read_user = Permission.query.filter_by(permission_name='READ_USER').first()
        edit_user = Permission.query.filter_by(permission_name='EDIT_USER').first()
        create_user = Permission.query.filter_by(permission_name='CREATE_USER').first()
        delete_user = Permission.query.filter_by(permission_name='DELETE_USER').first()
        view_reports = Permission.query.filter_by(permission_name='VIEW_REPORTS').first()
        manage_roles = Permission.query.filter_by(permission_name='MANAGE_ROLES').first()
        approve_signup = Permission.query.filter_by(permission_name='APPROVE_SIGNUP').first()

        role_permissions = [
            (hr_admin, [read_user, edit_user, create_user, delete_user, view_reports, manage_roles, approve_signup]),
            (instructor, [read_user, view_reports]),
            (manager, [read_user, view_reports]),
            (participant, [read_user])
        ]
        for role, perms in role_permissions:
            for perm in perms:
                role.permissions.append(perm)

        db.session.commit()