from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from models import Gender, Role, UpdatedUser, User

app = FastAPI()

database: List[User] = [
    User(
        id=UUID("a7cce501-e96b-43c8-9db8-4aaa0a38696a"),
        first_name="Jamila",
        last_name="Ahmed",
        gender=Gender.female,
        roles=[Role.student],
    ),
    User(
        id=UUID("27cce501-e96b-43c8-9db8-4aaa0a38696a"),
        first_name="Alex",
        last_name="Jones",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),
]


@app.get("/")
async def root():
    return {"Hello": "World BABEE!!!"}

@app.get("/api/v1/users")
async def fetch_users():
    return database # Return everything in the database

@app.post("/api/v1/users")
async def create_user(user: User):
    database.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in database:
        if user.id == user_id:
            database.remove(user)
            return {f"Deleted User:  {user.first_name} -> ID:{user.id}"}
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {user_id} does not exist.")

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UpdatedUser, user_id: UUID):
    for user in database:
        if user.id ==user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return f"User updated"
    raise HTTPException(
        status_code=404,
        detail=f"User with id {user_id} does not exist."
    )
            
            