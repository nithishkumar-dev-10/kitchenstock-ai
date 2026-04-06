from pydantic import BaseModel
from typing import List,Dict

class RecipeSuggestInput(BaseModel):
    max_missing:int=2

class RecipeData(BaseModel):
    available:List[str]
    partial:List[Dict]
class RecipeResponse(BaseModel):
    status:str
    suggestion:RecipeData