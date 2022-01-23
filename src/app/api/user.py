
from fastapi import APIRouter, Depends, exceptions, status
from sqlalchemy.orm import Session
from app.core.dependecies import get_db
from app import crud, schemas

router = APIRouter()


@router.get(
    "/users/",
    response_model=list[schemas.UserOutDB],
    status_code=status.HTTP_200_OK,
)
def user_list(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):

    return crud.user.get_multi(db, skip, limit)


@router.post(
    "/users/",
    response_model=schemas.UserOutDB,
    status_code=status.HTTP_201_CREATED,
)
def user_create(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if crud.user.get_user_by_email(db, user) is not None:
        raise exceptions.HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={"message": "This email is already registered."},
        )

    return crud.user.create(db, user)


@router.get(
    "/users/{user_id}/",
    response_model=schemas.UserOutDB,
    status_code=status.HTTP_200_OK,
)
def get_single_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.user.get(db, user_id)
    if user is None:
        raise exceptions.HTTPException(
            status.HTTP_404_NOT_FOUND, detail={"message": "User not found."}
        )
    return crud.user.get(db, user_id)


@router.put(
    "/users/{user_id}/",
    response_model=schemas.UserOutDB,
    status_code=status.HTTP_200_OK,
)
def update_user_with_put(
    user_id: int, update_schema: schemas.UserUpdate, db: Session = Depends(get_db)
):
    user = crud.user.get(db, user_id)
    if user is None:
        raise exceptions.HTTPException(
            status.HTTP_404_NOT_FOUND, detail={"message": "User not found."}
        )
    return crud.user.update(db, user, update_schema)


@router.patch(
    "/users/{user_id}/",
    response_model=schemas.UserOutDB,
    status_code=status.HTTP_200_OK,
)
def update_user_with_patch(
    user_id: int, update_schema: schemas.UserUpdate, db: Session = Depends(get_db)
):
    user = crud.user.get(db, user_id)
    if user is None:
        raise exceptions.HTTPException(
            status.HTTP_404_NOT_FOUND, detail={"message": "User not found."}
        )
    return crud.user.update(db, user, update_schema)
