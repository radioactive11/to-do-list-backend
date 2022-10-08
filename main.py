from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2


conn = psycopg2.connect(host="localhost", user="arijitroy")

app = FastAPI()


@app.get("/touch")
def _touch():
    return {"status": "ok"}


class CreateNote(BaseModel):
    value: str


@app.put("/create")
def _create_note(request_body: CreateNote):
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (value) VALUES (%s)", (request_body.value,))
    conn.commit()

    cur.close()

    return {"status": "inserted"}


class UpdateNote(BaseModel):
    id: int
    value: str


@app.post("/edit")
def _create_note(request_body: UpdateNote):
    cur = conn.cursor()
    cur.execute(
        "UPDATE notes SET value = %s WHERE id = %s",
        (request_body.value, request_body.id),
    )
    conn.commit()

    cur.close()

    return {"status": "updated"}


class CheckNote(BaseModel):
    id: int


@app.post("/check")
def _create_note(request_body: CheckNote):
    cur = conn.cursor()
    cur.execute(
        "UPDATE notes SET checked = NOT checked WHERE id = %s",
        (request_body.id,),
    )
    conn.commit()

    cur.close()

    return {"status": "toggled"}


@app.get("/notes")
def _fetch_all():
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes")

    query_results = cur.fetchall()
    results = []

    for result in query_results:
        temp_dict = {"id": result[0], "value": result[1], "checked": result[2]}
        results.append(temp_dict)

    return results
