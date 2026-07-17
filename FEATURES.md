# SRDT Internship Portal - Enhanced Features

## 📋 Overview

A full-stack internship portal built with Flask featuring advanced email verification, AI-powered assistant chatbot, and enhanced UI/UX.

## ✨ New Features Added

### 1. **Email Verification System** 📧
- Users must verify their email address before logging in
- Verification tokens are generated using `itsdangerous` with secure salts
- Automated email sending with token-based verification links
- Email validation using `email-validator` package
- Configurable SMTP settings for email delivery

**Key Files:**
- `app/utils.py` - Email and token utilities
- `app/routes/auth.py` - Email verification routes
- `app/models.py` - `email_verified` field added to User model

**Setup:**
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@internshipportal.local
```

### 2. **AI Assistant Chatbot** 🤖
- Real-time AI responses powered by OpenAI GPT-3.5-turbo
- Students can ask questions about internships, resumes, interviews, and skills
- Chat history is persisted in the database
- Quick prompt templates for common topics
- Admin panel for companies to view chat analytics

**Features:**
- Resume optimization tips
- Interview preparation guidance
- Tech skills recommendations
- General career advice
- Real-time message storage and retrieval

**Key Files:**
- `app/routes/ai.py` - AI routes and logic
- `app/models.py` - ChatMessage model
- `templates/ai_assistant.html` - Student chat interface
- `templates/ai_admin.html` - Admin dashboard

**Setup:**
```env
OPENAI_API_KEY=your-openai-api-key
```

### 3. **Enhanced UI/UX** 🎨
- Redesigned login page with gradient header and better styling
- Modern registration page with password requirements display
- Responsive design with Bootstrap 5
- Improved visual hierarchy and typography
- Better form controls and user feedback
- Enhanced color scheme and animations

**Updated Templates:**
- `templates/login.html` - Modern login interface
- `templates/register.html` - Enhanced registration with guidelines
- `templates/base.html` - Added AI links to navbar
- `templates/ai_assistant.html` - Beautiful chat interface
- `templates/ai_admin.html` - Admin analytics dashboard

### 4. **Generative AI Integration** 🧠
- OpenAI GPT-3.5-turbo for intelligent responses
- Context-aware system prompts for professional guidance
- Safe error handling and fallback messages
- Configurable model parameters (temperature, tokens, etc.)
- Graceful degradation if API key is missing

**Configuration:**
```python
# In config.py
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
```

## 🗄️ Database Models

### New Models:
```python
class ChatMessage(db.Model):
    id: Integer (PK)
    user_id: Integer (FK to User)
    sender: String ("user" or "ai")
    content: Text
    created_at: DateTime
```

### Updated Models:
```python
class User:
    email_verified: Boolean (default=False)
    chats: Relationship to ChatMessage
```

## 🛣️ New Routes

### Authentication:
- `GET/POST /verify_email/<token>` - Email verification endpoint

### AI Features:
- `GET/POST /ai_assistant` - Student AI chat interface
- `GET /ai_admin` - Company admin analytics dashboard

## 📦 Dependencies Added

```
email-validator==2.3.0  # Email validation
openai==0.28.1          # GPT-3.5 integration
itsdangerous==2.2.0     # Already included (token generation)
```

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file:
```env
# Database
DATABASE_URL=sqlite:///internship_portal.db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@internshipportal.local

# OpenAI API
OPENAI_API_KEY=sk-your-api-key

# Flask
SECRET_KEY=your-secret-key
```

### 3. Run Application
```bash
python run.py
```

The app will be available at `http://localhost:5000`

## 📱 User Flow

### Student Registration:
1. Fill registration form with password requirements
2. Submit registration
3. Receive verification email
4. Click verification link
5. Can now login
6. Access AI assistant for career guidance

### AI Assistant Usage:
1. Navigate to AI Assistant from navbar
2. Enter queries or select quick prompts
3. Get real-time AI responses
4. Chat history is saved automatically

### Company Admin Panel:
1. Login as company user
2. Click "AI Admin" in navbar
3. View student chat statistics
4. Monitor common query topics
5. Use insights for recruitment strategy

## 🔒 Security Features

- **Email Verification**: Prevents spam accounts
- **Token Expiration**: 24-hour token validity
- **Secure Hashing**: Password hashing with Werkzeug
- **Login Protection**: Email verification required
- **Role-Based Access**: AI admin only for companies
- **CSRF Protection**: Flask-WTF integration (if enabled)

## 🧪 Testing

Verify setup:
```bash
# Check Python syntax
python -m py_compile app/utils.py app/routes/ai.py app/models.py

# Test imports
python -c "from app import *; print('✅ All imports successful')"

# Test database
python -c "from wsgi import app; db.create_all(); print('✅ Database initialized')"
```

## 📊 File Structure

```
app/
├── models.py              # Updated with ChatMessage & email_verified
├── utils.py              # NEW: Email and token utilities
├── routes/
│   ├── auth.py          # Updated with email verification
│   ├── ai.py            # NEW: AI assistant routes
│   └── __init__.py       # Updated to include AI routes
├── database.py
└── ...

templates/
├── login.html           # Updated: Enhanced UI
├── register.html        # Updated: Enhanced UI
├── ai_assistant.html    # NEW: Student chat
├── ai_admin.html        # NEW: Admin dashboard
├── base.html            # Updated: AI navbar links
└── ...

config.py               # Updated: Email and AI config
requirements.txt        # Updated: Added dependencies
wsgi.py                 # Updated: Added ChatMessage model
```

## 🔄 Tech Stack

- **Backend**: Python 3.8+, Flask 3.1.3
- **Database**: SQLAlchemy 2.0, SQLite/MySQL
- **Authentication**: Flask-Login, Werkzeug
- **Email**: smtplib, email-validator
- **AI**: OpenAI GPT-3.5-turbo
- **Frontend**: Bootstrap 5, Jinja2
- **Security**: itsdangerous (token generation)

## 📝 Notes

- AI responses are cached in ChatMessage table for history
- Verify email link expires after 24 hours (configurable)
- OpenAI API calls have fallback error messages
- Email sending is optional (gracefully handles missing SMTP)
- Admin AI panel shows last 200 messages for performance

## 🐛 Troubleshooting

### Email not sending?
- Check MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD in config
- For Gmail, use app-specific password
- Verify MAIL_USE_TLS is true for port 587

### AI assistant not responding?
- Verify OPENAI_API_KEY is set
- Check OpenAI API quota and billing
- Review error logs: `current_app.logger`

### Email verification link not working?
- Verify token hasn't expired (24 hour default)
- Check email config allows external links
- Ensure `_external=True` in url_for()

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced AI model configuration
- [ ] Chat export/download feature
- [ ] Email template customization
- [ ] Two-factor authentication
- [ ] WebSocket real-time notifications
- [ ] Batch email verification reminders

## 👥 Author

Adarsh Rai

## 📄 License

This project is part of SRDT Internship Portal development.

---

**Version**: 2.1.0  
**Last Updated**: 2026-07-17  
**Status**: Active Development
