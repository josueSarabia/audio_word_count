from fastapi import APIRouter, HTTPException, UploadFile, File
from os import getcwd, path, mkdir
# delete reltive path "src."
from src.analyzeaudio import analyze_audio
from uuid import uuid4

uploadRouter = APIRouter()

@uploadRouter.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    # get results folder path
    # path.dirname(getcwd())
    results_folder = path.join(getcwd(), "results")

    # validate if results folder path exists
    if not path.exists(results_folder):
        mkdir(results_folder)

    # generate unique identifier 
    uuid_attemp = uuid4()

    # validate if the folder of the new attemp/request exists
    base_path = path.join(results_folder, str(uuid_attemp))
    if not path.exists(base_path):
        mkdir(base_path)
    
    # validate if vocabulary.txt(words configured by user) exists
    # path.dirname(getcwd())
    if not path.exists(path.join(getcwd(), "vocabulary.txt")):
        raise HTTPException(
            status_code=500,
            detail=f"file vocabulary.txt not found",
        )

    # save mp3 file to results folder
    file_path = path.join(base_path, file.filename)
    with open(file_path, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
    
    # start analyzing mp3 file
    result = analyze_audio(file_path, base_path)
    print(result)

    # add unique identifier to response
    result["UUID"] = uuid_attemp

    return result