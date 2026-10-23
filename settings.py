import os
###############################################################################
# Project-specific settings
###############################################################################

# Shows debug messages while Silence is running
DEBUG_ENABLED = False

# Database connection details
DB_CONN = {
    "host": os.environ.get("AIVEN_HOST", "localhost"),
    "port": int(os.environ.get("AIVEN_PORT", 3306)),
    "username": os.environ.get("AIVEN_USER", "root"),
    "password": os.environ.get("AIVEN_PASSWORD"),
    "database": os.environ.get("AIVEN_DATABASE", "rinconcito_db"),
}

# The sequence of SQL scripts located in the sql/ folder that must
# be ran when the 'silence createdb' command is issued
SQL_SCRIPTS = [
    "booking_calendar.sql",
]

# The port in which the API and the web server will be deployed
LISTEN_ADDRESS = "0.0.0.0"
HTTP_PORT = int(os.environ.get("PORT", 8080))

# The URL prefix for all API endpoints
API_PREFIX = "/api/v1"

# Table and fields that are used for both login and register
# Uncomment this and set up your own table and columns:

#USER_AUTH_DATA = {
#    "table": "Employees",
#    "identifier": "email",
#    "password": "password",
#}

# A random string that is used for security purposes
# (this has been generated automatically upon project creation)
SECRET_KEY = os.environ.get("SECRET_KEY", "x2Kd3wTvTrVPMzGCNz1Ph6ak8VShAEXHGTS00mU0HzF3z5Oclr6f0Emam2bgmDKf")