from pydantic import BaseModel,EmailStr,ConfigDict,Field
from datetime import datetime
from typing import Optional




"""For login schema to follow clients"""
class Users(BaseModel):
    email : EmailStr
    password : str

    
"""for api schema response """
class ResUser(BaseModel):
    email: EmailStr
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)


"""for login request to API"""
class UserLogin(BaseModel):
    email : EmailStr
    password: str

"""pydantic schema of the API for the clients or users to follow:"""

class PostCreate(BaseModel):
    title : str
    content : str
    published : bool = True

class CreatePost(PostCreate):
    pass


"""pydantic schema to control the response of the API :"""

class Post(PostCreate):
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime  # ISO timestamp string
    owner_id: int
    owner: ResUser

    model_config = ConfigDict(from_attributes=True)





class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., ge=0, le=1)
    