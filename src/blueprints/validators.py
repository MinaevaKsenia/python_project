from email_validator import validate_email, EmailNotValidError


def check_validate_email(email):
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        print(email)
        return False
    return True

def check_validate_password(password):
    if len(password) < 5 or len(password) > 100:
        return False
    return True