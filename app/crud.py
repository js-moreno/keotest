from sqlalchemy.orm import Session

from app import models, schemas


def get_records(db: Session, array: str = None, result: int = None):
    query = db.query(models.Record)
    if array is not None:
        query =  query.filter_by(array=array)
    if result is not None:
        query =  query.filter_by(result=result)
    return query.all()


def create_record(db: Session, record: schemas.RecordCreate):
    db_record = models.Record(array=record.array, result=record.result)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record