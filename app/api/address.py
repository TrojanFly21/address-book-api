from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.database import get_db
from app.schemas.address import (
    AddressCreate,
    AddressResponse,
    AddressUpdate,
    NearbyAddressResponse
)
from app.services.address_service import AddressService



# Router responsible for all address-related API endpoints.
router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"],
)


@router.post(
    "",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new address record.

    The request body is validated using the AddressCreate schema before
    delegating the business logic to the service layer.
    """
    logger.info("Received request to create address: %s", address.name)
    return AddressService.create_address(db, address)


@router.get(
    "",
    response_model=List[AddressResponse],
)
def get_all_addresses(
    db: Session = Depends(get_db),
):
    """
    Retrieve all stored addresses from the system.
    """
    logger.info("Received request to fetch all addresses")
    return AddressService.get_all_addresses(db)

@router.get(
    "/search/nearby",
    response_model=List[NearbyAddressResponse],
)
def get_nearby_addresses(
    latitude: float =Query(
    ...,
    ge=-90,
    le=90,
    description="Latitude of the search location.",
    ),
    longitude: float =  Query(
    ...,
    ge=-180,
    le=180,
    description="Longitude of the search location.",
    ),
    radius_km: float =  Query(
    ...,
    gt=0,
    description="Search radius in kilometers.",
    ),
    db: Session = Depends(get_db),
):
    """
    Search for addresses within a specified radius.

    The endpoint uses latitude and longitude as the search center and
    returns all matching addresses whose distance is less than or equal
    to the provided radius.
    """

    results = AddressService.find_nearby_addresses(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )
    
    logger.info(
    "Nearby search completed. Found %d addresses",
    len(results),
    )
    
    # Transform service output into the API response schema.
    return [
        {
            "distance_km": item["distance_km"],
            "address": item["address"],
        }
        for item in results
    ]
    
@router.get(
    "/{address_id}",
    response_model=AddressResponse,
)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a single address using its unique identifier.
    """
    logger.info("Fetching address with id=%s", address_id)
    address = AddressService.get_address(db, address_id)
    if address is None:
        logger.error("Address not found: id=%s", address_id)

    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    return address


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
)
def update_address(
    address_id: int,
    address_update: AddressUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing address identified by its ID.
    """
    logger.info("Updating address id=%s", address_id)
    
    updated = AddressService.update_address(
        db,
        address_id,
        address_update,
    )
    if updated is None:
        logger.error("Update failed. Address not found: id=%s", address_id)

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    return updated


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an address from the database.

    Returns HTTP 204 when the deletion succeeds.
    """
    logger.info("Deleting address id=%s", address_id)
    
    deleted = AddressService.delete_address(
        db,
        address_id,
    )
    
    if not deleted:
        logger.error("Delete failed. Address not found: id=%s", address_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    return None

