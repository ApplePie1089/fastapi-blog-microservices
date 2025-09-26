from app.configs import env

USERS_SERVICE = {
    "host": env.str("USERS_HOST", default="localhost"),
    "port": env.str("USERS_PORT", default="57776"),
}

AUTH_SERVICE = {
    "host": env.str("AUTH_HOST", default="localhost"),
    "port": env.str("AUTH_PORT", default="57775"),
}

BLOG_SERVICE = {
    "host": env.str("BLOG_HOST", default="localhost"),
    "port": env.str("BLOG_PORT", default="57777"),
}