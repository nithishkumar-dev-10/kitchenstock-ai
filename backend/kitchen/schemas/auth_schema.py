from pydantic import BaseModel, EmailStr
from typing import Optional, List


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    onboarded: bool
    user_id: str
    name: str


class OnboardingProfile(BaseModel):
    family_size: int = 1
    diet: str = "mixed"
    region: str = "india"
    cooking_freq: str = "twice_daily"


class IngredientSetup(BaseModel):
    item: str
    quantity: float
    unit: str
    threshold: Optional[float] = 200.0


class OnboardingInventory(BaseModel):
    ingredients: List[IngredientSetup]


class OnboardingComplete(BaseModel):
    profile: OnboardingProfile
    ingredients: List[IngredientSetup]
