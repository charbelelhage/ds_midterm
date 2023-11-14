import os
import subprocess
from starlette.responses import HTMLResponse
from fastapi import  FastAPI, Request, File, UploadFile,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="templates")
running_processes = {}

app.mount("/static", StaticFiles(directory="fastapi/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


#This is the new upload function
@app.post("/upload")
async def upload_file(bagfile: UploadFile = File(...), start_time: float = Form(...),
                      end_time: float = Form(...),output_folder: str = Form(...),
                      topics_dropdown: str = Form(...)):
    if start_time is None:
        start_time = 0 #Checking if stratTime was null then assign it the value 0
    if end_time is None:
        end_time = 9999999999  #Checking if End Time was null then assign it the value 9999999999
    if output_folder is None:
        output_folder = "/"
        #Checking if the output folder value was null, assign it the value "/"
        # to save the images in the same directory

    last_character=output_folder[-1] #to get the last character of the output folder specified
    if last_character!="/":
        output_folder=output_folder + "/"
        #to add / to the end of the output folder to be able to create the directory

    filename = bagfile.filename
    extension = os.path.splitext(filename)[1] #Split the filename to get the file extention
    if extension != ".bag":
        #if the user has uploaded a file different than a bag file,
        # the api will return a response with status fail and a message.
        data = {
            "status": "fail",
            "message": "Only bag format is accepted!"
        }
        return JSONResponse(status_code=200,content=data)

    if topics_dropdown =="/rgb_image":
        #Command that will call the python script responsible of extracting the images
        # depending on the arguments sent by the form.
        command="python3 extract_images.py "+ bagfile.filename +" --topic "+ topics_dropdown +" --output "+ output_folder +" --start_time "+ str(start_time)+" --end_time "+  str(end_time)
        #This call is used to run the command in the background so the function won't wait for the
        # command to finish execution to return a response.
        process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
        pid = process.pid
        data = {
            "status": "success",
            "message": "The action has started successfully!",
            "pid":pid
        }
    elif topics_dropdown=="/camera/points":
        #Command that will call the python script responsible of extracting
        # the pointclouds depending on the arguments sent by the form.
        command="python3 extract_pointcloud_to_pcd.py "+ bagfile.filename +" --topic "+ topics_dropdown +" --output "+ output_folder +" --start_time "+ str(start_time)+" --end_time "+  str(end_time)
        #This call is used to run the command in the background so the function
        # won't wait for the command to finish execution to return a response.
        process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
        pid = process.pid
        data = {
            "status": "success",
            "message": "The action has started successfully!",
            "pid":pid
        }
    return JSONResponse(status_code=200, content=data)



@app.post("/terminate-command/{pid}")
async def terminate_command(pid: int):
    try:
        os.killpg(os.getpgid(pid), 15)
        data = {"status": "success",
        "message": "Process killed successfully"}
        return JSONResponse(status_code=200, content=data)
    except OSError:
        data = {"status": "fail",
        "message": "Failed to kill the Proccess!"}
        return JSONResponse(status_code=200, content=data)

@app.get("/testing")
async def test():
    return 1
