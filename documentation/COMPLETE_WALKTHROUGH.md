# Complete Walkthrough: Quiz & Routine with Database

## 🎬 Real Example: Student using the app

---

## **Day 1: Monday - First Quiz & Routine**

### **Step 1: Take a Quiz**

**URL:** `http://localhost:5000/ai-quiz`

```
Screen 1: Quiz Setup
┌─────────────────────────────────────┐
│  🎯 AI Quiz Generator              │
│                                     │
│  Topic: [Mathematics       ]       │
│  Questions: [10 Questions   ▼]     │
│                                     │
│  [Start Quiz]                      │
└─────────────────────────────────────┘

User enters: "Mathematics"
User selects: 10 questions
User clicks: "Start Quiz"
```

**What happens backend:**
```python
POST /ai-quiz
├── Generate 10 questions about Mathematics
└── Return questions to frontend
```

---

**Screen 2: Quiz Display**
```
┌─────────────────────────────────────┐
│  Question 1 of 10        Score: 0   │
│                                     │
│  What is 5 + 3?                    │
│                                     │
│  ☐ A) 7                             │
│  ☐ B) 8   ← User clicks this       │
│  ☐ C) 9                             │
│  ☐ D) 10                            │
│                                     │
│  [← Previous] [Next →]              │
└─────────────────────────────────────┘

User answers all 10 questions...
```

---

**Screen 3: Results**
```
┌─────────────────────────────────────┐
│  Quiz Complete! 🎉                 │
│                                     │
│          ┌────────┐                 │
│          │  85%   │                 │
│          │ 8.5/10 │                 │
│          └────────┘                 │
│                                     │
│  Great job! 85% is excellent!      │
│                                     │
│  [Take Another Quiz]               │
└─────────────────────────────────────┘
```

**What happens backend - AUTO-SAVE:**
```javascript
// JavaScript automatically sends:
POST /save-quiz-results?user_id=1

{
  topic: "Mathematics",
  totalQuestions: 10,
  score: 8,
  percentage: 85,
  questions: [...],
  userAnswers: {...},
  duration: 12
}

// Backend response:
{
  "success": true,
  "message": "Quiz saved successfully",
  "quiz_id": 1
}
```

**What's saved in database:**
```
quizzes table:
┌────┬────────┬──────┬────────┬──────────────┐
│ id │ user_id│topic │ score  │ percentage   │
├────┼────────┼──────┼────────┼──────────────┤
│ 1  │   1    │Math  │   8    │     85       │
└────┴────────┴──────┴────────┴──────────────┘

activities table:
┌────┬────────┬─────────┬────────┐
│ id │user_id │quiz_id  │ type   │
├────┼────────┼─────────┼────────┤
│ 1  │   1    │    1    │ quiz   │
└────┴────────┴─────────┴────────┘
```

---

### **Step 2: Create a Study Routine**

**URL:** `http://localhost:5000/routine`

**Screen: Routine Setup Form**
```
┌──────────────────────────────────────┐
│ 📅 Create Your Study Routine         │
│                                      │
│ ⏰ Your Schedule                     │
│ Wake up time: [07:00     ]          │
│ Sleep time:   [23:00     ]          │
│                                      │
│ 📚 Study & Break Duration           │
│ Study session: [▯──45 min]          │
│ Break:        [▯──15 min]           │
│ Exercise:     [▯──30 min]           │
│                                      │
│ 📖 Subjects                          │
│ [Mathematics, Physics, English   ]  │
│                                      │
│ 🎯 Your Study Style                 │
│ ☑ Active Recall                     │
│ ☑ Spaced Repetition                 │
│                                      │
│ [Generate My Routine]               │
└──────────────────────────────────────┘
```

User fills in all fields and clicks "Generate My Routine"

---

**What happens backend:**
```python
POST /generate-routine

{
  wakeUpTime: "07:00",
  sleepTime: "23:00",
  studyDuration: 45,
  breakDuration: 15,
  exerciseDuration: 30,
  subjects: ["Mathematics", "Physics", "English"],
  preferences: ["active-recall", "spaced-repetition"],
  goals: "Improve grades",
  challenges: "Procrastination"
}

↓ 

AI generates personalized routine:
[
  "7:00 AM - Wake up and breakfast",
  "7:30 AM - Morning exercise (30 min)",
  "8:00 AM - Mathematics study (45 min)",
  "8:45 AM - Break (15 min)",
  "9:00 AM - Physics study (45 min)",
  ...
]
```

---

**Screen: Generated Routine**
```
┌──────────────────────────────────────┐
│ 📅 Your Personalized Routine         │
│                                      │
│ Schedule: 07:00 - 23:00             │
│ Subjects: Math, Physics, English    │
│                                      │
│ Daily Schedule:                      │
│ ┌─────────────────────────────────┐ │
│ │ 1. 7:00 AM - Wake & breakfast   │ │
│ │ 2. 7:30 AM - Exercise (30 min)  │ │
│ │ 3. 8:00 AM - Math study (45 min)│ │
│ │ 4. 8:45 AM - Break (15 min)     │ │
│ │ 5. 9:00 AM - Physics (45 min)   │ │
│ │ ... (more steps)                │ │
│ └─────────────────────────────────┘ │
│                                      │
│ [Save to Database] [Create Another] │
└──────────────────────────────────────┘
```

User clicks "Save to Database"

---

**What happens backend - AUTO-SAVE:**
```javascript
POST /save-routine-to-db?user_id=1

{
  routine: [step1, step2, step3, ...],
  preferences: {
    wakeUpTime: "07:00",
    sleepTime: "23:00",
    studyDuration: 45,
    subjects: ["Mathematics", "Physics", "English"],
    ...
  }
}

// Backend response:
{
  "success": true,
  "message": "Routine saved successfully",
  "routine_id": 1
}
```

**What's saved in database:**
```
routines table:
┌────┬────────┬──────┬──────────┬─────────────┐
│ id │user_id │title │wake_time │sleep_time   │
├────┼────────┼──────┼──────────┼─────────────┤
│ 1  │   1    │My... │  07:00   │   23:00     │
└────┴────────┴──────┴──────────┴─────────────┘

activities table (updated):
┌────┬────────┬──────────┬──────────┐
│ id │user_id │routine_id│ type     │
├────┼────────┼──────────┼──────────┤
│ 2  │   1    │    1     │ routine  │
└────┴────────┴──────────┴──────────┘
```

---

## **Step 3: View Activity Log & Analytics**

**URL:** `http://localhost:5000/activity-log`

**Screen: Activity Log Home**
```
┌────────────────────────────────────────────┐
│ 📊 Activity Log & Analysis                 │
│                                            │
│ ┌──────────┬──────────┬──────────┬──────┐ │
│ │Total: 2  │Quizzes: 1│Routines:1│Avg:85%
│ └──────────┴──────────┴──────────┴──────┘ │
│                                            │
│ [All] [📝 Quizzes] [📅 Routines]          │
│                                            │
│ 📈 Overview | 📋 Activity Log | 🎯 Perf  │
└────────────────────────────────────────────┘
```

### **Tab 1: Overview - Charts & Trends**

```
Activity This Week:
┌────────────────────────────────┐
│ ▓ ▓ ▓ ░ ░ ░ ░                 │ (bar chart)
│ Mon Tue Wed Thu Fri Sat Sun   │
└────────────────────────────────┘
Shows: 2 activities on Monday

Quiz Performance Trend:
┌────────────────────────────────┐
│       ▲                         │ (line chart)
│      / \                        │
│     /   \──                     │
│   Quiz1  Quiz2 (if more)       │
│    85%    -                     │
└────────────────────────────────┘

Performance Metrics:
┌─────────────────────────────────┐
│ Highest Score: 85%   (Math)     │
│ Average Score: 85%   (1 quiz)   │
│ Consistency: 100%    (steady)   │
└─────────────────────────────────┘
```

---

### **Tab 2: Activity Log - Detailed History**

```
┌────────────────────────────────────────┐
│ 📝 Mathematics Quiz                    │
│ Today at 15:30                        │
│ ┌──────────────────────────────────┐  │
│ │ Topic: Mathematics               │  │
│ │ Score: 8/10 (85%)               │  │
│ │ Duration: 12 minutes            │  │
│ └──────────────────────────────────┘  │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ 📅 Study Routine Created               │
│ Today at 15:00                        │
│ ┌──────────────────────────────────┐  │
│ │ Schedule: 07:00 - 23:00          │  │
│ │ Subjects: Math, Physics, English │  │
│ │ Study: 45 min | Break: 15 min    │  │
│ └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

---

### **Tab 3: Performance - Analytics**

```
┌─────────────────────────────────────┐
│ Quizzes by Topic:                   │
│ ┌──────────────────────────────────┐│
│ │ Mathematics: 85%                 ││
│ │ (1 quiz, needs more practice)    ││
│ └──────────────────────────────────┘│
└─────────────────────────────────────┘
```

---

## **Day 2: Tuesday - Another Quiz**

### **Take Another Quiz**

User goes to `/ai-quiz` again, takes Physics quiz, gets 92%

**Automatic Updates:**
```
Database Updated:
└── quizzes table now has 2 rows:
    ├── Row 1: Math (85%)
    └── Row 2: Physics (92%)

└── activities table now has 3 entries:
    ├── Math Quiz
    ├── Routine
    └── Physics Quiz
```

---

### **Check Activity Log Again**

**Stats Updated:**
```
Total Activities: 3 (was 2)
Quizzes Completed: 2 (was 1)
Average Score: 88.5% (was 85%)
```

**Charts Update:**
```
Performance Trend Chart:
     92% ▲
       /│
      / │
    85% └─ ▲
    Math Physics
    Quiz1 Quiz2

Shows improvement from 85% to 92%!
```

---

## **Week 1 Review**

Taking multiple quizzes throughout the week:

```
Monday:   Math (85%)
Tuesday:  Physics (92%)
Wednesday: Chemistry (88%)
Thursday:  History (78%)
Friday:    Math (90%) - improvement!

Activity Log Shows:
├── Upward trend chart
├── 5 quizzes logged
├── Average: 86.6%
├── Highest: 92% (Physics)
├── Lowest: 78% (History)
└── 1 Routine: Math/Physics/Chemistry
```

---

## **Export Report**

**Click "Export Report"**

Downloads: `activity-report.csv`

```
Type,Title,Date,Details
Quiz,"Math Quiz","12/8/2025","Score: 85%, Topic: Mathematics"
Routine,"My Routine","12/8/2025","Subjects: Math; Physics; English"
Quiz,"Physics Quiz","12/9/2025","Score: 92%, Topic: Physics"
Quiz,"Chemistry Quiz","12/10/2025","Score: 88%, Topic: Chemistry"
```

Can open in Excel/Google Sheets!

---

## 🔄 **Data Flow Diagram**

```
USER INTERACTION LAYER
│
├─ /ai-quiz
│  └─ User takes quiz
│     └─ Submits answers
│        └─ Auto: POST /save-quiz-results
│           └─ ✅ Saved to quizzes table
│              └─ ✅ Created activity log entry
│
├─ /routine
│  └─ User creates routine
│     └─ Clicks save
│        └─ POST /save-routine-to-db
│           └─ ✅ Saved to routines table
│              └─ ✅ Created activity log entry
│
└─ /activity-log
   └─ Page loads
      └─ GET /get-activities?user_id=1
         └─ Retrieves all activities
            └─ GET /get-user-stats?user_id=1
               └─ Retrieves stats
                  └─ ✅ Display everything
```

---

## 📊 **Real Database Contents After Week 1**

```sql
SELECT * FROM quizzes;
┌────┬────────┬──────────┬───────┬──────────┐
│ id │ topic  │ score    │ total │ percent  │
├────┼────────┼──────────┼───────┼──────────┤
│ 1  │ Math   │ 8        │ 10    │ 85       │
│ 2  │ Physics│ 9        │ 10    │ 92       │
│ 3  │ Chem   │ 8        │ 10    │ 88       │
│ 4  │ History│ 7        │ 10    │ 78       │
│ 5  │ Math   │ 9        │ 10    │ 90       │
└────┴────────┴──────────┴───────┴──────────┘

SELECT * FROM routines;
┌────┬─────────────┬──────────┐
│ id │ title       │ subjects │
├────┼─────────────┼──────────┤
│ 1  │ My Routine  │ Math,... │
│ 2  │ New Routine │ Physics..│
└────┴─────────────┴──────────┘

SELECT * FROM activities;
┌────┬─────────────┬─────────┐
│ id │ title       │ type    │
├────┼─────────────┼─────────┤
│ 1  │ Math Quiz   │ quiz    │
│ 2  │ My Routine  │ routine │
│ 3  │ Physics...  │ quiz    │
│ 4  │ Chem Quiz   │ quiz    │
│ 5  │ History..   │ quiz    │
│ 6  │ Math Quiz   │ quiz    │
│ 7  │ New Routine │ routine │
└────┴─────────────┴─────────┘
```

---

## ✅ **Summary: What Happens Automatically**

1. **Quiz completed** → Auto-saved to DB
2. **Routine created** → Auto-saved to DB
3. **Activity logged** → Tracked in DB
4. **Stats calculated** → Aggregated from DB
5. **Charts generated** → Data from DB
6. **Report exportable** → Data from DB

**No manual database operations needed!** Everything is automatic! 🚀

---

This is how your app integrates quiz, routine, and database together!
