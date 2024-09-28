# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
import httpx
import uuid

from interfaces.IUser import IUser  # Correct import
from interfaces.IResponseStatus import IResponseStatus  # Correct import

app = FastAPI()

# In-memory storage for users
users_db: List[IUser] = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/usersInit", response_model=List[IUser])
async def usersInit():
    global users_db  # Use the global users_db variable
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/users")
        response.raise_for_status()
        users_data = response.json()
        
        # Clear the existing users_db list and populate it with new data
        users_db.clear()
        users_db.extend(
            IUser(
                id=user["id"],
                name=user["name"],
                username=user["username"],
                email=user["email"]
            )
            for user in users_data
        )
        
        return users_db
    
@app.get("/users", response_model=List[IUser])
async def get_users():         
    return users_db
    
@app.post("/users", response_model=IUser)
async def create_user(user: IUser):
    # Generate a random ID if not provided
    user_id = uuid.uuid4().int & (1<<31)-1  # Generate a random 32-bit integer
    new_user = IUser(id=user_id, name=user.name, username=user.username, email=user.email)
    users_db.append(new_user)
    return new_user

@app.delete("/users/{user_id}", response_model=IResponseStatus)
async def delete_user(user_id: int):
    user = next((u for u in users_db if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    users_db.remove(user)
    return IResponseStatus(status="Eliminado",data=user)  # Return as IResponseStatus object

@app.put("/users/{user_id}", response_model=IResponseStatus)
async def update_user(user_id: int, updated_user: IUser):
    print("user_id update=>", user_id)
    user = next((u for u in users_db if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = updated_user.name
    user.username = updated_user.username
    user.email = updated_user.email
    return IResponseStatus(status="Actualizado",data=user)  # Return as IResponseStatus object