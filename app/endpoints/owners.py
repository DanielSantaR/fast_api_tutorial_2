from app.crud import owners
from app.models import models
from app.schemas import owner, pet
from db.database import SessionLocal, engine
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List


models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/all/", response_model=List[owner.OwnerOut])
def get_all_owners(db: Session = Depends(get_db)):
    db_owners = owners.get_all_owners(db=db)
    if not db_owners:
        raise HTTPException(
            status_code=404, detail=f"No owners found"
        )
    return db_owners


@router.get("/id/{id}", response_model=owner.OwnerOut)
def get_owner_by_id(id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_owners = owners.get_owner_by_id(db=db, id=id)
    if db_owners is None:
        raise HTTPException(
            status_code=404, detail=f"No owners found with id {id}"
        )
    return db_owners


@router.get("/username/{username}", response_model=owner.OwnerOut)
def get_owner_by_username(username: str, db: Session = Depends(get_db)):
    db_owners = owners.get_owner_by_username(db=db, username=username)
    if db_owners is None:
        raise HTTPException(
            status_code=404, detail=f"No owners found with username {username}"
        )
    return db_owners


@router.get("/email/{email}", response_model=owner.OwnerOut)
def get_owner_by_email(email: str, db: Session = Depends(get_db)):
    db_owners = owners.get_owner_by_email(db=db, email=email)
    if db_owners is None:
        raise HTTPException(
            status_code=404, detail=f"No owners found with email {email}"
        )
    return db_owners


@router.get("/pets/{id}", response_model=List[pet.Pet])
def get_owner_pets(id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_owners = owners.get_owner_pets(db=db, id=id)
    if not db_owners:
        raise HTTPException(
            status_code=404, detail=f"No owners found with id {id}"
        )
    return db_owners


@router.post("/insert/")
def insert_owner(owner: owner.Owner, db: Session = Depends(get_db)):
    field_validation(owner=owner, db=db)
    return owners.insert_owner(db=db, owner=owner)


@router.put("/update/{id}")
def update_owner(owner: owner.OwnerUpdate, id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_owner_id = owners.update_owner(db=db, owner=owner, id=id)
    if db_owner_id is None:
        raise HTTPException(
            status_code=404, detail=f"Owner with id {id} not found"
        )
    field_validation(owner=owner, db=db)
    return db_owner_id


@router.delete("/delete_id/{id}")
def delete_owner_by_id(id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return owners.delete_owner_by_id(db=db, id=id)


@router.delete("/delete_username/{username}")
def delete_owner_by_username(username: str, db: Session = Depends(get_db)):
    return owners.delete_owner_by_username(db=db, username=username)


@router.delete("/delete_all/")
def delete_all(db: Session = Depends(get_db)):
    return owners.delete_all_owners(db=db)


@router.post("/test_data/")
def generate_test_data(db: Session = Depends(get_db)):
    return owners.test_data(db=db)


@router.post("/reset_index/")
def reset_owner_index(db: Session = Depends(get_db)):
    return owners.reset_index(db=db)


def field_validation(owner: owner.Owner, db: Session = Depends(get_db)):
    db_owner_username = owners.get_owner_by_username(
        db=db, username=owner.username)
    if db_owner_username is not None:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )

    db_owner_email = owners.get_owner_by_email(db=db, email=owner.email)
    if db_owner_email is not None:
        raise HTTPException(
            status_code=404, detail="email already registered"
        )
    else:
        return None
