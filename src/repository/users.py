from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def confirmed_email(email: str, db: Session) -> None:
    """
       Confirms the user's email address in the database and saves this change.

       :param email: A string representing the user's email address to be confirmed.
       :type email: str
       :param db: Session for interacting with the database.
       :type db: Session
       :return: None
       :rtype: None
       """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def get_user_by_email(email: str, db: Session) -> User:
    """
       Retrieves a user by their email address from the database.

       :param email: A string representing the email address of the user to search for.
       :type email: str
       :param db: Session for interacting with the database.
       :type db: Session
       :return: A user object.
       :rtype: User
       """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
       Creates a new user in the database based on the provided UserModel data.

       :param body: An instance of UserModel containing data for the new user.
       :type body: UserModel
       :param db: Session for interacting with the database.
       :type db: Session
       :return: The newly created user.
       :rtype: User
       """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(),avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
        Updates the refresh token for a user in the database.

        :param user: A User object for which to update the token.
        :type user: User
        :param token: A string representing the new refresh token. It can be None.
        :type token: str | None
        :param db: Session for interacting with the database.
        :type db: Session
        :return: None
        :rtype: None
        """
    user.refresh_token = token
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
       Updates the user's avatar in the database based on their email address.

       :param email: A string representing the user's email address for which to update the avatar.
       :type email: str
       :param url: A string representing the new avatar URL.
       :type url: str
       :param db: Session for interacting with the database.
       :type db: Session
       :return: The updated user object.
       :rtype: User
       """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user