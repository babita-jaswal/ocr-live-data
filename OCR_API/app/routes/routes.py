from flask import Blueprint
from app.routes.endpoints import main_bp

# Expose the blueprint for the Flask app to register
__all__ = ["main_bp"]
