# Study-Life Balance Application

from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
import requests
import json
from models import db, User, Quiz, Routine, Activity, Badge, UserBadge
from datetime import datetime

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'), static_url_path='/static', instance_relative_config=True)
app.secret_key = 'your-secret-key-change-this-in-production'

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "study_balance.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize database
db.init_app(app)

# OpenRouter API Configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


# ====================== BADGE MILESTONE SYSTEM ======================
# Dictionary mapping milestones to badge criteria_key
BADGE_MILESTONES = {
    "first_quiz": {
        "milestone": 1,
        "metric": "total_quizzes",
        "badge_name": "First Quiz!",
        "description": "Completed your first quiz.",
    },
    "quiz_3": {
        "milestone": 3,
        "metric": "total_quizzes",
        "badge_name": "Quiz Beginner",
        "description": "Completed 3 quizzes.",
    },
    "quiz_5": {
        "milestone": 5,
        "metric": "total_quizzes",
        "badge_name": "Quiz Enthusiast",
        "description": "Completed 5 quizzes.",
    },
    "quiz_10": {
        "milestone": 10,
        "metric": "total_quizzes",
        "badge_name": "Quiz Expert",
        "description": "Completed 10 quizzes.",
    },
    "perfect_score": {
        "milestone": 100,
        "metric": "highest_score",
        "badge_name": "Perfect Score",
        "description": "Scored 100% on a quiz.",
    },
    "first_routine": {
        "milestone": 1,
        "metric": "total_routines",
        "badge_name": "Routine Starter",
        "description": "Created your first study routine.",
    },
    "routine_3": {
        "milestone": 3,
        "metric": "total_routines",
        "badge_name": "Routine Builder",
        "description": "Created 3 study routines.",
    },
    "routine_5": {
        "milestone": 5,
        "metric": "total_routines",
        "badge_name": "Routine Master",
        "description": "Created 5 study routines.",
    },
    "activities_10": {
        "milestone": 10,
        "metric": "total_activities",
        "badge_name": "Activity Lover",
        "description": "Completed 10 activities.",
    },
    "activities_50": {
        "milestone": 50,
        "metric": "total_activities",
        "badge_name": "Activity Star",
        "description": "Completed 50 activities.",
    },
}


def check_and_award_badges(user):
    """
    Award badges to user based on milestones defined in BADGE_MILESTONES dictionary.
    Works for both new and existing users.
    """
    badges_awarded = []
    
    # Get existing badges for this user
    owned_badges = {ub.badge_id for ub in UserBadge.query.filter_by(user_id=user.id).all()}
    
    # Calculate user stats
    total_quizzes = Quiz.query.filter_by(user_id=user.id).count()
    highest_score = db.session.query(db.func.max(Quiz.score)).filter_by(user_id=user.id).scalar() or 0
    total_routines = Routine.query.filter_by(user_id=user.id).count()
    total_activities = Activity.query.filter_by(user_id=user.id).count()
    
    # Build user stats dictionary
    user_stats = {
        "total_quizzes": total_quizzes,
        "highest_score": highest_score,
        "total_routines": total_routines,
        "total_activities": total_activities,
    }
    
    # Iterate through BADGE_MILESTONES dictionary
    for criteria_key, milestone_data in BADGE_MILESTONES.items():
        metric_name = milestone_data["metric"]
        required_value = milestone_data["milestone"]
        badge_name = milestone_data["badge_name"]
        badge_description = milestone_data["description"]
        
        # Check if user has reached this milestone
        current_value = user_stats.get(metric_name, 0)
        
        if current_value >= required_value:
            # Get or create the badge
            badge = Badge.query.filter_by(criteria_key=criteria_key).first()
            
            if not badge:
                # Create badge if it doesn't exist
                badge = Badge(
                    name=badge_name,
                    description=badge_description,
                    criteria_key=criteria_key,
                    icon=f"{criteria_key}.png"
                )
                db.session.add(badge)
                db.session.flush()  # Get the badge ID without committing
            
            # Award badge if user doesn't have it
            if badge.id not in owned_badges:
                user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
                db.session.add(user_badge)
                
                # Create activity log entry
                activity = Activity(
                    user_id=user.id,
                    activity_type='badge',
                    title='New Badge Earned!',
                    description=f'You earned the "{badge.name}" badge! ({badge_description})'
                )
                db.session.add(activity)
                
                badges_awarded.append(badge.name)
                owned_badges.add(badge.id)
    
    # Commit all changes at once
    if badges_awarded:
        db.session.commit()
    
    return badges_awarded


# Function to generate AI quiz questions
def generate_quiz_questions(topic, num_questions=5):
    """
    Generate AI quiz questions using OpenRouter API
    """
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Generate exactly {num_questions} multiple choice quiz questions about '{topic}' for a student study app.
        
        Format the response as a JSON array with this structure:
        [
            {{
                "question": "Question text?",
                "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                "correct_answer": "A"
            }}
        ]
        
        Only return valid JSON, no other text."""
        
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Parse the JSON response
        questions = json.loads(content)
        return questions
        
    except Exception as e:
        print(f"Error generating quiz: {str(e)}")
        return None


# Function to generate study routine
def generate_study_routine(routine_data):
    """
    Generate a personalized study routine using OpenRouter API
    """
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Create a detailed daily study routine based on these preferences:
        - Wake up time: {routine_data.get('wakeUpTime')}
        - Sleep time: {routine_data.get('sleepTime')}
        - Subjects: {', '.join(routine_data.get('subjects', []))}
        - Study session: {routine_data.get('studyDuration')} minutes
        - Break duration: {routine_data.get('breakDuration')} minutes
        - Exercise time: {routine_data.get('exerciseDuration')} minutes
        - Preferred environment: {routine_data.get('environment')}
        - Study methods: {', '.join(routine_data.get('preferences', [])) if routine_data.get('preferences') else 'Flexible'}
        - Goals: {routine_data.get('goals', 'General learning')}
        - Challenges: {routine_data.get('challenges', 'None')}
        
        Return as a numbered list of routine activities/time blocks (7-10 items). 
        Include specific times, activities, and tips to maintain focus and avoid challenges.
        Format as simple numbered list (1. 2. 3. etc) with activity name and time."""
        
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Parse the response into a list of routine items
        routine_items = content.strip().split('\n')
        routine_items = [item.strip() for item in routine_items if item.strip()]
        
        return routine_items
        
    except Exception as e:
        print(f"Error generating routine: {str(e)}")
        return None



# main route
@app.route('/')
@login_required
def home():
    return render_template('index.html')


def compute_user_stats(user_id):
    quizzes = Quiz.query.filter_by(user_id=user_id).all()
    routines = Routine.query.filter_by(user_id=user_id).all()
    activities = Activity.query.filter_by(user_id=user_id).all()

    total_score = sum(q.score for q in quizzes if q.score) if quizzes else 0
    avg_score = total_score / len(quizzes) if quizzes else 0

    return {
        "total_quizzes": len(quizzes),
        "total_routines": len(routines),
        "total_activities": len(activities),
        "average_quiz_score": round(avg_score, 2),
        "highest_score": max([q.score for q in quizzes if q.score], default=0)
    }

# get user badges
@app.route('/get-user-badges')
@login_required
def get_user_badges():
    # Fetch existing badges from DB
    existing_user_badges = UserBadge.query.filter_by(user_id=current_user.id).all()
    existing_badge_ids = {b.badge_id for b in existing_user_badges}

    # Fetch user stats
    stats = compute_user_stats(current_user.id)

    # Use BADGE_MILESTONES to evaluate what badges the user should have
    badges_to_return = []

    for criteria_key, milestone in BADGE_MILESTONES.items():
        metric = milestone.get('metric')
        required = milestone.get('milestone')

        user_value = stats.get(metric, 0)

        # Find or create the badge record
        badge_obj = Badge.query.filter_by(criteria_key=criteria_key).first()
        if not badge_obj:
            # Create the badge record if missing
            badge_obj = Badge(
                name=milestone.get('badge_name'),
                description=milestone.get('description'),
                criteria_key=criteria_key,
                icon=f"{criteria_key}.png"
            )
            db.session.add(badge_obj)
            db.session.commit()

        # Award if user reached milestone and doesn't already have it
        if user_value >= required and badge_obj.id not in existing_badge_ids:
            new_user_badge = UserBadge(user_id=current_user.id, badge_id=badge_obj.id)
            db.session.add(new_user_badge)
            activity = Activity(
                user_id=current_user.id,
                activity_type='badge',
                title='New Badge Earned!',
                description=f'You earned the "{badge_obj.name}" badge!'
            )
            db.session.add(activity)
            db.session.commit()
            existing_badge_ids.add(badge_obj.id)

        # If user owns it, include in response
        if badge_obj.id in existing_badge_ids:
            badges_to_return.append(badge_obj.to_dict())

    return jsonify({"success": True, "badges": badges_to_return})


# ai quiz page redirect with questions
@app.route('/ai-quiz', methods=['GET', 'POST'])
@login_required
def ai_quiz():
    if request.method == 'POST':
        data = request.json
        topic = data.get('topic', 'General Knowledge')
        num_questions = int(data.get('num_questions', 5))
        
        questions = generate_quiz_questions(topic, num_questions)
        
        if questions:
            return jsonify({"success": True, "questions": questions})
        else:
            return jsonify({"success": False, "error": "Failed to generate questions"}), 500
    
    return render_template('quiz.html')


# save quiz results to database
@app.route('/save-quiz-results', methods=['POST'])
@login_required
def save_quiz_results():
    """
    Save quiz results to database
    """
    try:
        data = request.json
        user_id = current_user.id  # Get from logged-in user
        
        # Create quiz record
        quiz = Quiz(
            user_id=user_id,
            topic=data.get('topic'),
            num_questions=data.get('totalQuestions'),
            score=data.get('score'),
            total_questions=data.get('totalQuestions'),
            percentage=data.get('percentage'),
            questions=json.dumps(data.get('questions', [])),
            user_answers=json.dumps(data.get('userAnswers', {})),
            duration_minutes=data.get('duration', 0)
        )
        
        db.session.add(quiz)
        db.session.commit()

        new_badges = check_and_award_badges(current_user)

        
        # Create activity record
        activity = Activity(
            user_id=user_id,
            activity_type='quiz',
            quiz_id=quiz.id,
            title=f"{data.get('topic')} Quiz",
            description=f"Score: {data.get('score')}/{data.get('totalQuestions')} ({data.get('percentage')}%)"
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({"success": True, "message": "Quiz saved successfully", "quiz_id": quiz.id, "new_badges": new_badges})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error saving quiz: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/routine')
@login_required
def routine():
    return render_template('routine.html')


# generate routine endpoint
@app.route('/generate-routine', methods=['POST'])
def generate_routine():
    try:
        routine_data = request.json
        
        if not routine_data or not routine_data.get('subjects'):
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        # Generate routine using AI
        routine = generate_study_routine(routine_data)
        
        if routine:
            return jsonify({
                "success": True,
                "routine": routine,
                "data": routine_data
            })
        else:
            return jsonify({"success": False, "error": "Failed to generate routine"}), 500
            
    except Exception as e:
        print(f"Error in generate_routine: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/save-routine-to-db', methods=['POST'])
@login_required
def save_routine_to_db():
    """
    Save routine to database
    """
    try:
        data = request.json
        user_id = current_user.id
        
        # Extract preferences from the data structure
        preferences = data.get('preferences', {})
        
        routine = Routine(
            user_id=user_id,
            title=preferences.get('goals', 'My Study Routine') or 'My Study Routine',
            wake_up_time=preferences.get('wakeUpTime'),
            sleep_time=preferences.get('sleepTime'),
            study_duration=preferences.get('studyDuration'),
            break_duration=preferences.get('breakDuration'),
            exercise_duration=preferences.get('exerciseDuration'),
            subjects=json.dumps(preferences.get('subjects', [])),
            environment=preferences.get('environment'),
            preferences=json.dumps(preferences.get('preferences', [])),
            goals=preferences.get('goals'),
            challenges=preferences.get('challenges'),
            routine_schedule=json.dumps(data.get('schedule', []))
        )
        
        db.session.add(routine)
        db.session.commit()
        
        # Create activity record
        activity = Activity(
            user_id=user_id,
            activity_type='routine',
            routine_id=routine.id,
            title='Study Routine Created',
            description=f"Subjects: {', '.join(preferences.get('subjects', []))}"
        )
        
        db.session.add(activity)
        db.session.commit()
        
        new_badges = check_and_award_badges(current_user)
        
        return jsonify({"success": True, "message": "Routine saved successfully", "routine_id": routine.id, "new_badges": new_badges})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error saving routine: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# get all activities for user
@app.route('/get-activities', methods=['GET'])
@login_required
def get_activities():
    try:
        user_id = current_user.id
        
        activities = Activity.query.filter_by(user_id=user_id).order_by(Activity.created_at.desc()).all()
        
        return jsonify({
            "success": True,
            "activities": [activity.to_dict() for activity in activities]
        })
        
    except Exception as e:
        print(f"Error retrieving activities: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# get user stats
@app.route('/get-user-stats', methods=['GET'])
@login_required
def get_user_stats():
    try:
        user_id = current_user.id

        stats = compute_user_stats(user_id)

        return jsonify({
            "success": True,
            "stats": stats
        })

    except Exception as e:
        print(f"Error retrieving stats: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500




# ====================== AUTHENTICATION ROUTES ======================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user, remember=True)
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ====================== PROTECTED ROUTES ======================

@app.route('/about-us')
@login_required
def about_us():
    return render_template('about-us.html')

@app.route('/activity-log')
@login_required
def activity_log():
    return render_template('activity-log.html')


# Leaderboard page
@app.route('/leaderboard')
@login_required
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/api/weekly-preview')
@login_required
def weekly_preview():
    # get latest routine for this user
    routine = (
        Routine.query.filter_by(user_id=current_user.id)
        .order_by(Routine.created_at.desc())
        .first()
    )
    if not routine:
        return jsonify({
            "success": True,
            "has_routine": False
        })

    data = routine.to_dict()
    return jsonify({
        "success": True,
        "has_routine": True,
        "study_duration": data.get("study_duration") or 50,
        "break_duration": data.get("break_duration") or 10,
        "exercise_duration": data.get("exercise_duration") or 5,
        "title": data.get("title") or "My Weekly Plan"
    })

# Leaderboard API
@app.route('/api/leaderboard', methods=['GET'])
def api_leaderboard():
    try:
        users = User.query.all()
        leaderboard = []

        for user in users:
            # Sum of quiz scores (use 0 when null)
            total_quiz_score = db.session.query(db.func.coalesce(db.func.sum(Quiz.score), 0)).filter(Quiz.user_id == user.id).scalar() or 0
            quizzes_count = Quiz.query.filter_by(user_id=user.id).count()
            routines_count = Routine.query.filter_by(user_id=user.id).count()
            activities_count = Activity.query.filter_by(user_id=user.id).count()

            # Simple scoring formula: quiz points + routines*10 + activities*2
            score = int(total_quiz_score) + (routines_count * 10) + (activities_count * 2)

            leaderboard.append({
                'user_id': user.id,
                'username': user.username,
                'score': score,
                'quizzes': quizzes_count,
                'routines': routines_count,
                'activities': activities_count
            })

        leaderboard_sorted = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:20]

        return jsonify({'success': True, 'leaderboard': leaderboard_sorted})
    except Exception as e:
        print(f"Error generating leaderboard: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ====================== DEBUG ENDPOINTS ======================

@app.route('/debug')
def debug():
    return render_template('debug.html')

@app.route('/api/debug/all-data', methods=['GET'])
def debug_all_data():
    try:
        users = User.query.all()
        quizzes = Quiz.query.all()
        routines = Routine.query.all()
        activities = Activity.query.all()
        
        return jsonify({
            "users": [u.to_dict() for u in users],
            "quizzes": [q.to_dict() for q in quizzes],
            "routines": [r.to_dict() for r in routines],
            "activities": [a.to_dict() for a in activities]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/debug/user-badges/<string:username>', methods=['GET'])
def debug_user_badges(username):
    """Debug endpoint: return user stats, existing badges, and awarded badges."""
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        stats = compute_user_stats(user.id)
        owned = UserBadge.query.filter_by(user_id=user.id).all()
        owned_badge_ids = [ub.badge_id for ub in owned]
        owned_badge_objs = [Badge.query.get(bid).to_dict() for bid in owned_badge_ids if Badge.query.get(bid)]

        # Show all badges in DB too
        all_badges = [b.to_dict() for b in Badge.query.all()]

        return jsonify({
            "success": True,
            "user": user.to_dict(),
            "stats": stats,
            "owned_badge_ids": owned_badge_ids,
            "owned_badges": owned_badge_objs,
            "all_badges": all_badges
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/admin/award-badges/<string:username>', methods=['POST'])
def admin_award_badges(username):
    """Force-run badge awarding for a specific user (debug/admin use)."""
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        badges_awarded = check_and_award_badges(user)
        return jsonify({"success": True, "awarded": badges_awarded})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/admin/award-badges-all', methods=['POST'])
def admin_award_badges_all():
    """Force-run badge awarding for all users and return summary."""
    try:
        users = User.query.all()
        total_awarded = 0
        details = {}

        for user in users:
            awarded = check_and_award_badges(user)
            if awarded:
                details[user.username] = awarded
                total_awarded += len(awarded)

        return jsonify({"success": True, "total_awarded": total_awarded, "details": details})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/debug/clear-all', methods=['POST'])
def debug_clear_all():
    try:
        # Delete all records
        Activity.query.delete()
        Quiz.query.delete()
        Routine.query.delete()
        User.query.delete()
        
        db.session.commit()
        
        return jsonify({"success": True, "message": "✅ All database data cleared!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": True, "error": str(e)}), 500


# ====================== INITIALIZE BADGES FOR ALL USERS ======================
def initialize_badges():
    """Initialize badges from BADGE_MILESTONES and award to all existing users."""
    with app.app_context():
        db.create_all()
        
        # Initialize badges from BADGE_MILESTONES dictionary
        if Badge.query.count() == 0:
            badges_to_create = []
            for criteria_key, milestone_data in BADGE_MILESTONES.items():
                badge = Badge(
                    name=milestone_data["badge_name"],
                    description=milestone_data["description"],
                    criteria_key=criteria_key,
                    icon=f"{criteria_key}.png"
                )
                badges_to_create.append(badge)
            
            db.session.add_all(badges_to_create)
            db.session.commit()
            print(f"🎉 Created {len(badges_to_create)} badges from BADGE_MILESTONES!")
        
        # Award badges to all existing users based on their current stats
        all_users = User.query.all()
        total_badges_awarded = 0
        
        for user in all_users:
            badges_awarded = check_and_award_badges(user)
            if badges_awarded:
                total_badges_awarded += len(badges_awarded)
                print(f"✅ {user.username} earned: {', '.join(badges_awarded)}")
        
        if total_badges_awarded > 0:
            print(f"🏆 Total badges awarded to existing users: {total_badges_awarded}")
        else:
            print("ℹ️ No new badges awarded to existing users.")


if __name__ == '__main__':
    # Initialize badges before running the app
    initialize_badges()
    app.run(host='0.0.0.0', port=5000, debug=True)