from sqlalchemy.orm import Session
from app.models import models
from app.schemas import owner

from datetime import datetime
import requests


def get_all_owners(db: Session):
    return db.query(models.Owner).all()


def get_owner_by_username(db: Session, username: str):
    return db.query(models.Owner).filter(models.Owner.username == username).first()


def get_owner_by_id(db: Session, id: int):
    return db.query(models.Owner).filter(models.Owner.id == id).first()


def get_owner_by_email(db: Session, email: str):
    return db.query(models.Owner).filter(models.Owner.email == email).first()


def get_owner_pets(db: Session, id: int):
    return (db.query(models.Owner).filter(models.Owner.id == id).first()).pets


def insert_owner(db: Session, owner: owner.Owner):
    db_owner = models.Owner(**owner.dict())

    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    message = f'{owner.username} was successfully added'
    return {'message': message, 'data': db_owner}


def update_owner(db: Session, owner: owner.OwnerOut, id: int):
    update_owner = db.query(models.Owner).filter(
        models.Owner.id == id).first()
    if (update_owner):
        update_owner.name = owner.name
        update_owner.surname = owner.surname
        update_owner.username = owner.username
        update_owner.email = owner.email
        update_owner.password = owner.password
        db.commit()

        message = f'Owner with id {id} and named {update_owner.name} was successfully updated'
        return {'message': message}

    return None


def delete_owner_by_id(db: Session, id: int):
    owner_deleted = db.query(models.Owner).filter(
        models.Owner.id == id).delete()
    if (owner_deleted != 0):
        db.commit()
        message = f'owner with id {id} and his dogs were successfully deleted'
        return {'message': message}
    message = f'owner with id {id} not found'
    return {'message': message}


def delete_owner_by_username(db: Session, username: int):
    owner_deleted = db.query(models.Owner).filter(
        models.Owner.username == username).delete()
    if (owner_deleted != 0):
        db.commit()
        message = f'owner with username {username} and his dogs were successfully deleted'
        return {'message': message}
    message = f'owner with username {username} not found'
    return {'message': message}


def delete_all_owners(db: Session):
    db.query(models.Owner).delete()
    db.commit()
    message = 'All owners and dogs deleted successfully'
    return {'message': message}


def reset_index(db: Session):
    db.execute('ALTER SEQUENCE owners_id_seq RESTART;')
    db.execute("UPDATE owners SET id = DEFAULT;")
    db.commit()
    message = 'Index reset successfully'
    return {'message': message}


def test_data(db: Session):
    db_owner = models.Owner(
        name='juan',
        surname='lopez',
        username='juan123',
        password='123',
        email='juan@gmail.com'
    )
    db.add(db_owner)
    db_owner = models.Owner(
        name='lucas',
        surname='ospina',
        username='lucas23',
        password='567',
        email='lucas1@gmail.com'
    )
    db.add(db_owner)
    db_owner = models.Owner(
        name='maria',
        surname='gaviria',
        username='maria123',
        password='123',
        email='maria@gmail.com'
    )
    db.add(db_owner)
    db_owner = models.Owner(
        name='juana',
        surname='jimenez',
        username='jeana123',
        password='abc',
        email='juana@gmail.com'
    )
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    message = 'test data generated correctly'
    return {'message': message}
