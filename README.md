# Keotest

Welcome to the keotest!

Keotest is a documented RESTful API powered by [FastAPI](https://fastapi.tiangolo.com/) with you can find the smallest positive integer in a given array and also get a interesting stats

Example https://keotest.herokuapp.com

## Pre-requirements

- Python 3.7+

## Get started

Firstable you need to clone the repository using `git clone https://github.com/js-moreno/keotest.git`.

Then you can create and activate a isolated virtualenv using `python -m virtualenv .venv` to create and `source .venv/Scripts/activate` to activate (Windows OS)

Now you can install all dependencies with `pip install -r requirements.txt`.

Finally you must to define your environ variables using **.env.example** as a reference create a **.env** file. (For a quick-start dev environment you could use `SQLALCHEMY_DATABASE_URL="sqlite:///./sql_app.db?check_same_thread=False"`)

In the end you will be able to run a server with `uvicorn app.main:app`.

In addition if you want to check tests you can use command `pytest` or even `pytest --cov-report term-missing --cov=app` if you want to verify the coverage.
