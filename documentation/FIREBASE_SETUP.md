# Firebase Integration Setup Guide

## Step 1: Get Your Firebase Service Account Key

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Click the **Settings icon (⚙️)** → **Project Settings**
4. Go to the **Service Accounts** tab
5. Click **Generate New Private Key**
6. A JSON file will download - save it in your project folder

## Step 2: Add the Service Account Key to Your Project

1. Move/Copy the downloaded JSON file to your project root directory
2. **Rename it to: `firebase-service-account-key.json`**

Your project structure should look like:
```
tehelkaProject/
├── app.py
├── firebase-config.py
├── firebase-service-account-key.json  ← Add this file here
├── requirements.txt
├── static/
├── templates/
└── ...
```

## Step 3: Create Firestore Database

1. In Firebase Console → Select your project
2. Go to **Firestore Database**
3. Click **Create Database**
4. Choose **Start in production mode** (or test mode for development)
5. Select your region (closest to you)
6. Click **Create**

## Step 4: Set Firestore Security Rules (for development)

Go to **Firestore → Rules** and use these rules (for testing only):

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth.uid == userId;
    }
    match /users/{userId} {
      allow read, write: if true;  // For testing only - change this for production
    }
  }
}
```

## Step 5: Verify Installation

Run your Flask app:
```bash
python app.py
```

If successful, you should see in the terminal:
```
✅ Firebase initialized successfully!
```

## Step 6: Test Firebase Integration

1. Go to your routine page: `http://localhost:5000/routine`
2. Create a routine
3. Click "Save to Firebase"
4. Check [Firebase Console → Firestore](https://console.firebase.google.com/) → Collections
5. You should see a `users` collection with your routine data

## Database Structure

Your Firestore database will be organized like this:

```
users/
  └── {user_id}/
      ├── routines/
      │   └── current/
      │       ├── routine: [array of routine items]
      │       ├── preferences: {user preferences}
      │       ├── createdAt: timestamp
      │       └── updatedAt: timestamp
      └── quizzes/
          ├── {quiz_id_1}/
          ├── {quiz_id_2}/
          └── ...
```

## What Gets Saved

### Routines:
- Study schedule (wake/sleep times)
- Study duration, break duration, exercise time
- Subjects
- Study environment preference
- Study preferences (active recall, spaced repetition, etc.)
- Goals and challenges
- Creation timestamp

### Quizzes:
- Quiz topic
- All questions asked
- User's answers
- Score and percentage
- Completion timestamp

## Environment Variables (Optional but Recommended)

For security, you can use environment variables instead of hardcoding paths:

```python
# In firebase-config.py
import os
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate(os.getenv('FIREBASE_KEY_PATH', 'firebase-service-account-key.json'))
```

Then create a `.env` file:
```
FIREBASE_KEY_PATH=firebase-service-account-key.json
```

## Troubleshooting

**Issue**: "Firebase initialization error"
- Make sure `firebase-service-account-key.json` is in the project root
- Check that the JSON file wasn't corrupted when downloading

**Issue**: "Permission denied" when saving
- Go to Firestore Rules (in Firebase Console)
- Make sure the rules allow write access
- For testing, use the test mode rules above

**Issue**: Data not appearing in Firestore
- Check the browser console for errors
- Look at Flask terminal output for error messages
- Make sure Firestore database is created (not just project)

## Production Considerations

⚠️ **IMPORTANT**: The current setup is for development only!

For production:
1. Never commit `firebase-service-account-key.json` to Git
2. Add it to `.gitignore`: `echo firebase-service-account-key.json >> .gitignore`
3. Use proper Firestore security rules
4. Implement user authentication
5. Use environment variables for sensitive data
6. Enable authentication in Firebase Console

## Next Steps

1. Add user authentication (Google Sign-In, Email/Password)
2. Set up proper Firestore security rules
3. Create user dashboard to view saved routines/quizzes
4. Implement data analytics

## Useful Links

- [Firebase Admin SDK Python](https://firebase.google.com/docs/database/admin/start)
- [Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Security Rules](https://firebase.google.com/docs/rules)
