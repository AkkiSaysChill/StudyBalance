"""
Database Models for StudyBalance App
Using SQLAlchemy with SQLite (compatible with PostgreSQL)
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

# ==================================================
# USER MODEL
# ==================================================

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    quizzes = db.relationship(
        'Quiz',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )
    routines = db.relationship(
        'Routine',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )
    activities = db.relationship(
        'Activity',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

    # NEW: user badge relationship
    badges = db.relationship(
        'UserBadge',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    # ------------------------------
    # Password helpers
    # ------------------------------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # ------------------------------
    # JSON serializable representation
    # ------------------------------
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


# ==================================================
# BADGES
# ==================================================

class Badge(db.Model):
    __tablename__ = 'badges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(200))  # icon file path
    criteria_key = db.Column(db.String(100), nullable=False)

    user_badges = db.relationship('UserBadge', backref='badge', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'criteria_key': self.criteria_key
        }


class UserBadge(db.Model):
    __tablename__ = 'user_badges'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'badge': self.badge.to_dict(),
            'awarded_at': self.awarded_at.isoformat()
        }


# ==================================================
# QUIZ MODEL
# ==================================================

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    topic = db.Column(db.String(200), nullable=False)
    num_questions = db.Column(db.Integer, default=5)

    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    percentage = db.Column(db.Float)

    questions = db.Column(db.Text)        # JSON list stored as string
    user_answers = db.Column(db.Text)     # JSON dict stored as string

    duration_minutes = db.Column(db.Integer)

    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'topic': self.topic,
            'num_questions': self.num_questions,
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': self.percentage,
            'duration_minutes': self.duration_minutes,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat()
        }


# ==================================================
# ROUTINE MODEL
# ==================================================

class Routine(db.Model):
    __tablename__ = 'routines'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    wake_up_time = db.Column(db.String(10))  # HH:MM
    sleep_time = db.Column(db.String(10))

    study_duration = db.Column(db.Integer)
    break_duration = db.Column(db.Integer)
    exercise_duration = db.Column(db.Integer)

    subjects = db.Column(db.Text)        # JSON list
    environment = db.Column(db.String(50))

    preferences = db.Column(db.Text)     # JSON dict
    goals = db.Column(db.Text)
    challenges = db.Column(db.Text)

    routine_schedule = db.Column(db.Text)  # JSON list

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'wake_up_time': self.wake_up_time,
            'sleep_time': self.sleep_time,
            'study_duration': self.study_duration,
            'break_duration': self.break_duration,
            'exercise_duration': self.exercise_duration,
            'subjects': json.loads(self.subjects) if self.subjects else [],
            'environment': self.environment,
            'preferences': json.loads(self.preferences) if self.preferences else {},
            'goals': self.goals,
            'challenges': self.challenges,
            'routine_schedule': json.loads(self.routine_schedule) if self.routine_schedule else [],
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# ==================================================
# ACTIVITY LOG
# ==================================================

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    activity_type = db.Column(db.String(20))  # quiz | routine
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=True)
    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id'), nullable=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Linked objects
    quiz = db.relationship('Quiz', foreign_keys=[quiz_id])
    routine = db.relationship('Routine', foreign_keys=[routine_id])

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'quiz': self.quiz.to_dict() if self.quiz else None,
            'routine': self.routine.to_dict() if self.routine else None
        }
