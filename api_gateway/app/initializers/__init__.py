import logging
from app.initializers.admin import AdminInitializer


def initialize():
    """Initialize default data on startup"""
    logging.info("Initializing admin user")
    AdminInitializer().create_admin()
    logging.info("Initialization completed")