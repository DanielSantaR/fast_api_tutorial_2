from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.crud import owners, pets
from app.models import models
from app.schemas import owner, pet
from db.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/all/", response_model=List[pet.Pet])
def get_all_pets(db: Session = Depends(get_db)):
    db_pets = pets.get_all_pets(db=db)
    if not db_pets:
        raise HTTPException(
            status_code=404, detail=f"No pets found"
        )
    return db_pets


@router.get("/name/{name}", response_model=List[pet.Pet])
def get_pet_by_name(name: str = Path(..., min_length=2), db: Session = Depends(get_db)):
    db_pet_name = pets.get_pet_by_name(db=db, name=name)
    if not db_pet_name:
        raise HTTPException(
            status_code=404, detail=f"Pet named {name} not found"
        )
    return db_pet_name


@router.get("/id/{id}", response_model=pet.Pet)
def get_pet_by_id(id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_pet_id = pets.get_pet_by_id(db=db, id=id)
    if db_pet_id is None:
        raise HTTPException(
            status_code=404, detail=f"Pet with id {id} not found"
        )
    return db_pet_id


@router.get("/is_adopted/", response_model=List[pet.Pet])
def get_adopted_pets(db: Session = Depends(get_db)):
    db_adopted_pet = pets.get_adopted_pets(db=db)
    if not db_adopted_pet:
        raise HTTPException(
            status_code=404, detail=f"No adopted pets found"
        )
    return db_adopted_pet


@router.get("/pet_type/{p_type}", response_model=List[pet.Pet])
def get_pets_by_type(p_type: str, db: Session = Depends(get_db)):
    db_pets = pets.get_pets_type(db=db, p_type=p_type)
    if not db_pets:
        raise HTTPException(
            status_code=404, detail=f"No {p_type}s found"
        )
    return db_pets


@router.get("/owner/{id}", response_model=owner.OwnerOut)
def get_pet_owner(id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_pet_owner = pets.get_pet_owner(db=db, id=id)
    if db_pet_owner is None:
        raise HTTPException(
            status_code=404, detail=f"Pet with id {id} not found"
        )
    return db_pet_owner


@router.post("/insert/{name}")
def insert_pet(pet: pet.BasePet, name: str = Path(..., min_length=2), db: Session = Depends(get_db)):
    pet_owner = owners.get_owner_by_id(db=db, id=pet.owner_id)
    if pet_owner is None:
        raise HTTPException(
            status_code=404, detail=f"Owner with id {pet.owner_id} not found"
        )
    return pets.insert_pet(db=db, pet=pet, name=name)


@router.delete("/{id}")
def delete_pet(id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return pets.delete_pet(db=db, id=id)


@router.delete("/delete_all/")
def delete_all(db: Session = Depends(get_db)):
    return pets.delete_all_pets(db=db)


@router.put("/update/{id}")
def update_pet(pet: pet.UpdatePet, id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_pet_id = pets.update_pet(db=db, pet=pet, id=id)
    if db_pet_id is None:
        raise HTTPException(
            status_code=404, detail=f"Pet with id {id} not found"
        )
    return db_pet_id


@router.post("/test_data/")
def generate_test_data(db: Session = Depends(get_db)):
    return pets.test_data(db=db)


@router.post("/reset_index/")
def reset_pet_index(db: Session = Depends(get_db)):
    return pets.reset_index(db=db)
