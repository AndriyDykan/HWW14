from datetime import datetime, timedelta
from typing import List

from sqlalchemy import or_, extract,and_
from sqlalchemy.orm import Session

from src.database.models import Contact,User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int,user: User , db: Session) -> List[Contact]:
    """
        Retrieves a list of contacts for a specific user with specified pagination parameters.

        :param skip: The number of contacts to skip.
        :type skip: int
        :param limit: The maximum number of contacts to return.
        :type limit: int
        :param user: The user to retrieve contacts for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: A list of contacts.
        :rtype: List[Contacts]
        """
    return db.query(Contact).filter(Contact.user_id==user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User ,db: Session) -> Contact:
    """
        Retrieves a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to retrieve.
        :type contact_id: int
        :param user: The user to retrieve the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The contact with the specified ID, or None if it does not exist.
        :rtype: Note | None
        """
    return db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id==user.id )).first()


async def create_contact(body: ContactModel, user: User , db: Session) -> Contact:
    """
       Creates a new contact for a specific user.

       :param body: The data for the contact to create.
       :type body: ContactModel
       :param user: The user to create the contact for.
       :type user: User
       :param db: The database session.
       :type db: Session
       :return: The newly created contact.
       :rtype: Contact
       """
    contact = Contact(
        name=body.name,
        email=body.email,
        phone_number=body.phone_number,
        birth_date=body.birth_date,
        additional_data=body.additional_data,
        user_id = user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel,user: User , db: Session) -> Contact | None:
    """
        Updates a single note with the specified ID for a specific user.

        :param contact_id: The ID of the note to update.
        :type contact_id: int
        :param body: The updated data for the contact.
        :type body: ContactModel
        :param user: The user to update the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The updated contact, or None if it does not exist.
        :rtype: Contact | None
        """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id==user.id)).first()
    if contact:
        contact.name = body.name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def remove_contact(contact_id: int,user: User , db: Session) -> Contact | None:
    """
        Removes a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to remove.
        :type contact_id: int
        :param user: The user to remove the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The removed contact, or None if it does not exist.
        :rtype: Contact| None
        """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id==user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str,user: User , db: Session)-> List[Contact]:
    """
           Retrieves contacts with the specified name or email for a specific user.

           :param query: The filter of the contact to retrieve.
           :type query: str
           :param user: The user to retrieve the contact for.
           :type user: User
           :param db: The database session.
           :type db: Session
           :return: a list of contacts.
           :rtype: List[Contact]
           """
    contacts = (
        db.query(Contact)
        .filter(and_(
            or_(
                Contact.name.contains(query),
                Contact.email.contains(query)
            ),Contact.user_id==user.id)
        )
        .all()
    )
    return contacts


async def get_birthdays(user: User ,db: Session) -> List[Contact]:
    """
               Retrieves contacts with the specified birthday for a specific user.

               :param user: The user to retrieve the contact for.
               :type user: User
               :param db: The database session.
               :type db: Session
               :return: a list of contacts with specified birthday.
               :rtype: List[Contact]
               """
    today = datetime.today()
    end_date = today + timedelta(days=7)
    contacts = (
        db.query(Contact)
        .filter(and_(
            ((extract('month', Contact.birth_date) == today.month) & (
                    extract('day', Contact.birth_date) >= today.day)) |
            ((extract('month', Contact.birth_date) == end_date.month) & (
                    extract('day', Contact.birth_date) <= end_date.day))
        ),Contact.user_id==user.id)
        .all()
    )
    return contacts
