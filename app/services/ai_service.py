import os
import re
import json
from flask import current_app

class AIService:
    @staticmethod
    def _call_llm(prompt, system_instruction=None):
        api_key = current_app.config.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                import openai
                openai.api_key = api_key
                messages = []
                if system_instruction:
                    messages.append({"role": "system", "content": system_instruction})
                messages.append({"role": "user", "content": prompt})
                res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=600,
                    temperature=0.7
                )
                return res.choices[0].message.content.strip()
            except Exception as e:
                current_app.logger.warning(f"OpenAI call failed: {e}. Falling back to internal engine.")

        return None

    @classmethod
    def analyze_resume_ats(cls, resume_text, target_role="Software Engineer"):
        resume_clean = resume_text.lower() if resume_text else ""
        
        # Core standard tech skills dictionary
        tech_keywords = {
            "python", "javascript", "react", "node", "sql", "flask", "django", "html", "css",
            "git", "docker", "aws", "c++", "java", "mongodb", "postgresql", "rest api", "linux",
            "data structures", "algorithms", "machine learning", "ai", "tailwind", "bootstrap"
        }
        
        found_skills = [k for k in tech_keywords if k in resume_clean]
        if not found_skills:
            found_skills = ["Communication", "Problem Solving", "Teamwork"]

        # Expected critical skills for target role
        role_expectations = {
            "software engineer": ["python", "javascript", "sql", "git", "data structures", "rest api"],
            "data scientist": ["python", "machine learning", "sql", "pandas", "numpy", "statistics"],
            "frontend developer": ["javascript", "react", "html", "css", "tailwind", "git"],
            "backend developer": ["python", "node", "sql", "postgresql", "docker", "rest api"]
        }
        target_clean = target_role.lower()
        critical_skills = role_expectations.get(target_clean, ["python", "sql", "git", "problem solving"])
        missing_skills = [k for k in critical_skills if k not in resume_clean]

        # Calculate scores
        keyword_density = min(len(found_skills) * 4, 40)
        has_sections = sum([1 for sec in ["education", "experience", "projects", "skills"] if sec in resume_clean])
        structure_score = has_sections * 10
        readability_score = 30 if len(resume_clean) > 200 else 15
        
        overall_ats = min(keyword_density + structure_score + readability_score, 98)
        if overall_ats < 35:
            overall_ats = 45

        suggestions = []
        if missing_skills:
            suggestions.append(f"Add critical missing skills for {target_role}: {', '.join(missing_skills).title()}.")
        if "projects" not in resume_clean:
            suggestions.append("Include a dedicated 'Projects' section highlighting real-world GitHub repositories.")
        if "metrics" not in resume_clean and "%" not in resume_clean:
            suggestions.append("Quantify your achievements using measurable metrics (e.g., 'improved performance by 30%').")
        suggestions.append("Use standard bullet points with active action verbs (Developed, Optimized, Engineered).")

        return {
            "ats_score": overall_ats,
            "readability_score": min(readability_score * 3, 95),
            "found_skills": found_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions
        }

    @classmethod
    def generate_cover_letter(cls, student_name, student_skills, company_name, internship_title, job_description=""):
        prompt = (
            f"Write an outstanding, professional cover letter for {student_name} applying for the "
            f"'{internship_title}' position at '{company_name}'. "
            f"Applicant skills: {student_skills}. Job description: {job_description}."
        )
        llm_response = cls._call_llm(prompt, "You are an elite career advisor crafting tailored cover letters.")
        if llm_response:
            return llm_response

        # Fallback professional generator
        return f"""Dear Hiring Manager at {company_name},

I am writing to express my enthusiastic interest in the {internship_title} role at {company_name}. As a motivated professional with strong foundations in {student_skills}, I have followed {company_name}'s innovation with immense admiration and would welcome the opportunity to contribute to your team.

Throughout my academic and project journey, I have focused on solving real-world challenges through hands-on development and collaborative problem solving. Working with {student_skills}, I have engineered functional projects, optimized technical performance, and delivered reliable outcomes. I am particularly excited about this internship because it directly aligns with my goal of delivering high-quality, impactful software solutions.

I welcome the opportunity to discuss how my background and enthusiasm can support {company_name}'s upcoming initiatives. Thank you for your time and consideration.

Warm regards,
{student_name}"""

    @classmethod
    def generate_skill_gap(cls, current_skills_str, target_role):
        user_skills = [s.strip().lower() for s in current_skills_str.split(",") if s.strip()]
        role_benchmarks = {
            "Full Stack Developer": ["python", "javascript", "react", "sql", "docker", "rest api", "git"],
            "Data Analyst": ["sql", "python", "excel", "power bi", "tableau", "statistics"],
            "AI/ML Engineer": ["python", "machine learning", "deep learning", "pytorch", "tensorflow", "math"],
            "DevOps Engineer": ["linux", "docker", "kubernetes", "aws", "ci/cd", "terraform", "bash"]
        }
        benchmark = role_benchmarks.get(target_role, ["python", "javascript", "sql", "git", "rest api"])
        missing = [b for b in benchmark if b not in user_skills]

        roadmap = [
            {"week": "Week 1", "focus": "Foundations & Core Syntax", "topics": [f"Master fundamentals of {missing[0] if missing else 'Advanced Architecture'}."]},
            {"week": "Week 2", "focus": "Practical Application & Tooling", "topics": [f"Build functional components using {missing[1] if len(missing)>1 else 'Testing & Automation'}."]},
            {"week": "Week 3", "focus": "System Integration & APIs", "topics": ["Deploy a full-stack proof-of-work project to GitHub."]},
            {"week": "Week 4", "focus": "Mock Interviews & Production Readiness", "topics": ["Complete algorithmic challenges and deploy live on cloud."]}
        ]

        return {
            "current_skills": user_skills,
            "target_skills": benchmark,
            "missing_skills": missing,
            "roadmap": roadmap
        }

    @classmethod
    def get_mock_interview_questions(cls, role="Full Stack Developer", interview_type="Technical"):
        questions_db = {
            "technical": [
                "Can you explain the difference between synchronous and asynchronous execution in web applications?",
                "How do database indexes improve query performance, and what are their potential drawbacks?",
                "Explain the architectural trade-offs between monolithic architecture and microservices.",
                "How do you secure REST APIs against common vulnerabilities like CSRF, XSS, and SQL Injection?",
                "Walk me through a technically challenging project you built and how you debugged a critical issue."
            ],
            "hr": [
                "Tell me about yourself and what specifically attracted you to this internship.",
                "Describe a situation where you had to meet a tight deadline while managing unexpected project blockers.",
                "How do you handle constructive feedback or disagreements within a technical team?",
                "Where do you see your technical career progressing over the next 2 to 3 years?",
                "Why should our company select you over other qualified applicants?"
            ]
        }
        category = "hr" if interview_type.lower() == "hr" else "technical"
        return questions_db[category]

    @classmethod
    def evaluate_mock_answer(cls, question, answer, role="Software Engineer"):
        ans_clean = answer.strip().lower() if answer else ""
        word_count = len(ans_clean.split())
        
        if word_count < 10:
            return {
                "score": 3,
                "feedback": "Your answer is too brief. Provide a structured explanation using the STAR method (Situation, Task, Action, Result).",
                "strengths": "Direct response.",
                "improvement": "Elaborate with concrete examples and technical terminology."
            }
        
        score = 8 if word_count > 40 else 6
        return {
            "score": score,
            "feedback": "Strong answer demonstrating good conceptual understanding and structured communication.",
            "strengths": "Clear clarity, professional vocabulary, and relevant practical focus.",
            "improvement": "Connect your explanation to measurable outcomes or business impact."
        }

    @classmethod
    def chat_copilot(cls, message, history=[]):
        prompt = f"User asks: {message}\nProvide concise, encouraging, and actionable internship and career guidance."
        llm = cls._call_llm(prompt, "You are TELEPORTAL's expert AI Career Copilot.")
        if llm:
            return llm

        msg = message.lower()
        if "resume" in msg or "ats" in msg:
            return "To optimize your resume for ATS, ensure your section headings are standard (Education, Experience, Projects, Skills) and incorporate keywords directly matching the job description."
        if "stipend" in msg or "salary" in msg:
            return "On TELEPORTAL, internships with the 'Verified Stipend' badge guarantee timely payouts through verified employer credentials."
        if "interview" in msg:
            return "For interviews, practice the STAR method (Situation, Task, Action, Result). Try our AI Mock Interviewer in the AI Hub to test your responses!"
        return "I am your TELEPORTAL Career Copilot! I can help you analyze your resume, prepare for technical & HR interviews, and bridge skill gaps to secure your dream internship."

ai_service = AIService()