import logging
from .repository import Repository
from app.extensions import db

logger = logging.getLogger(__name__)

class SQLAlchemyRepository(Repository):
    """Repository implementation using SQLAlchemy"""
    # All CRUD methods already implemented

    def __init__(self, model_class):
        self.model_class = model_class
        logger.debug(f"Created SQLAlchemy repository for {model_class.__name__}")

    def add(self, obj):
        """Add an object to the database"""
        logger.debug(f"Adding object with ID {obj.id} to database")
        db.session.add(obj)
        db.session.commit()
        logger.debug(f"Successfully added object with ID {obj.id}")
        return obj

    def get(self, obj_id):
        """Get an object by ID"""
        logger.debug(f"Fetching object with ID {obj_id}")
        obj = self.model_class.query.get(obj_id)
        if obj:
            logger.debug(f"Found object with ID {obj_id}")
        else:
            logger.debug(f"No object found with ID {obj_id}")
        return obj

    def get_all(self):
        """Get all objects"""
        logger.debug(f"Fetching all {self.model_class.__name__} objects")
        return self.model_class.query.all()

    def update(self, obj_id, data):
        """Update an object"""
        logger.debug(f"Updating object with ID {obj_id}")
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            db.session.commit()
            logger.debug(f"Updated object with ID {obj_id}")
            return obj
        logger.debug(f"Failed to update: no object with ID {obj_id}")
        return None

    def delete(self, obj_id):
        """Delete an object"""
        logger.debug(f"Deleting object with ID {obj_id}")
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            logger.debug(f"Deleted object with ID {obj_id}")
            return True
        logger.debug(f"Failed to delete: no object with ID {obj_id}")
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute"""
        logger.debug(f"Searching for object with {attr_name}={attr_value}")
        try:
            obj = self.model_class.query.filter(getattr(self.model_class, attr_name) == attr_value).first()
            if obj:
                logger.debug(f"Found object with {attr_name}={attr_value}")
            else:
                logger.debug(f"No object found with {attr_name}={attr_value}")
            return obj
        except Exception as e:
            logger.error(f"Error searching by attribute: {str(e)}")
            return None
