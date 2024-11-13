from fastapi import FastAPI
from httpx import post
from pydantic import BaseModel
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
app = FastAPI()
while True:
    
    try:
        connection = psycopg2.connect(user="kweku",
                                  password="black@124",
                                  host="academy.iridislabs.dev",
                                
                                  database="b_blaq", cursor_factory=RealDictCursor) 
        cursor = connection.cursor()
        print("Connected to PostgreSQL")
        break
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
        time.sleep(2)

##GET ALL POSTS
@app.get("/")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

##CREATE POST
@app.post("/posts", status_code=201)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (Title, content, published) VALUES (%s, %s, %s)RETURNING * """, 
                   
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connection.commit()
    return {"data": new_post}

##GET POST BY ID
@app.get("/posts/{id}", status_code=200)
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    return {"data": post}

##UPDATE POST
@app.put("/posts/{id}", status_code=200)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    connection.commit()
    return {"data": updated_post}

##DELETE POST
@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    connection.commit()
    return {"data": deleted_post}

