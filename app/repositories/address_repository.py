from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
from app.core.logger import logger


class AddressRepository:
    """
    Repository responsible for all database operations
    related to the Address model.
    """

    @staticmethod
    def create(db: Session, address: AddressCreate) -> Address:
        db_address = Address(**address.model_dump())
        logger.info("Inserting address into database")

        db.add(db_address)
        db.commit()
        db.refresh(db_address)

        return db_address

    @staticmethod
    def get_by_id(db: Session, address_id: int) -> Optional[Address]:
        logger.info("Querying address id=%s", address_id)
        return (
            db.query(Address)
            .filter(Address.id == address_id)
            .first()
        )

    @staticmethod
    def get_all(db: Session) -> List[Address]:
        logger.info("Fetching all addresses from database")
        return (
            db.query(Address)
            .order_by(Address.id.asc())
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        db_address: Address,
        address_update: AddressUpdate,
    ) -> Address:

        update_data = address_update.model_dump()
        logger.info("Persisting updated address id=%s", db_address.id)

        for key, value in update_data.items():
            setattr(db_address, key, value)

        db.commit()
        db.refresh(db_address)

        return db_address

    @staticmethod
    def delete(db: Session, db_address: Address) -> None:
        logger.info("Deleting address id=%s from database", db_address.id)
        db.delete(db_address)
        db.commit()