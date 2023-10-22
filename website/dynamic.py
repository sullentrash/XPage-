from inference import *
from database import *
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Depends, FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
import base64

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def dynamic_file(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("dynamic.html", {"request": request})

@app.post("/dynamic")
def dynamic(request: Request, file: UploadFile = File(), db: Session = Depends(get_db)):
    data = file.file.read()
    fl_name = "uploads/saved_" + file.filename
    with open(fl_name, "wb") as f:
        f.write(data)
    _,label = infer('weigths/vit_b_20epoch',fl_name)
    label = 'кошка' if label == 'cat' else 'собака'
    file.file.close()
    visit = Visit(date=datetime.now(), img_name=file.filename, animal = label)
    db.add(visit)
    db.commit()
    db.refresh(visit)

    # encoding and decoding the image bytes
    encoded_image = base64.b64encode(data).decode("utf-8")

    return templates.TemplateResponse("dynamic.html", {"request": request,  "img": encoded_image, "label" : label})