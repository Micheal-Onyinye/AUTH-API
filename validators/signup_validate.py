from utils.tools import EMAIL_PATTERN, PASSWORD_LENGTH, PASSWORD_HAS_UPPERCASE, PASSWORD_HAS_LOWERCASE, PASSWORD_HAS_DIGIT, PASSWORD_HAS_SPECIAL,USERNAME_PATTERN


def validate_email(email: str) -> str | None:
    if not email:
        return "Email is required"
    if not EMAIL_PATTERN.match(email):
        return "Email format is invalid"
    return None

def validate_password(password: str) -> str | None:
    if not password:
        return "Password is required"
    if len(password) < PASSWORD_LENGTH:
        return f"Password must be at least {PASSWORD_LENGTH} characters long"
    if not PASSWORD_HAS_UPPERCASE.search(password):
        return "Password must contain at least one uppercase letter"
    if not PASSWORD_HAS_LOWERCASE.search(password):
        return "Password must contain at least one lowercase letter"
    if not PASSWORD_HAS_DIGIT.search(password):
        return "Password must contain at least one digit"
    if not PASSWORD_HAS_SPECIAL.search(password):
        return "Password must contain at least one special character"
    return None

def validate_username(username: str) -> str | None:
    if not username:
        return "Username is required"
    if not USERNAME_PATTERN.match(username):
        return "Username must be 3-30 characters long and contain only letters, numbers, and underscores"
    return None



