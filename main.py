from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


def generate_html_response(users):

    t = ""
    for user in users:
        t += "<li>{}</li>".format(user.name)

    html_content = """
    <html>
        <head>
            <title>Hello</title>
        </head>
        <body>
            <h1>Add your name</h1>
            <input type="text" id="name" name="name">
            <button onclick="addName()">Add</button>
            <ol>""" + t + """</ol>
        </body>
        
        <script>
        function addName(){
          var name = document.getElementById("name").value;
          console.log(name);
          var apiUrl = 'http://localhost:8000/users/';
          fetch(apiUrl, {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
              'Content-Type': 'application/json'
            },
            redirect: 'follow',
            referrerPolicy: 'no-referrer',
            body: JSON.stringify({name:name})
          }).then(response => {
            return response.json();
          }).then(data => {
            console.log(data);
            window.location.reload();
          }).catch(err => {
          });
          document.getElementById("name").value = ""
        }
        </script>
        
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)


@app.get("/", response_class=HTMLResponse)
def root(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return generate_html_response(users)