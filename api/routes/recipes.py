from fastapi import APIRouter
from kitchen.services.recipe_suggester import suggest_recipes
from fastapi import HTTPException
from kitchen.schemas.recipe_schema import RecipeResponse,RecipeSuggestInput

router=APIRouter()

@router.post("/recipes/suggest",response_model=RecipeResponse)
def suggest(data:RecipeSuggestInput):
    result=suggest_recipes(data.max_missing)
    if result is None:
        raise HTTPException(status_code=404, detail="No items to suggest ")
    return{
        "status":"success",
        "suggestion":result
    }