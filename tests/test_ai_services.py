from app.services.ai_service import ai_service

def test_resume_ats_analysis(app):
    with app.app_context():
        sample_resume = """
        John Doe
        Email: john@example.com
        Education: B.Tech in Computer Science
        Experience: Intern at Tech Corp working on Python, Flask, Docker, and PostgreSQL.
        Projects: Built high throughput REST API with JWT authentication. Optimized query performance by 40%.
        Skills: Python, Flask, SQL, Docker, Git, REST API, Linux
        """
        result = ai_service.analyze_resume_ats(sample_resume, target_role="Software Engineer")
        assert "ats_score" in result
        assert result["ats_score"] >= 70
        assert "python" in result["found_skills"]
        assert "sql" in result["found_skills"]
        assert len(result["suggestions"]) > 0

def test_cover_letter_generation(app):
    with app.app_context():
        letter = ai_service.generate_cover_letter(
            student_name="Adarsh Rai",
            student_skills="Python, Flask, AI Agents",
            company_name="Nexus AI Innovations",
            internship_title="Generative AI Research Intern"
        )
        assert "Nexus AI Innovations" in letter
        assert "Generative AI Research Intern" in letter
        assert "Adarsh Rai" in letter
        assert "Python" in letter

def test_skill_gap_analysis(app):
    with app.app_context():
        gap = ai_service.generate_skill_gap(
            current_skills_str="Python, SQL, HTML",
            target_role="Full Stack Developer"
        )
        assert "current_skills" in gap
        assert "target_skills" in gap
        assert "missing_skills" in gap
        assert "roadmap" in gap
        assert len(gap["roadmap"]) == 4

def test_mock_interview_questions_and_evaluation(app):
    with app.app_context():
        tech_q = ai_service.get_mock_interview_questions(role="Full Stack Developer", interview_type="Technical")
        assert len(tech_q) >= 5
        assert isinstance(tech_q[0], str)

        hr_q = ai_service.get_mock_interview_questions(role="Full Stack Developer", interview_type="HR")
        assert len(hr_q) >= 5

        # Test short answer evaluation
        eval_short = ai_service.evaluate_mock_answer("Explain REST", "It is an API.")
        assert eval_short["score"] <= 4

        # Test comprehensive answer evaluation
        eval_good = ai_service.evaluate_mock_answer(
            "Explain synchronous vs asynchronous execution",
            "In synchronous programming, operations block subsequent tasks until completion. In asynchronous programming, long-running operations like database I/O or network requests run in the background using event loops or promises, preventing the main thread from freezing and drastically improving application throughput and user experience."
        )
        assert eval_good["score"] >= 7
        assert "feedback" in eval_good

def test_copilot_chat(app):
    with app.app_context():
        res1 = ai_service.chat_copilot("How do I improve my resume ATS score?")
        assert "resume" in res1.lower() or "ats" in res1.lower()

        res2 = ai_service.chat_copilot("Tell me about interview tips")
        assert "interview" in res2.lower() or "star" in res2.lower()

def test_ai_hub_page(client, student_user):
    client.post("/login", data={
        "email": student_user.email,
        "password": "StudentPass@123"
    })
    res = client.get("/ai/")
    assert res.status_code == 200
    assert b"AI Career Accelerator Hub" in res.data or b"AI Hub" in res.data