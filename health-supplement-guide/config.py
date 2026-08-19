import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "health-guide-dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance", "health.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.environ.get(
        "GEMINI_API_KEY",
        "AQ.Ab8RN6I7Y0c6m70Ek17zetd5WW8B7QP__OdZURKYMV9jdl3-OQ",
    )
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
