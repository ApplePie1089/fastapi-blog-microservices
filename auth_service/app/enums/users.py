from enum import Enum


class UserRole(str, Enum):
    """User role enum that matches users_service"""
    USER_ROLE_USER = "USER_ROLE_USER"
    USER_ROLE_ADMIN = "USER_ROLE_ADMIN"