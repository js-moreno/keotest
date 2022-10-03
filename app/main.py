from typing import List

from pydantic import BaseModel

from sqlalchemy.orm import Session

from fastapi import  Depends, FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse, JSONResponse
import fastapi.openapi.utils as fu

from app.database import SessionLocal, engine
from app import crud, models, schemas

import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Handling error override
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({"error":str(exc)}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

# Documentation error override
fu.validation_error_response_definition = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "error": {"title": "Message", "type": "string"}, 
    },
}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/redoc')


class Array(BaseModel):
    array: List[int]

class Result(BaseModel):
    result: int

@app.post("/smallest", responses={200:{"model": Result}})
async def smallest(input:Array, db: Session = Depends(get_db)):
        json_array = json.dumps(input.array)
        records = crud.get_records(db,array=json_array)
        if records:
            return {"result": records[0].result}
        else:
            i = 1
            values = set(input.array)
            while True: # O(n)
                if i not in values: # O(1)
                    result = i
                    break
                else:
                    i = i + 1
            crud.create_record(db, record=schemas.RecordCreate(array=json.dumps(input.array), result=result))
            return {"result": result}


class Stats(BaseModel):
    count: int
    total: int
    ratio: float

@app.get("/stats",responses={200:{"model":Stats}})
async def stats(result: int, db: Session = Depends(get_db)):

        records_total = len(crud.get_records(db))
        records_filtered = len(crud.get_records(db, result=result))

        return {
                "count": records_filtered,
                "total": records_total,
                "ratio": (records_filtered/records_total) if records_total > 0 else 0
            }
