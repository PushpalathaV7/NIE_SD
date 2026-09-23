from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import pymongo
from pymongo import MongoClient
from bson import ObjectId

#app
app = FastAPI()

#db configuration
URI = "mongodb://127.0.0.1:27017"
client = MongoClient(URI)
db = client["college_service_db"]
ticket_collection = db["tickets"]

#SCHEMA
class TicketCreate(BaseModel):
    title: str
    description: str
    category: str
    status: str

class TicketResponse(TicketCreate):
    id: str
    
#helper
def ticket_helper(ticket_doc):
    return {
        "id": str(ticket_doc["_id"]),
        "title": ticket_doc["title"],
        "description": ticket_doc["description"],
        "category": ticket_doc["category"],
        "status": ticket_doc["status"]
    }
    
    #apis -CURD - create, read all, read by id, update, delete
    @app.post("/tickets",status_code=201, response_model=TicketResponse)
    def ticket_create(PLAYLOAD: TicketCreate):
        ticket_dict = payload.model_dump()
        result = ticket_collection.insert_one(ticket_dict)
        new_ticket = ticket_collection.find_one({"_id": result.inserted_id})
        return ticket_helper(new_ticket)
    
    @app.get("/tickets", response_model=list[TicketResponse])
    def ticket_read_all():
        doc=ticket_collection.find()
        tickets = [ticket_helper(doc) for doc in doc]
        return tickets
     
    @app.get("/tickets/{id}", response_model=TicketResponse)
    def ticket_read_by_id(id: str):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=403, detail="Invalid ticket ID")
        doc = ticket_collection.find_one({"_id": ObjectId(id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket_helper(doc)
    
    @app.put("/tickets/{id}", response_model=TicketResponse)
    def ticket_update(id: str, payload: TicketCreate):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=403, detail="Invalid ticket ID")
        ticket_dict = payload.model_dump()
        result = ticket_collection.update_one({"_id": ObjectId(id)}, {"$set": ticket_dict})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Ticket not found")
        new_ticket = ticket_collection.find_one({"_id": ObjectId(id)})
        return ticket_helper(new_ticket)
    
    @app.delete("/tickets/{id}")
    def ticket_delete(id: str):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=403, detail="Invalid ticket ID")
        result = ticket_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return {"message": "Ticket deleted successfully"}