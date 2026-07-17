import os
from datetime import datetime

from flask import render_template, request, redirect, flash, url_for, current_app
from flask_login import login_required, current_user

from app.database import db
from app.models import ChatMessage

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None


def init_ai_routes(app):

    def generate_ai_response(prompt: str) -> str:
        system_message = (
            "You are an internship portal AI assistant. "
            "Help students prepare for applications, resumes, interviews, and answer company hiring questions. "
            "Provide concise, actionable guidance and keep the tone professional and supportive."
        )

        api_key = app.config.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

        if not api_key or openai is None:
            current_app.logger.warning("OpenAI API key missing or client not installed.")
            return (
                "AI assistant is not available right now. "
                "Please configure OPENAI_API_KEY or install the OpenAI SDK."
            )

        openai.api_key = api_key

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=350,
                temperature=0.7,
            )

            return response.choices[0].message.content.strip()

        except Exception as exc:
            current_app.logger.warning("OpenAI request failed: %s", exc)
            return (
                "AI assistant is currently unavailable. "
                "Please try again later or contact support."
            )

    @app.route("/ai_assistant", methods=["GET", "POST"])
    @login_required
    def ai_assistant():

        if request.method == "POST":
            prompt = request.form.get("prompt", "").strip()

            if not prompt:
                flash("Please enter a message for the AI assistant.", "warning")
                return redirect(url_for("ai_assistant"))

            user_message = ChatMessage(
                user_id=current_user.id,
                sender="user",
                content=prompt,
                created_at=datetime.utcnow()
            )

            db.session.add(user_message)
            db.session.commit()

            ai_text = generate_ai_response(prompt)

            ai_message = ChatMessage(
                user_id=current_user.id,
                sender="ai",
                content=ai_text,
                created_at=datetime.utcnow()
            )

            db.session.add(ai_message)
            db.session.commit()

            return redirect(url_for("ai_assistant"))

        messages = ChatMessage.query.filter_by(
            user_id=current_user.id
        ).order_by(ChatMessage.created_at).all()

        return render_template(
            "ai_assistant.html",
            messages=messages,
            openai_enabled=(openai is not None and bool(app.config.get("OPENAI_API_KEY")))
        )

    @app.route("/ai_admin")
    @login_required
    def ai_admin():

        if current_user.role.lower() != "company":
            flash("AI admin page is available to company users only.", "danger")
            return redirect(url_for("dashboard"))

        chat_history = ChatMessage.query.join(
            ChatMessage.user
        ).order_by(ChatMessage.created_at.desc()).limit(200).all()

        return render_template(
            "ai_admin.html",
            chat_history=chat_history
        )

    app.logger.debug("✅ AI routes registered successfully")
