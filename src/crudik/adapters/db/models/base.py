from sqlalchemy.orm import registry

mapper_registry = registry()
"""Central SQLAlchemy mapper registry instance used for mapping domain entities to database tables."""
