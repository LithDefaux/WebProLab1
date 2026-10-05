from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3
import uuid

app = FastAPI()

# Allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the WebPro API! Go to /docs to see the documentation."}

def get_db_connection():
    conn = sqlite3.connect('database.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            fullName TEXT NOT NULL,
            firstName TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            skills TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class User(BaseModel):
    fullName: str
    firstName: str
    email: str
    phone: str
    skills: str

@app.post("/users")
def create_user(user: User):
    conn = get_db_connection()
    user_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO users (id, fullName, firstName, email, phone, skills) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, user.fullName, user.firstName, user.email, user.phone, user.skills)
    )
    conn.commit()
    conn.close()
    return {"id": user_id, **user.model_dump()}

@app.get("/users")
def get_users(skill: Optional[str] = Query(None)):
    conn = get_db_connection()
    if skill:
        # Search for the skill string anywhere inside the user's skills column
        search_term = f"%{skill}%"
        users = conn.execute("SELECT * FROM users WHERE skills LIKE ?", (search_term,)).fetchall()
    else:
        users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(row) for row in users]

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    conn.close()
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
