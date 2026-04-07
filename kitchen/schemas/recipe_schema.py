from pydantic import BaseModel, Field
from typing import List, Dict

class RecipeSuggestInput(BaseModel):
    max_missing: int = Field(default=2, ge=0, example=2)

class RecipeData(BaseModel):
    available: List[str] = Field(default_factory=list, example=["rice", "egg"])
    partial: List[Dict] = Field(default_factory=list)

class RecipeResponse(BaseModel):
    status: str = Field(..., example="success")
    suggestion: RecipeData