
from .. import models,schemas,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter 
from sqlalchemy.orm import Session
from ..DataBase import get_db
from typing import List,Optional




router = APIRouter(
    prefix = "/posts",
    tags= ['Posts']
)

"""retrieves the posts through get request by client:"""
@router.get("/",response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 5,skip: int = 0,search:Optional[str] = ""):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()
    return  posts
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()


"""creates post by clients through post requests and updates the DB:"""

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()

    new_post = models.Post(
        title=post.title,
        content=post.content,
        published=post.published,
        owner_id=current_user.id 
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


"""retrieves the posts through "id", if not in the DB returns the HTTP_Exception_code"""

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",
    # (id,))
    # post = cursor.fetchone()
    # post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
        # response.status_code =  status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return post 


"""deletes the post with "id" from the DB and returns the Status_code: HTTP_204_NO_CONTENT. 
 if the id not found in the DB, Returns the status_code: HTTP_404_NOT_FOUND:"""

@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def del_post(id: int,db: Session = Depends(get_db),
             current_user: models.User = Depends(oauth2.get_current_user)):    
    # cursor.execute("""DELETE FROM posts WHERE ID  = (%s) RETURNING * ;""",(id,))
    # del_post = cursor.fetchone()
    # conn.commit()

    post_to_del = db.query(models.Post).filter(models.Post.id == id)
    post = post_to_del.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(stutus_code = status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_to_del.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)
        # else:
        #     return f"there is no post with the id {id} in my_posts"


"""updates the posts through put request and if no ID found, 
returns status code: HTTP_404_NOT_FOUND:"""

@router.put("/{id}",response_model = schemas.PostOut)
def update_post(id: int, up_post: schemas.PostCreate,db: Session = Depends(get_db),
                current_user : models.User  = Depends(oauth2.get_current_user)):


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail = "not authorized to perform requested action") 
    
    post_query.update(up_post.dict(), synchronize_session = False)
    db.commit()
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return  post




    # cursor.execute("""UPDATE posts SET title  = %s,content  = %s,
    #                published = %s where id = %s returning *""",
    #                (post.title,post.content,post.published, (id,)))
    # updated_posts = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)



    """for postgre database conn with python"""
    # cursor.execute("""insert into posts("title","content","published") 
    #                values (%s,%s,%s) RETURNING * """, (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    # return  {"data": post_dict}
    # conn.commit()
    



"""for formated output use this return statement, instead of using above one"""
    # return {
    #     "id":new_post.id,
    #     "title": new_post.title,
    #     "content": new_post.content,
    #     "published": new_post.published,
    #     "created_at": new_post.created_at.isoformat()
    # }


"""retrieves the latest or recent post details:"""

# @router.get("/posts/recent/latest")
# def latest_post():
    # cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1 """)
    # latest = cursor.fetchone()
    # return latest



"""python implementation of DB"""

# cursor.execute("""create table posts("title" character varying, "content" character varying,"published" Boolean)""")
# cursor.execute("""insert into posts("title","content","published") 
#                values('first title','content of the first post',true)""")
# conn.commit()

# cursor.execute("""
#             ALTER TABLE posts
#             ADD COLUMN id SERIAL PRIMARY KEY;
#         """)

# cursor.execute("""ALTER TABLE posts
#                 ADD COLUMN created_at TIMESTAMP WITH TIME ZONE
#                 DEFAULT NOW()
#                 NOT NULL;""")

# cursor.execute("""ALTER TABLE users ADD COLUMN created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()""")
# conn.commit()
