# 🔑 Step-by-Step Credentials Setup

## What You Need to Provide - 4 Simple Items:

### 1️⃣ **Canvas URL** ✅ 
**Your Value:** `https://umamherst.instructure.com`
- ✅ This is correct for UMass Amherst
- This is where you normally log into Canvas

---

### 2️⃣ **Canvas Username (Email)** 
**You Need:** Your UMass email address
- Example format: `yourname@umass.edu` 
- This is the email you use to log into Canvas/Moodle
- The same one you use for university login

**Where to find it:**
1. Go to https://umamherst.instructure.com
2. Look at the login page - it asks for your email
3. That's your Canvas username

---

### 3️⃣ **Canvas Password**
**You Need:** Your Canvas/University password
- This is your regular UMass IT Account password
- Same password you use for:
  - Canvas
  - Email
  - SPIRE
  - Moodle

⚠️ **Note:** If you have Multi-Factor Authentication (MFA/2FA) enabled, the browser will pop up and you'll need to approve it.

---

### 4️⃣ **OpenAI API Key**
**You Need:** An API key from OpenAI (starts with `sk-`)

**How to Get One:**

1. **Create OpenAI Account:**
   - Go to: https://platform.openai.com/signup
   - Sign up with any email (can be personal)

2. **Add Payment Method:**
   - Go to: https://platform.openai.com/account/billing
   - Add a credit/debit card
   - Set a monthly limit (suggest $10 to start)

3. **Generate API Key:**
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Name it: "Course Companion"
   - Copy the key (starts with `sk-`)
   - ⚠️ **SAVE IT** - You can't see it again!

**Cost:** About $0.01-0.05 per question (very cheap!)

---

## 📝 Creating Your Configuration File

### Step 1: Navigate to backend folder
```bash
cd /Users/rishikmuthyala/Desktop/AI\ Course\ Companion/intelligent-course-companion/backend
```

### Step 2: Create the .env file
Create a new file called `.env` (with the dot!) and add:

```env
# Canvas Configuration
CANVAS_BASE_URL="https://umamherst.instructure.com"
CANVAS_USERNAME="your_actual_email@umass.edu"
CANVAS_PASSWORD="your_actual_password"

# OpenAI Configuration  
OPENAI_API_KEY="sk-paste_your_actual_key_here"

# Keep these as default
CHROMA_PERSIST_DIRECTORY="./chroma_db"
DEBUG_MODE=true
LOG_LEVEL="INFO"
```

### Step 3: Replace with YOUR actual values:

| Item | Replace This | With Your Value |
|------|--------------|-----------------|
| CANVAS_USERNAME | `your_actual_email@umass.edu` | Your real UMass email |
| CANVAS_PASSWORD | `your_actual_password` | Your real password |
| OPENAI_API_KEY | `sk-paste_your_actual_key_here` | Your real OpenAI key |

---

## ✅ Final Checklist

Before running the app, make sure you have:

- [ ] Your UMass email address (like: `jdoe@umass.edu`)
- [ ] Your UMass password (same as Canvas/SPIRE)
- [ ] An OpenAI API key (starts with `sk-`)
- [ ] Created the `.env` file in the backend folder
- [ ] Replaced all placeholder values with real ones

---

## 🚨 Example of COMPLETE .env file:

```env
# This is what your ACTUAL .env should look like (with fake values as example)
CANVAS_BASE_URL="https://umamherst.instructure.com"
CANVAS_USERNAME="johndoe@umass.edu"
CANVAS_PASSWORD="MySecureP@ssw0rd123"
OPENAI_API_KEY="sk-proj-a7B9cD3fGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIjKlMnOpQrStUvWxYz"
CHROMA_PERSIST_DIRECTORY="./chroma_db"
DEBUG_MODE=true
LOG_LEVEL="INFO"
```

---

## 🔒 Security Reminder

- **NEVER** share your `.env` file with anyone
- **NEVER** commit it to GitHub
- **NEVER** post your API keys online
- The `.gitignore` already protects this file

---

## 📞 Quick Test

After creating your `.env` file, test it:

```bash
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Canvas URL:', os.getenv('CANVAS_BASE_URL')); print('Username:', os.getenv('CANVAS_USERNAME')[:3] + '***' if os.getenv('CANVAS_USERNAME') else 'NOT SET'); print('OpenAI Key:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
```

You should see:
```
Canvas URL: https://umamherst.instructure.com
Username: joh***  (first 3 letters of your email)
OpenAI Key: SET
```

If you see "NOT SET" for any value, check your `.env` file!
