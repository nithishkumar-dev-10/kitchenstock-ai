from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from kitchen.core.database import get_db
from kitchen.core.auth import hash_password, verify_password, create_access_token, get_current_user
from kitchen.models.models import User, UserInventory
from kitchen.schemas.auth_schema import (
    SignupRequest, LoginRequest, TokenResponse,
    OnboardingComplete
)
import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    # Check duplicate email
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        id=str(uuid.uuid4()),
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        onboarded=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id})

    return TokenResponse(
        access_token=token,
        onboarded=user.onboarded,
        user_id=user.id,
        name=user.name
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.id})

    return TokenResponse(
        access_token=token,
        onboarded=user.onboarded,
        user_id=user.id,
        name=user.name
    )


@router.post("/onboarding")
def complete_onboarding(
    data: OnboardingComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Save profile
    current_user.family_size = data.profile.family_size
    current_user.diet = data.profile.diet
    current_user.region = data.profile.region
    current_user.cooking_freq = data.profile.cooking_freq
    current_user.onboarded = True

    # Clear old inventory if any
    db.query(UserInventory).filter(UserInventory.user_id == current_user.id).delete()

    # Insert selected ingredients
    for ing in data.ingredients:
        item = UserInventory(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            item=ing.item,
            quantity=ing.quantity,
            unit=ing.unit,
            threshold=ing.threshold or 200.0
        )
        db.add(item)

    db.commit()

    return {"message": "Onboarding complete", "user_id": current_user.id}


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "onboarded": current_user.onboarded,
        "family_size": current_user.family_size,
        "diet": current_user.diet,
        "region": current_user.region,
    }
