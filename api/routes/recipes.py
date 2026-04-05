from fastapi import APIRouter
from pydantic import BaseModel
from typing import List,Dict
from kitchen.services.recipe_suggester import suggest_recipes
from fastapi import HTTPException

class RecipeSuggestInput(BaseModel):
    max_missing:int=2

class RecipeData(BaseModel):
    available:List[str]
    partial:List[Dict]
class RecipeResponse(BaseModel):
    status:str
    suggestion:RecipeData

router=APIRouter()

@router.post("/recipe_suggestion",response_model=RecipeResponse)
def suggest(data:RecipeSuggestInput):
    result=suggest_recipes(data.max_missing)
    if not result:
        raise HTTPException(status_code=404, detail="No items to suggest ")
    return{
        "status":"success",
        "suggestion":result
    }