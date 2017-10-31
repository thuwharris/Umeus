import os

# ENCRYPTION
SECRET_KEY = os.environ['SECRET_KEY']
BCRYPT_LEVEL = 12
BCRYPT_LOG_ROUNDS = 12

# DATABASE FOR LOCAL USE
# basedir = os.path.abspath(os.path.dirname(__file__))
# basedir = os.path.join(basedir, '..')
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/database.db')

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE']

# RECAPTCHA
RECAPTCHA_PUBLIC_KEY  = os.environ['RECAPTCHA_PUBLIC']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE']

# APP CONFIGURATION
COMMENTS_PER_PAGE = 15