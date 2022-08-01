from fastapi import APIRouter, HTTPException
from os import getcwd, path
import json


resultsRouter = APIRouter()

@resultsRouter.get("/result/{id}", status_code=200)
async def get_result_by_id(id: str):

    if not id:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid id",
            },
        )

    results_folder = path.join(getcwd(), "results")
    # validate if results folder path exists
    if not path.exists(results_folder):
        return {}
    
    # validate if the specific folder for this id exists
    result_folder = path.join(results_folder, id)
    if not path.exists(result_folder):
        return {}

    # validate if the results were generated
    result_json = path.join(result_folder, "results.json")
    if not path.exists(result_json):
        return {}
    
    with open(result_json) as json_file:
        data = json.load(json_file)
    
        
    return data