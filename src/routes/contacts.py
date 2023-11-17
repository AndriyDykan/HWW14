from typing import List
from fastapi_limiter.depends import RateLimiter
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.models import User
from src.database.db import get_db
from src.schemas import ContactModel,ResponseContact
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
router = APIRouter(prefix='/contacts', tags=["contacts"])



@router.get("/", response_model=List[ResponseContact], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
        Get a list of contacts for the current user with rate limiting.

        :param skip: The number of contacts to skip.
        :type skip: int
        :param limit: The maximum number of contacts to return.
        :type limit: int
        :param db: The database session.
        :type db: Session
        :param current_user: The currently authenticated user.
        :type current_user: User
        :return: List of contacts.
        :rtype: List[ResponseContact]
        """


    contacts = await repository_contacts.get_contacts(skip, limit,current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts

@router.get("/birthdays", response_model=List[ResponseContact])
async def search_birthdays(db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
        Search for upcoming birthdays among the user's contacts.

        :param db: The database session.
        :type db: Session
        :param current_user: The currently authenticated user.
        :type current_user: User
        :return: List of contacts with upcoming birthdays.
        :rtype: List[Contact]
        """
    contacts = await repository_contacts.get_birthdays(current_user,db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts

@router.get("/query/{query}", response_model=List[ResponseContact])
async def get_contacts_query(query: str, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    Search for contacts based on a query string.

    :param query: The search query.
    :type query: str
    :param db: The database session.
    :type db: Session
    :param current_user: The currently authenticated user.
    :type current_user: User
    :return: List of matching contacts.
    :rtype: List[Contact]
    """
    contacts = await repository_contacts.search_contacts(query, current_user,db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts

@router.get("/{contact_id}", response_model=ResponseContact)
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
       Get a specific contact by ID.

       :param contact_id: The ID of the contact to retrieve.
       :type contact_id: int
       :param db: The database session.
       :type db: Session
       :param current_user: The currently authenticated user.
       :type current_user: User
       :return: The requested contact.
       :rtype: List[Contact]
       """

    contact = await repository_contacts.get_contact(contact_id,current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ResponseContact,description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
        Create a new contact with rate limiting.

        :param body: The contact data to create.
        :type body: ContactModel
        :param db: The database session.
        :type db: Session
        :param current_user: The currently authenticated user.
        :type current_user: User
        :return: The created contact.
        :rtype: Contact
        """
    return await repository_contacts.create_contact(body, current_user,db)


@router.put("/{contact_id}", response_model=ResponseContact)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
        Update a specific contact by ID.

        :param body: The contact data to update.
        :type body: ContactModel
        :param contact_id: The ID of the contact to update.
        :type contact_id: int
        :param db: The database session.
        :type db: Session
        :param current_user: The currently authenticated user.
        :type current_user: User
        :return: The updated contact.
        :rtype: Contact
        """
    contact = await repository_contacts.update_contact(contact_id, body,current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ResponseContact)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
       Remove a specific contact by ID.

       :param contact_id: The ID of the contact to remove.
       :type contact_id: int
       :param db: The database session.
       :type db: Session
       :param current_user: The currently authenticated user.
       :type current_user: User
       :return: The removed contact.
       :rtype: Contact
       """
    contact = await repository_contacts.remove_contact(contact_id, current_user,db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact