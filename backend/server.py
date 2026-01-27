from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Contact Message Models
class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    company: Optional[str] = Field(None, max_length=200)
    message: str = Field(..., min_length=1, max_length=2000)

class ContactMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    company: Optional[str] = None
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    read: bool = False
    replied: bool = False

class ContactMessageUpdate(BaseModel):
    read: Optional[bool] = None
    replied: Optional[bool] = None

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Contact Message Endpoints
@api_router.post("/contact", response_model=ContactMessage, status_code=201)
async def create_contact_message(contact: ContactMessageCreate):
    """
    Create a new contact message from the landing page form
    """
    try:
        contact_dict = contact.model_dump()
        contact_obj = ContactMessage(**contact_dict)
        
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = contact_obj.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        
        # Insert into MongoDB
        _ = await db.contact_messages.insert_one(doc)
        
        # Log the contact message
        logger.info(f"New contact message from {contact_obj.email}")
        
        return contact_obj
    except Exception as e:
        logger.error(f"Error creating contact message: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating contact message")

@api_router.get("/contact", response_model=List[ContactMessage])
async def get_contact_messages():
    """
    Get all contact messages (for admin panel)
    """
    try:
        messages = await db.contact_messages.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
        
        # Convert ISO string timestamps back to datetime objects
        for msg in messages:
            if isinstance(msg['created_at'], str):
                msg['created_at'] = datetime.fromisoformat(msg['created_at'])
        
        return messages
    except Exception as e:
        logger.error(f"Error fetching contact messages: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching contact messages")

@api_router.get("/contact/{contact_id}", response_model=ContactMessage)
async def get_contact_message(contact_id: str):
    """
    Get a specific contact message by ID
    """
    try:
        message = await db.contact_messages.find_one({"id": contact_id}, {"_id": 0})
        if not message:
            raise HTTPException(status_code=404, detail="Contact message not found")
        
        # Convert ISO string timestamp back to datetime object
        if isinstance(message['created_at'], str):
            message['created_at'] = datetime.fromisoformat(message['created_at'])
        
        return ContactMessage(**message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching contact message: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching contact message")

@api_router.patch("/contact/{contact_id}", response_model=ContactMessage)
async def update_contact_message(contact_id: str, update: ContactMessageUpdate):
    """
    Update contact message status (mark as read/replied)
    """
    try:
        # Build update dict only with provided fields
        update_dict = {k: v for k, v in update.model_dump().items() if v is not None}
        
        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Update in MongoDB
        result = await db.contact_messages.find_one_and_update(
            {"id": contact_id},
            {"$set": update_dict},
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Contact message not found")
        
        # Convert ISO string timestamp back to datetime object
        if isinstance(result['created_at'], str):
            result['created_at'] = datetime.fromisoformat(result['created_at'])
        
        return ContactMessage(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating contact message: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating contact message")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()