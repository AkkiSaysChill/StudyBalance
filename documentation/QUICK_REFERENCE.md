# Quick Reference: Database Integration

## 🎯 What You Need to Know

### **3 Main Pages & What They Do:**

| Page | URL | What It Does |
|------|-----|-------------|
| **Quiz Generator** | `/ai-quiz` | Take quizzes, auto-saves results |
| **Routine Generator** | `/routine` | Create routines, save to database |
| **Activity Log** | `/activity-log` | View all quizzes & routines, see stats |

---

## 📊 Complete Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    USER JOURNEY                         │
└─────────────────────────────────────────────────────────┘

Visit /ai-quiz
    ↓
Take Quiz (10 questions)
    ↓
Get Score (85%)
    ↓
✅ AUTO-SAVED TO DATABASE
    ↓
Visit /activity-log
    ↓
See Quiz in Activity List + Stats Updated
    ↓
View Charts & Performance Trends
```

---

## 🗂️ Database Structure (Simple Version)

```
DATABASE: study_balance.db

QUIZZES (stores each quiz attempt)
├── Topic: "Mathematics"
├── Score: 85
├── Questions: [Q1, Q2, Q3...]
└── Timestamp: 2025-12-08 15:30

ROUTINES (stores each routine)
├── Wake Time: 07:00
├── Sleep Time: 23:00
├── Subjects: [Math, Physics, English]
├── Study Schedule: [Step 1, Step 2...]
└── Timestamp: 2025-12-08 14:00

ACTIVITIES (log of all actions)
├── Type: "quiz" or "routine"
├── Title: "Mathematics Quiz"
├── Link to Quiz/Routine
└── Timestamp
```

---

## ✨ What Auto-Saves

### **When You Complete a Quiz:**
```
✅ Topic
✅ All questions asked
✅ Your answers
✅ Your score
✅ Time taken
✅ Completion date/time
```

### **When You Create a Routine:**
```
✅ Wake & sleep times
✅ Study/break/exercise durations
✅ Subjects
✅ Environment preference
✅ Study methods chosen
✅ The generated routine steps
✅ Your goals & challenges
✅ Creation date/time
```

---

## 📈 Activity Log Shows

### **Stats Dashboard:**
- Total Activities (quizzes + routines)
- Quizzes Completed (count)
- Routines Created (count)
- Average Quiz Score
- Total Study Time

### **Charts:**
- Activity per day (bar chart)
- Quiz score trend (line chart)
- Performance metrics

### **Activity List:**
- All quizzes with scores
- All routines with subjects
- Filter by type
- Export to CSV

---

## 🚀 How to Use (3 Simple Steps)

### **Step 1: Create Data**
```
Quiz: /ai-quiz → Take test → Auto-saves
Routine: /routine → Create → Save to database
```

### **Step 2: Check Activity Log**
```
Visit: /activity-log
See: All your activities + stats
Filter: By type or date
```

### **Step 3: Analyze Performance**
```
Overview Tab: See charts & trends
Activity Log Tab: See detailed history
Performance Tab: See detailed analytics
```

---

## 💾 Files Involved

```
d:\tehelkaProject\

├── app.py (Main Flask app)
│   ├── Quiz endpoints
│   ├── Routine endpoints
│   ├── Database save endpoints
│   └── Statistics endpoints
│
├── models.py (Database structure)
│   ├── User model
│   ├── Quiz model
│   ├── Routine model
│   └── Activity model
│
├── templates/
│   ├── quiz.html (takes quiz + auto-saves)
│   ├── routine.html (creates routine + saves)
│   └── activity-log.html (displays data from DB)
│
└── study_balance.db (SQLite database file)
```

---

## 🔗 How Data Flows

```
quiz.html (Frontend)
    ↓ (user submits)
POST /save-quiz-results
    ↓
app.py saves to database
    ↓
Database updated
    ↓
activity-log.html
    ↓ (fetch data)
GET /get-activities
    ↓ (returns saved data)
Display on page
```

---

## 📱 Current User Setup

Using `user_id=1` for all operations.

When you add authentication later:
```javascript
// Change from:
fetch('/save-quiz-results?user_id=1', ...)

// To:
fetch(`/save-quiz-results?user_id=${currentUser.id}`, ...)
```

---

## ⚡ Quick Commands

### **View Database (if you have SQLite Browser):**
```bash
# Open the database file:
study_balance.db
```

### **Clear Data (delete database):**
```bash
# Delete study_balance.db
# Restart Flask
# New empty database created
```

### **Check if saving works:**
```
1. Open browser console (F12)
2. Take a quiz
3. Look for: "Quiz saved to database" in network tab
4. Check /activity-log → should see new quiz
```

---

## 🎯 Common Use Cases

### **Scenario 1: Student practicing for exam**
```
1. Takes multiple math quizzes
2. Each one saved automatically
3. Views /activity-log
4. Sees score progression
5. Exports report for teacher
```

### **Scenario 2: Creating daily routine**
```
1. Fills out routine preferences
2. AI generates routine
3. Saves to database
4. Views in Activity Log
5. Creates multiple versions, all saved
```

### **Scenario 3: Tracking progress**
```
1. Week 1: Takes 5 quizzes (average 70%)
2. Week 2: Takes 5 quizzes (average 80%)
3. Views Activity Log
4. Chart shows improvement
5. Exports data to show parents
```

---

## ✅ Verification Checklist

- [ ] Flask running (see "Database initialized" message)
- [ ] study_balance.db file exists
- [ ] Can take a quiz
- [ ] Quiz appears in Activity Log
- [ ] Can create a routine
- [ ] Routine appears in Activity Log
- [ ] Stats update correctly
- [ ] Charts display data
- [ ] Can export CSV

---

## 🆘 Quick Fixes

| Problem | Solution |
|---------|----------|
| Activity Log empty | Take a quiz first |
| Database not saving | Restart Flask server |
| Can't see database | File is at project root |
| Wrong user data | Default user_id=1, change in URLs |
| Stats showing 0 | May need to refresh Activity Log |

---

**Everything is integrated and working! Just use it!** 🚀
