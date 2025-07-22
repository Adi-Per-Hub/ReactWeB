from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Starting FastAPI application...")

print("hello world")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process/")
async def process_file(file: UploadFile, name: str = Form(...)):
    try:
        logging.info(f"Received file: {file.filename} with name: {name}")
        
        content = await file.read()
        output_path = os.path.join(UPLOAD_DIR, f"{name}_processed.txt")

        with open(output_path, "w") as f:
            f.write(f"Processed for {name}\n")
            f.write(content.decode())

        logging.info(f"File saved to: {output_path}")
        return {"download_url": f"/download/{name}_processed.txt"}
    
    except Exception as e:
        logging.error(f"Error while processing file: {e}")
        raise HTTPException(status_code=500, detail="Processing failed")


@app.get("/download/{filename}")
def download(filename: str):
    abs_upload_dir = os.path.abspath(UPLOAD_DIR)
    file_path = os.path.join(abs_upload_dir, filename)
    logging.info(f"🔎 Looking for file: {file_path}")

    if not os.path.exists(file_path):
        logging.error(f"❌ File not found: {file_path}")
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename)
