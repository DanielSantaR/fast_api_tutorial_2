from sqlalchemy.orm import Session
from app.models import models
from app.schemas import pet

from datetime import datetime
import requests


def get_all_pets(db: Session):
    return db.query(models.Pet).all()


def get_pet_by_name(db: Session, pet_name: str):
    return db.query(models.Pet).filter(models.Pet.name == pet_name).all()


def get_pet_by_id(db: Session, pet_id: int):
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()


def get_adopted_pets(db: Session):
    return db.query(models.Pet).filter(models.Pet.is_adopted == True).all()


def get_pets_type(db: Session, pet_type: str):
    return db.query(models.Pet).filter(models.Pet.pet_type == pet_type).all()


def update_pet(db: Session, pet: pet.UpdatePet, pet_id: int):
    update_pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if (update_pet):
        update_pet.name = pet.name
        update_pet.update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        update_pet.breed = pet.breed
        if(pet.picture):
            update_pet.picture = get_pet_image(update_pet.pet_type.lower())
        update_pet.is_adopted = pet.is_adopted
        update_pet.age = pet.age
        update_pet.weight = pet.weight
        db.commit()

        message = f'Dog with id {pet_id} and named {update_pet.name} was successfully updated'
        return {'message': message}

    return None


def insert_pet(db: Session, pet: pet.BasePet, pet_name: str):
    standarized_type = pet.pet_type.lower()
    picture = get_pet_image(standarized_type)
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    db_pet = models.Pet(name=pet_name, picture=picture,
                        create_date=create_date, update_date=update_date, **pet.dict())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    message = f'{pet_name} was successfully added'
    return {'message': message, 'data': db_pet}


def delete_pet(db: Session, pet_id: int):
    pet_deleted = db.query(models.Pet).filter(models.Pet.id == pet_id).delete()
    if (pet_deleted != 0):
        db.commit()
        message = f'Pet with id {pet_id} was successfully deleted'
        return {'message': message}
    message = f'Pet with id {pet_id} not found'
    return {'message': message}


def delete_all_pets(db: Session):
    db.query(models.Pet).delete()
    db.commit()
    message = 'All pets deleted successfully'
    return {'message': message}


def reset_index(db: Session):
    db.execute('ALTER SEQUENCE pets_id_seq RESTART;')
    db.execute("UPDATE pets SET id = DEFAULT;")
    db.commit()
    message = 'Index reset successfully'
    return {'message': message}


def get_pet_image(pet_type: str):
    if (pet_type == 'dog'):
        return (requests.get(
            'https://dog.ceo/api/breeds/image/random').json())['message']
    if (pet_type == 'bird'):
        return (requests.get(
            'https://some-random-api.ml/img/birb').json())['link']
    if (pet_type == 'cat'):
        return (requests.get(
            'https://api.thecatapi.com/v1/images/search').json())[0]['url']
    else:
        return None


def test_data(db: Session):
    db_pet = models.Pet(
        name='Lazy',
        pet_type='dog',
        breed='boxer',
        picture='https://images.dog.ceo/breeds/papillon/n02086910_6483.jpg',
        create_date=datetime.now().strftime('2020-05-21 10:58:55.104954'),
        update_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        is_adopted=True,
        age=10,
        weight=9.3
        #owner_id=1
    )
    db.add(db_pet)
    db_pet = models.Pet(
        name='Bruna',
        pet_type='cat',
        breed='persa',
        picture='https://cdn2.thecatapi.com/images/1ql.jpg',
        create_date=datetime.now().strftime('2020-04-21 11:45:55.104954'),
        update_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        is_adopted=False,
        age=8,
        weight=5.5
        #owner_id=1
    )
    db.add(db_pet)
    db_pet = models.Pet(
        name='Lazy',
        pet_type='fish',
        breed=None,
        picture=None,
        create_date=datetime.now().strftime('2019-11-21 11:45:55.104954'),
        update_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        is_adopted=False,
        age=7,
        weight=6.2
        #owner_id=2
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    message = 'test data generated correctly'
    return {'message': message}
