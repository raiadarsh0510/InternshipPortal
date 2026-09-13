from app import create_app
from werkzeug.middleware.proxy_fix import ProxyFix
import os

env = os.getenv("FLASK_ENV", "prod" if os.getenv("RENDER") or os.getenv("PORT") else "dev")
app = create_app(env)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)