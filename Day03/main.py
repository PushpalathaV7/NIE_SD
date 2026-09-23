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
    
    