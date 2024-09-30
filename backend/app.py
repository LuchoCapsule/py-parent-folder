# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
import httpx
import uuid

from interfaces.IUser import IUser  # Correct import
from interfaces.IResponseStatus import IResponseStatus  # Correct import
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
        #write the users_db to txt file
        resp =  await write_users_db(users_db)
        if resp == False:
            raise HTTPException(status_code=404, detail="Error writing users_db to file")            
        else:
            print("users_db written to file")
            lst_users = await read_users_db()
            return lst_users        
    
@app.get("/users", response_model=List[IUser])
async def get_users():    
    lst_users = await read_users_db()     
    return lst_users
    
@app.post("/users", response_model=IUser)
async def create_user(user: IUser):
    # Generate a random ID if not provided
    user_id = uuid.uuid4().int & (1<<31)-1  # Generate a random 32-bit integer
    new_user = IUser(id=user_id, name=user.name, username=user.username, email=user.email)
    #users_db.append(new_user)
    resp = await add_user_db(new_user)
    if resp == False:
        raise HTTPException(status_code=404, detail="Error adding user to file")
    else:
        print("user added to file")
        lst_users = await read_users_db()
        return new_user

@app.delete("/users/{user_id}", response_model=IResponseStatus)
async def delete_user(user_id: int):
    resp = await read_users_db()
    if resp == False:
        raise HTTPException(status_code=404, detail="Error reading users_db from file")
    
    user = next((u for u in users_db if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    resp = await remove_user_db(user)
    if resp == False:
        raise HTTPException(status_code=404, detail="Error removing user from file")
    else:
        print("user removed from file")
        return IResponseStatus(status="Eliminado",data=user)  # Return as IResponseStatus object

@app.put("/users/{user_id}", response_model=IResponseStatus)
async def update_user(user_id: int, updated_user: IUser):
    print("user_id update=>", user_id)
    resp = await read_users_db()
    user = next((u for u in users_db if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user.id = user_id
    resp = await update_user_db(updated_user)
    return IResponseStatus(status="Actualizado",data=updated_user)  # Return as IResponseStatus object

async def write_users_db( p_users_db : List[IUser] ):
    #write the users_db to txt file
    with open("users_db.txt", "w") as file:
        for user in p_users_db:
            file.write(f"{user.id},{user.name},{user.username},{user.email}\n")
    return True
# function to add a new user to the users_db.txt file
async def add_user_db( p_user : IUser ):
    #write the users_db to txt file
    with open("users_db.txt", "a") as file:
        file.write(f"{p_user.id},{p_user.name},{p_user.username},{p_user.email}\n")
    return True
# function to read the users_db from txt file
# function to read the users_db from txt file
async def read_users_db():
    # Check if the file exists
    if not os.path.exists("users_db.txt"):
        return []  # Return an empty list if the file does not exist

    # Read the users_db from txt file
    users_db.clear()
    with open("users_db.txt", "r") as file:
        for line in file:
            id, name, username, email = line.strip().split(",")
            users_db.append(IUser(id=int(id), name=name, username=username, email=email))
    return users_db

# function to remove a user from the users_db.txt file
async def remove_user_db( p_user : IUser ):
    #write the users_db to txt file
    with open("users_db.txt", "w") as file:
        for user in users_db:
            if user.id != p_user.id:
                file.write(f"{user.id},{user.name},{user.username},{user.email}\n")
    return True

# function to update a user from the users_db.txt file
async def update_user_db( p_user : IUser ):
    resp = read_users_db()
    #write the users_db to txt file
    with open("users_db.txt", "w") as file:
        for user in users_db:
            if user.id == p_user.id:
                print("user found=>", user.id)
                file.write(f"{p_user.id},{p_user.name},{p_user.username},{p_user.email}\n")
            else:
                file.write(f"{user.id},{user.name},{user.username},{user.email}\n")
    return True