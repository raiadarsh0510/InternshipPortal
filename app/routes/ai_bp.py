import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.ai import ResumeAnalysis, MockInterviewSession, SkillGapReport, ChatMessage
from app.services import ai_service

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")

@ai_bp.route("/")
@ai_bp.route("/hub")
def hub():
    return render_template("ai/hub.html")

@ai_bp.route("/resume-analyzer", methods=["GET", "POST"])
@login_required
def resume_analyzer():
    result = None
    if request.method == "POST":
        resume_text = request.form.get("resume_text", "").strip()
        target_role = request.form.get("target_role", "Software Engineer").strip()

        if not resume_text or len(resume_text) < 50:
            flash("Please paste a comprehensive resume text with at least 50 characters.", "warning")
            return render_template("ai/resume_analyzer.html")

        result = ai_service.analyze_resume_ats(resume_text, target_role)

        # Persist analysis
        analysis = ResumeAnalysis(
            user_id=current_user.id,
            overall_score=result["ats_score"],
            ats_score=result["ats_score"],
            readability_score=result["readability_score"],
            skills_detected=json.dumps(result["found_skills"]),
            missing_critical_skills=json.dumps(result["missing_skills"]),
            suggestions=json.dumps(result["suggestions"])
        )
        db.session.add(analysis)
        db.session.commit()

        flash("Resume analysis and ATS score generated successfully!", "success")

    previous = ResumeAnalysis.query.filter_by(user_id=current_user.id).order_by(ResumeAnalysis.created_at.desc()).limit(3).all()
    return render_template("ai/resume_analyzer.html", result=result, previous=previous)

@ai_bp.route("/mock-interview", methods=["GET"])
@login_required
def mock_interview():
    role = request.args.get("role", "Software Engineer")
    int_type = request.args.get("type", "Technical")
    questions = ai_service.get_mock_interview_questions(role, int_type)
    return render_template("ai/mock_interview.html", role=role, int_type=int_type, questions=questions)

@ai_bp.route("/mock-interview/evaluate", methods=["POST"])
@login_required
def evaluate_answer():
    data = request.get_json() or {}
    question = data.get("question", "")
    answer = data.get("answer", "")
    role = data.get("role", "Software Engineer")

    eval_result = ai_service.evaluate_mock_answer(question, answer, role)
    return jsonify(eval_result)

@ai_bp.route("/skill-gap", methods=["GET", "POST"])
@login_required
def skill_gap():
    report = None
    if request.method == "POST":
        current_skills = request.form.get("current_skills", "")
        target_role = request.form.get("target_role", "Full Stack Developer")

        report = ai_service.generate_skill_gap(current_skills, target_role)

        db_report = SkillGapReport(
            user_id=current_user.id,
            target_role=target_role,
            current_skills=json.dumps(report["current_skills"]),
            required_skills=json.dumps(report["target_skills"]),
            missing_skills=json.dumps(report["missing_skills"]),
            learning_roadmap=json.dumps(report["roadmap"])
        )
        db.session.add(db_report)
        db.session.commit()
        flash("Skill gap analysis and personalized 4-week learning roadmap generated!", "success")

    return render_template("ai/skill_gap.html", report=report)

@ai_bp.route("/cover-letter", methods=["GET", "POST"])
@login_required
def cover_letter():
    letter = None
    if request.method == "POST":
        company = request.form.get("company_name", "")
        role = request.form.get("internship_title", "")
        skills = request.form.get("skills", "")
        desc = request.form.get("description", "")

        letter = ai_service.generate_cover_letter(
            student_name=current_user.name,
            student_skills=skills,
            company_name=company,
            internship_title=role,
            job_description=desc
        )
        flash("AI-crafted tailored cover letter ready!", "success")

    return render_template("ai/cover_letter.html", letter=letter)

@ai_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"reply": "Please enter a message."}), 400

    reply = ai_service.chat_copilot(message)
    if current_user.is_authenticated:
        db.session.add(ChatMessage(user_id=current_user.id, sender="user", content=message))
        db.session.add(ChatMessage(user_id=current_user.id, sender="ai", content=reply))
        db.session.commit()

    return jsonify({"reply": reply})