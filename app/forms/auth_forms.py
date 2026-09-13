from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, IntegerField, DateField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange, URL

class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")

class StudentRegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    phone = StringField("Phone Number", validators=[Optional(), Length(max=15)])
    college = StringField("College / University", validators=[Optional(), Length(max=150)])
    branch = StringField("Branch / Major", validators=[Optional(), Length(max=100)])

class CompanyRegisterForm(FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired(), Length(min=2, max=120)])
    hr_name = StringField("Contact Person Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Work Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    location = StringField("Headquarters Location", validators=[Optional(), Length(max=120)])
    website = StringField("Company Website", validators=[Optional(), Length(max=180)])

class InternshipPostForm(FlaskForm):
    title = StringField("Internship Title", validators=[DataRequired(), Length(max=150)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    internship_type = SelectField("Work Mode", choices=[("Virtual", "Remote / Virtual"), ("On-site", "In-Office / On-site"), ("Hybrid", "Hybrid")], default="Virtual")
    experience_level = SelectField("Experience Level", choices=[("Fresher", "Fresher / College Student"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")], default="Fresher")
    location = StringField("Location / City", default="Remote", validators=[DataRequired()])
    stipend_type = SelectField("Stipend Type", choices=[("Fixed", "Fixed Monthly"), ("Performance", "Performance-based"), ("Unpaid", "Unpaid")], default="Fixed")
    stipend_amount = IntegerField("Monthly Stipend (₹)", default=10000, validators=[NumberRange(min=0)])
    duration_weeks = IntegerField("Duration (Weeks)", default=8, validators=[NumberRange(min=1, max=52)])
    openings = IntegerField("Number of Openings", default=2, validators=[NumberRange(min=1)])
    skills = StringField("Required Skills (Comma separated)", validators=[DataRequired()])
    description = TextAreaField("About the Role", validators=[DataRequired(), Length(min=20)])
    responsibilities = TextAreaField("Day-to-day Responsibilities", validators=[Optional()])
    requirements = TextAreaField("Candidate Requirements", validators=[Optional()])
    benefits = TextAreaField("Perks & Benefits (Certificate, LOR, PPO)", validators=[Optional()])
    deadline = DateField("Application Deadline", format="%Y-%m-%d", validators=[DataRequired()])

class StudentProfileForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    college = StringField("College / University", validators=[Optional()])
    branch = StringField("Branch / Specialization", validators=[Optional()])
    graduation_year = StringField("Graduation Year", validators=[Optional()])
    cgpa = FloatField("CGPA / Percentage", validators=[Optional(), NumberRange(min=0, max=100)])
    skills = StringField("Skills (Comma separated)", validators=[Optional()])
    bio = TextAreaField("Professional Bio", validators=[Optional()])
    github_url = StringField("GitHub URL", validators=[Optional()])
    linkedin_url = StringField("LinkedIn URL", validators=[Optional()])
    leetcode_url = StringField("LeetCode Profile", validators=[Optional()])
    codeforces_url = StringField("Codeforces Profile", validators=[Optional()])
    portfolio_url = StringField("Personal Portfolio URL", validators=[Optional()])