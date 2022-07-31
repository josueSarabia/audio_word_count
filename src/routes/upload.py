from fastapi import APIRouter, UploadFile, File
from os import getcwd, path, mkdir
from analyzeaudio import analyze_audio
from uuid import uuid4

uploadRouter = APIRouter()

@uploadRouter.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    results_folder = path.join(path.dirname(getcwd()), "results")
    if not path.isdir(results_folder):
        mkdir(results_folder)

    base_path = path.join(results_folder, str(uuid4()))
    if not path.isdir(base_path):
        mkdir(base_path)

    file_path = path.join(base_path, file.filename)
    with open(file_path, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
    result = analyze_audio(file_path, base_path)
    print(result)
    return result