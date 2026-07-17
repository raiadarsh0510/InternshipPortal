# 🚀 InternshipPortal - Quick Start Guide

## New Features Summary

### ✅ Completed Features

1. **Email Verification System** 📧
   - All new users must verify their email before login
   - Verification links sent automatically after registration
   - Secure token-based system with 24-hour expiration

2. **AI Assistant Chatbot** 🤖
   - Powered by OpenAI GPT-3.5-turbo
   - Available to students from navbar: "AI Assistant"
   - Quick prompt templates for:
     - Resume tips
     - Tech skills
     - Interview preparation
     - Question suggestions
   - Chat history saved automatically

3. **AI Admin Panel** 📊
   - Available to companies: "AI Admin" in navbar
   - View student chat statistics
   - Monitor common query topics
   - Track engagement metrics

4. **Enhanced UI/UX** 🎨
   - Modern login page with gradient design
   - Improved registration flow
   - Better visual hierarchy
   - Responsive design for all devices
   - Professional color scheme

## 🔧 Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
Create `.env` file in project root:

```env
# Database
DATABASE_URL=sqlite:///internship_portal.db

# Email Configuration (Gmail Example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=noreply@internshipportal.local

# OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key

# Flask
SECRET_KEY=your-secret-key-here
```

### Step 3: Initialize Database
```bash
python -c "from wsgi import app, db; app.app_context().push(); db.create_all()"
```

### Step 4: Run Application
```bash
python run.py
```

Visit: `http://localhost:5000`

## 📖 User Workflows

### Student Registration & Login
```
1. Click "Register"
2. Fill form (name, email, password, role)
3. Password requirements are displayed
4. Submit → Email verification link sent
5. Check email and verify account
6. Login with credentials
7. Access internships and AI assistant
```

### Using AI Assistant
```
1. Logged in as student
2. Click "AI Assistant" in navbar
3. Choose quick prompts OR type custom question
4. Get instant AI response
5. Chat history saved automatically
```

### Company Admin Features
```
1. Login as company
2. Click "AI Admin" in navbar
3. View chat statistics
4. See recent student queries
5. Analyze trending topics
6. Use insights for recruitment
```

## 🔐 Security & Configuration

### Email Configuration Tips

**Gmail:**
1. Enable 2-factor authentication
2. Generate app-specific password
3. Use app password in MAIL_PASSWORD

**Other Providers:**
- Outlook/Office 365: smtp-mail.outlook.com:587
- SendGrid: smtp.sendgrid.net:587
- AWS SES: email-smtp.[region].amazonaws.com:587

### OpenAI Configuration

1. Get API key from https://platform.openai.com/api-keys
2. Ensure account has credits
3. Set usage limits in OpenAI dashboard
4. Monitor API costs in platform settings

## 📊 Database Schema

### New Tables
- `chat_messages`: Stores all AI conversations
  - user_id: Student who initiated chat
  - sender: "user" or "ai"
  - content: Message text
  - created_at: Timestamp

### Updated Tables
- `users`: Added email_verified field

## 🧪 Testing Setup

### Verify Installation
```bash
# Test imports
python -c "from wsgi import app; print('✓ App loaded')"

# Test database
python -c "from wsgi import app, db; app.app_context().push(); db.create_all(); print('✓ DB ready')"

# Test AI module
python -c "from app.routes.ai import init_ai_routes; print('✓ AI module ready')"

# Test email module
python -c "from app.utils import send_verification_email; print('✓ Email module ready')"
```

## 🎯 Features by User Role

### Student Features
- ✅ Email verification for security
- ✅ AI Assistant for career guidance
- ✅ Chat history with AI
- ✅ Browse internships
- ✅ Apply for internships
- ✅ Save internships
- ✅ View applications

### Company Features
- ✅ Email verification for security
- ✅ Post internships
- ✅ View applicants
- ✅ Accept/Reject applications
- ✅ AI Admin dashboard
- ✅ View student queries

## 📱 API Endpoints

### New Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET/POST | /ai_assistant | Student chat interface |
| GET | /ai_admin | Company analytics dashboard |
| GET | /verify_email/<token> | Email verification |

### AI Features
- Built-in error handling for missing API key
- Graceful fallback messages
- Configurable response parameters

## ⚠️ Important Notes

1. **Email Verification Required**: All new accounts must verify email before login
2. **AI Requires API Key**: Without OPENAI_API_KEY, AI assistant will show unavailable message
3. **Chat History**: All conversations stored in database (no external API calls to history)
4. **Token Expiration**: Email verification tokens expire after 24 hours
5. **Email Configuration Optional**: App works without email, but verification disabled

## 🐛 Troubleshooting

### Email not sending?
```
✗ Check MAIL_SERVER and MAIL_USERNAME
✗ Verify MAIL_PASSWORD is correct
✗ For Gmail, use app-specific password (not regular password)
✗ Ensure MAIL_PORT=587 and MAIL_USE_TLS=true
```

### AI Assistant not responding?
```
✗ Verify OPENAI_API_KEY is set
✗ Check OpenAI account has credits
✗ Monitor API usage and rate limits
✗ Check Flask logs for specific errors
```

### Registration failing?
```
✗ Verify password meets all requirements (8+ chars, uppercase, lowercase, digit, special char)
✗ Check email format is valid
✗ Ensure email not already registered
✗ Check database connection
```

## 📚 Documentation Files

- `README.md` - Project overview
- `FEATURES.md` - Detailed feature documentation
- `config.py` - Configuration reference
- `app/utils.py` - Email/token utilities
- `app/routes/ai.py` - AI implementation
- `templates/ai_assistant.html` - Student chat interface

## 🚀 Performance Tips

1. Cache OpenAI responses for common questions
2. Limit chat history queries with pagination
3. Use database indexes on user_id and created_at
4. Monitor email sending queue
5. Set OpenAI model parameters based on needs:
   - temperature: 0.7 (current) - increase for creativity
   - max_tokens: 350 (current) - reduce for faster responses

## 📞 Support

For issues or questions:
1. Check logs: `instance/` or Flask debug output
2. Review FEATURES.md documentation
3. Verify all config variables are set
4. Test individual components with provided test commands

---

**Status**: ✅ Production Ready  
**Version**: 2.1.0  
**Last Updated**: 2026-07-17
