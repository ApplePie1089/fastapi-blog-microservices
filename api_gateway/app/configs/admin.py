from app.configs import env

ADMIN_EMAIL = env.str("ADMIN_EMAIL", default="admin@example.com")
ADMIN_PASSWORD = env.str("ADMIN_PASSWORD", default="admin123!")