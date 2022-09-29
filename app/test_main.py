from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.main import app, get_db
from app.database import Base, engine

import pytest
import json

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

db = TestingSessionLocal()
client = TestClient(app)

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.mark.parametrize(
    "array,result",
    [
        ([1, 3, 6, 4, 1, 2],5),
        ([1, 2, 3],4),
        ([-1,-3],1),
    ],
)
def test_smallest_endpoint_correct(test_db,array,result):
    response = client.post("/smallest",json={"array": array})
    assert response.status_code == 200
    assert response.json() == {"result": result}

@pytest.mark.parametrize(
    "result",
    [5,4,3,2,1,0],
)
def test_stats_endpoint_correct(test_db,result):
    response = client.get("/stats", params={"result": result})

    records_total = db.query(models.Record).count()
    records_filtered = db.query(models.Record).filter_by(result=result).count()

    assert response.status_code == 200
    assert response.json() == {
        "count": records_filtered,
        "total": records_total,
        "ratio": (records_filtered/records_total) if records_total > 0 else 0
    }

def test_smallest_endpoint_missing_data(test_db):
    response = client.post("/smallest")
    assert response.status_code == 422
    assert "error" in response.json()
    assert "value_error" in response.json()["error"]


def test_smallest_endpoint_error_data(test_db):
    response = client.post("/smallest",json={"array": "foo"})
    assert response.status_code == 422
    assert "error" in response.json()
    assert "type_error" in response.json()["error"]


def test_stats_endpoint_missing_data(test_db):
    response = client.get("/stats")
    assert response.status_code == 422
    assert "error" in response.json()
    assert "value_error" in response.json()["error"]


def test_stats_endpoint_error_data(test_db):
    response = client.get("/stats", params={"result": "foo"})
    assert response.status_code == 422
    assert "error" in response.json()
    assert "type_error" in response.json()["error"]


def test_smallest_endpoint_unique_array(test_db):
    array = [1,2,3,4,5]
    assert db.query(models.Record).filter_by(array=json.dumps(array)).all() == []
    response = client.post("/smallest",json={"array": array})
    assert response.status_code == 200
    assert db.query(models.Record).filter_by(array=json.dumps(array)).all() != []    
