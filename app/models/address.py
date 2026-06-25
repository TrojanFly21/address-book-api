from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.core.database import Base


class Address(Base):
    """
    SQLAlchemy model representing an address record.

    Stores address details along with geographic coordinates that are
    used for nearby location searches.
    """
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    zipcode = Column(String(20), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )