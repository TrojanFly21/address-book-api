from sqlalchemy.orm import Session

from app.repositories.address_repository import AddressRepository
from app.schemas.address import AddressCreate, AddressUpdate
from app.services.geo_service import GeoService
from app.core.logger import logger

class AddressService:

    @staticmethod
    def create_address(
        db: Session,
        address: AddressCreate,
    ):
        logger.info("Creating address in service layer")
        return AddressRepository.create(db, address)

    @staticmethod
    def get_address(
        db: Session,
        address_id: int,
    ):
        logger.info("Getting address id=%s", address_id)
        return AddressRepository.get_by_id(db, address_id)

    @staticmethod
    def get_all_addresses(db: Session):
        return AddressRepository.get_all(db)

    @staticmethod
    def update_address(
        db: Session,
        address_id: int,
        address_update: AddressUpdate,
    ):
        existing = AddressRepository.get_by_id(db, address_id)
        logger.info("Updating address id=%s", address_id)

        if existing is None:
            logger.error("Address id=%s not found for update", address_id)

        if existing is None:
            return None

        return AddressRepository.update(
            db,
            existing,
            address_update,
        )

    @staticmethod
    def delete_address(
        db: Session,
        address_id: int,
    ):
        existing = AddressRepository.get_by_id(db, address_id)
        logger.info("Deleting address id=%s", address_id)

        if existing is None:
            logger.error("Address id=%s not found for deletion", address_id)

        if existing is None:
            return False

        AddressRepository.delete(db, existing)
        return True

    @staticmethod
    def find_nearby_addresses(
        db: Session,
        latitude: float,
        longitude: float,
        radius_km: float,
    ):
        
        logger.info("Searching nearby addresses")
        addresses = AddressRepository.get_all(db)
        

        nearby = []

        for address in addresses:

            distance = GeoService.distance_in_km(
                latitude,
                longitude,
                address.latitude,
                address.longitude,
            )

            if distance <= radius_km:
                nearby.append(
                    {
                        "distance_km": round(distance, 2),
                        "address": address,
                    }
                )

        nearby.sort(key=lambda item: item["distance_km"])
        
        logger.info(
            "Search center=(%s,%s), radius=%s km",
            latitude,
            longitude,
            radius_km,
        )
        logger.info("Nearby search found %d matches", len(nearby))

        return nearby