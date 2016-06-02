
# DB URI
# example DB URI:
# mysql+oursql://scott:tiger@localhost/mydatabase
# postgresql+psycopg2://scott:tiger@localhost/mydatabase
SQLALCHEMY_DATABASE_URI = 'mysql+oursql://<userid>:<password>@<servername>/<db_name>'
# example
#SQLALCHEMY_DATABASE_URI = 'mysql+oursql://root:mysql@localhost/userdirectory'

# Debug from SQLAlchemy
# Turn this to False on production
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

# List of allowed origins for CORS
ALLOWED_ORIGINS = "['*']"

# List of allowed IPs
WHITELIST_IPS = ["127.0.0.1"]

# Configure your log paths
LOG_FILE_DIRECTORY = 'logs'
LOG_FILE = 'user-directory.log'

# Log level for the application
#10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR, 50=CRITICAL",
LOG_LEVEL = 10

# APP_URL
APP_URL = "http://localhost:5000"

# Persona Verifier URL
PERSONA_VERIFIER_URL = "https://verifier.login.persona.org/verify"
