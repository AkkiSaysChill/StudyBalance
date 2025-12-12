# How to Use Quiz & Routine Generator with Database

## 🔄 How It All Works Together

### **Workflow:**

```
1. Quiz/Routine Generator
   ↓
2. User submits quiz/creates routine
   ↓
3. Automatically saved to SQLite database
   ↓
4. Activity Log displays all activities
   ↓
5. Analytics show performance trends
```

---

## 📝 **Quiz Generator Integration**

### **What Happens When You Complete a Quiz:**

1. **User takes quiz** on `/ai-quiz` page
2. **Submits answers** and gets score
3. **Automatically saved to database:**
   - Quiz topic
   - Questions asked
   - User's answers
   - Score and percentage
   - Completion time
4. **Activity is logged** in activities table

### **Database Fields Saved:**
```
quizzes table:
- topic: "Mathematics"
- num_questions: 10
- score: 85
- percentage: 85.0
- questions: JSON array
- user_answers: JSON of answers
- completed_at: timestamp
```

### **How It's Used:**
- Activity log shows all past quizzes
- Performance charts display score trends
- Stats show highest score and average

---

## 📅 **Routine Generator Integration**

### **What Happens When You Create a Routine:**

1. **User fills out preferences** on `/routine` page
2. **AI generates routine** based on their inputs
3. **User clicks "Save to Database"**
4. **Automatically saved to database:**
   - Wake time and sleep time
   - Study/break/exercise durations
   - Subjects
   - Study environment preference
   - Goals and challenges
   - The generated routine schedule
5. **Activity is logged**

### **Database Fields Saved:**
```
routines table:
- title: "My Study Routine"
- wake_up_time: "07:00"
- sleep_time: "23:00"
- study_duration: 45 (minutes)
- break_duration: 15 (minutes)
- exercise_duration: 30 (minutes)
- subjects: JSON ["Math", "Physics"]
- environment: "quiet"
- preferences: JSON of study methods
- goals: User's goals
- challenges: Distractions they face
- routine_schedule: JSON of generated routine
```

---

## 📊 **Activity Log & Analytics**

### **What Gets Displayed:**

#### **1. Stats Dashboard (Top of page)**
```
Total Activities: Count of all quizzes + routines
Quizzes Completed: Number of quizzes done
Routines Created: Number of routines made
Study Time: Calculated from activities
```

#### **2. Three Main Tabs:**

**📈 Overview Tab:**
- Charts showing activity per day
- Quiz performance trend line
- Performance metrics (highest score, average, consistency)

**📋 Activity Log Tab:**
- Complete history of all activities
- Filter by quiz/routine or time period
- Details for each activity

**🎯 Performance Tab:**
- Detailed performance analytics
- Score trends
- Best performing topics

---

## 🚀 **How to Use It - Step by Step**

### **Step 1: Take a Quiz**
```
1. Go to http://localhost:5000/ai-quiz
2. Enter topic (e.g., "Mathematics")
3. Select number of questions
4. Click "Start Quiz"
5. Answer all questions
6. Click "Submit Quiz"
7. ✅ Automatically saved to database
```

### **Step 2: Create a Routine**
```
1. Go to http://localhost:5000/routine
2. Fill in all preferences:
   - Wake/sleep times
   - Study durations
   - Subjects
   - Study style
   - Goals
3. Click "Generate My Routine"
4. Review generated routine
5. Click "💾 Save to Database"
6. ✅ Saved to database
```

### **Step 3: View Activity Log & Analytics**
```
1. Go to http://localhost:5000/activity-log
2. See all your quizzes and routines
3. Check stats at the top
4. Switch between tabs:
   - Overview: Charts and trends
   - Activity Log: Detailed history
   - Performance: Detailed analytics
5. Filter by type or time period
6. Export report as CSV
```

---

## 💾 **What's Stored in Database**

### **Database Structure:**

```
study_balance.db (SQLite file)
├── users table
│   ├── id
│   ├── username
│   ├── email
│   └── created_at
│
├── quizzes table
│   ├── id
│   ├── user_id (foreign key)
│   ├── topic
│   ├── score
│   ├── total_questions
│   ├── percentage
│   ├── questions (JSON)
│   ├── user_answers (JSON)
│   └── completed_at
│
├── routines table
│   ├── id
│   ├── user_id (foreign key)
│   ├── title
│   ├── wake_up_time
│   ├── sleep_time
│   ├── study_duration
│   ├── subjects (JSON)
│   ├── environment
│   ├── routine_schedule (JSON)
│   └── created_at
│
└── activities table
    ├── id
    ├── user_id (foreign key)
    ├── activity_type ('quiz' or 'routine')
    ├── quiz_id (optional)
    ├── routine_id (optional)
    ├── title
    └── created_at
```

---

## 🔗 **API Endpoints for Database**

### **Quiz Endpoints:**
```
POST /save-quiz-results?user_id=1
- Saves quiz completion
- Payload: topic, score, questions, answers, etc.
- Returns: success, quiz_id
```

### **Routine Endpoints:**
```
POST /save-routine-to-db?user_id=1
- Saves created routine
- Payload: routine schedule, preferences, subjects, etc.
- Returns: success, routine_id
```

### **Activity Endpoints:**
```
GET /get-activities?user_id=1
- Retrieves all activities for user
- Returns: array of activities with details

GET /get-user-stats?user_id=1
- Gets user statistics
- Returns: total_quizzes, total_routines, average_score, etc.
```

---

## 🔄 **Data Flow Example**

### **Complete User Journey:**

```
User Day 1:
1. Takes Mathematics Quiz
   → Quiz saved to database
   → Activity created (type: quiz)
   → Can see in Activity Log

2. Creates Study Routine
   → Routine saved to database
   → Activity created (type: routine)
   → Can see in Activity Log

User Day 2:
1. Takes Physics Quiz
   → Saved to database
   → Performance chart updates

2. Views Activity Log
   → Shows both quizzes and routine
   → Stats show: 2 quizzes, 1 routine
   → Performance tab shows quiz trends

3. Creates another Routine
   → Replaces previous routine
   → Both still in Activity Log
```

---

## 📱 **Multi-User Support (Future)**

Currently using `user_id=1` for testing. When adding authentication:

```python
# In quiz.html
fetch('/save-quiz-results?user_id=' + current_user_id, ...)

# In routine.html
fetch('/save-routine-to-db?user_id=' + current_user_id, ...)
```

---

## 🐛 **Troubleshooting**

### **Quiz not saving?**
```
1. Check browser console (F12)
2. Check Flask terminal for errors
3. Verify database file exists (study_balance.db)
4. Make sure you see "✅ Database initialized"
```

### **Activity Log shows empty?**
```
1. Make sure you completed a quiz or routine
2. Check Flask terminal for any errors
3. Verify /get-activities endpoint works
4. Try refreshing the page
```

### **Database file not created?**
```
1. Restart Flask server
2. Check terminal output for initialization
3. Verify write permissions to folder
```

---

## 🚀 **Next Steps**

1. **Add User Authentication:** Login/signup system
2. **Share Routines:** Let users share routines with others
3. **Export Routines:** PDF/calendar format
4. **Mobile App:** React Native or Flutter
5. **Real-time Sync:** Sync across devices
6. **Progress Notifications:** Reminders and achievements

---

## 📚 **Example: Complete Workflow**

### **Monday:**
- User takes 10-question Math quiz → Score: 85% → Saved to DB
- Creates routine with Math, Physics, English → Saved to DB
- Activity log shows 1 quiz, 1 routine

### **Tuesday:**
- User takes 15-question Physics quiz → Score: 92% → Saved to DB
- Activity log now shows 2 quizzes, 1 routine
- Performance chart shows upward trend (85% → 92%)

### **Wednesday:**
- Views Activity Log → Sees all activities
- Overview tab shows charts of progress
- Performance tab compares Math (85%) vs Physics (92%)
- Exports report as CSV for parents/teacher

---

## 💡 **Key Features Now Available**

✅ Automatic quiz saving  
✅ Automatic routine saving  
✅ Activity history tracking  
✅ Performance analytics  
✅ Stats dashboard  
✅ Data export to CSV  
✅ Multi-activity filtering  
✅ Real-time chart updates  
✅ Works without internet (local DB)  
✅ Easy to deploy (SQLite goes with code)

---

That's it! Your app now has a fully integrated database system! 🎉
