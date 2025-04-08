"""Shared services for API endpoints."""
from app.services.facade import HBnBFacade

# Create a singleton facade instance to be shared across API endpoints
facade = HBnBFacade()
