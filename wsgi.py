from app import create_app
import os

env = os.getenv("FLASK_ENV", "prod" if os.getenv("RENDER") or os.getenv("PORT") else "dev")
app = create_app(env)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)