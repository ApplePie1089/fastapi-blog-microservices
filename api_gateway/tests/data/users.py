TEST_USERS = [
    {
        "id": 1,
        "email": "admin@example.com",
        "password": "admin123!",
        "role": "USER_ROLE_ADMIN"
    },
    {
        "id": 2,
        "email": "user@test.com",
        "password": "user123!",
        "role": "USER_ROLE_USER"
    },
    {
        "id": 3,
        "email": "moderator@test.com",
        "password": "moderator123!",
        "role": "USER_ROLE_USER"
    }
]

ADMIN_USERS = [user for user in TEST_USERS if user["role"] == "USER_ROLE_ADMIN"]

REGULAR_USERS = [user for user in TEST_USERS if user["role"] == "USER_ROLE_USER"]

DISPOSABLE_USERS = [
    {
        "id": 99,
        "email": "disposable@test.com",
        "password": "disposable123!",
        "role": "USER_ROLE_USER"
    }
]