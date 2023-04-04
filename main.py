from fastapi import FastAPI,Depends
from numpy import append
import schemas,models
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from database import engine
from typing import List
from fastapi import status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import status,HTTPException
from hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm
import Token,oauth2
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from jose import JWTError,jwt
from typing import Optional
import schemas
import Token

models.Base.metadata.create_all(engine)

app=FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3000/Barrowedbooks",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
@app.post('/issuedbooks',response_model=schemas.ShowBook,tags = ['book'])
def create_book(request:schemas.Book,db:Session=Depends(get_db)):
    new_book=models.Book(Accessnumber=request.Accessnumber,Username=request.Username,Title=request.Title,Author=request.Author,Subject=request.Subject,KeyWord=request.KeyWord,bookcategory=request.bookcategory)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    db.close()
    return new_book

@app.post('/login',tags=['members'])
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    member=db.query(models.Book).filter(models.Book.email==form_data.username).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    if not Hash.verify(member.password,form_data.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    access_token = Token.create_access_token(data={"sub":member.email})
    return {"access_token":access_token,"token_type":"bearer"}

@app.post("/decoder", tags=['decoder'])
def verify_token(token:str, db:Session=Depends(get_db)):
        payload = jwt.decode(token, Token.SECRET_KEY, algorithms=[Token.ALGORITHM])
        email: str = payload.get("sub")  
        if email is None:
            raise HTTPException(status_code=404,detail="token not decoded")
        token_data = schemas.TokenData(email=email)
        return db.query(models.Member).filter(models.Member.email==email).first()
    

@app.delete('/issuedbooks/{Accessnumber}/',status_code=status.HTTP_404_NOT_FOUND,tags = ['book'])
def member(Accessnumber,db:Session=Depends(get_db)):
    db.query(models.Book).filter(models.Book.Accessnumber==Accessnumber).delete(synchronize_session=False)
    db.commit()
    return 'DONE'

@app.get('/issuedbooks/',response_model=list[schemas.ShowBook],tags=['book'])
def get_book(db:Session=Depends(get_db)):
    book=db.query(models.Book).all()
    return book


@app.get('/issuedbooks/{Username}',tags=['book'])
def get_book(Username:str,db:Session=Depends(get_db)):
    book=db.query(models.Book).filter(models.Book.Username==Username).all()
    return book

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=True)
