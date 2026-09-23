from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message": "College Service Request System - Server"}

db = {

    1: {
        "id": 1,
        "title": "Classroom fan is not working",
        "description": "Fan is not working in classroom",
        "category": "Electrical",
        "status": "new"
    },

    2: {
        "id": 2,
        "title": "Projector is not working",
        "description": "Projector is not displaying properly",
        "category": "Technical",
        "status": "new"
    },

    3: {
        "id": 3,
        "title": "Water problem in college",
        "description": "Drinking water facility is not working",
        "category": "Maintenance",
        "status": "new"
    },

}

# Schema for service request creation

class TicketCreate(BaseModel):

    title: str

    description: str

    category: str

    status: str


class TicketResponse(TicketCreate):

    id: int


# API to create a service request

@app.get("/college")
def ticket_read_all():

    return list(db.values())


@app.get("/college/{id}")
def ticket_read_by_id(id: int):

    if id not in db:

        raise HTTPException(status_code=404, detail="Service request not found")

    return db[id]


@app.post("/college", status_code=201, response_model=TicketResponse)
def ticket_create(ticket_payload: TicketCreate):

    new_id = max(db.keys(), default=0) + 1

    db[new_id] = {
        "id": new_id,
        **ticket_payload.model_dump()
    }

    return db[new_id]


@app.put("/college/{id}", response_model=TicketResponse)
def ticket_update(id: int, ticket_payload: TicketCreate):

    if id not in db:

        raise HTTPException(status_code=404, detail="Service request not found")

    db[id] = {
        "id": id,
        **ticket_payload.model_dump()
    }

    return db[id]


@app.delete("/college/{id}")
def ticket_delete(id: int):

    if id not in db:

        raise HTTPException(status_code=404, detail="Service request not found")

    del db[id]

    return {"message": "Service request deleted successfully"}