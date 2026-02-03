import re

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
EMAIL_PATTERN = re.compile(EMAIL_REGEX)

PASSWORD_LENGTH = 8

PASSWORD_CHARSETS={
  'uppercase': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  'lowercase': 'abcdefghijklmnopqrstuvwxyz',
  'digits': '0123456789',
  'special': '!@#$%^&*()-_=+[]{}|;:,.<>?/'
}

PASSWORD_HAS_UPPERCASE = re.compile(r'[A-Z]')
PASSWORD_HAS_LOWERCASE = re.compile(r'[a-z]')
PASSWORD_HAS_DIGIT = re.compile(r'\d')
PASSWORD_HAS_SPECIAL = re.compile(r'[!@#$%^&*()\-_=\+\[\]{}|;:,.<>?/]')

USERNAME_REGEX = r'^[a-zA-Z0-9_]{3,30}$'
USERNAME_PATTERN = re.compile(USERNAME_REGEX)