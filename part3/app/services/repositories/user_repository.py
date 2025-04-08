"""User repository implementation using SQLAlchemy."""

import logging
from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

logger = logging.getLogger(__name__)

class UserRepository(SQLAlchemyRepository):
    """Repository for User entity operations."""

    def __init__(self):
        """Initialize with User model."""
        super().__init__(User)

    def get_by_email(self, email):
        """Find a user by their email address.

        Args:
            email: The email address to search for

        Returns:
            User: The user with the given email, or None if not found
        """
        logger.debug(f"Searching for user with email {email}")
        return User.query.filter_by(email=email).first()

    def get_all_admins(self):
        """Get all admin users.

        Returns:
            list: List of users with admin privileges
        """
        logger.debug("Fetching all admin users")
        return User.query.filter_by(is_admin=True).all()

    def email_exists(self, email):
        """Check if an email is already registered.

        Args:
            email: The email to check

        Returns:
            bool: True if the email exists, False otherwise
        """
        return self.get_by_email(email) is not None
