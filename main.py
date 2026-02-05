from fastapi import Body, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from validators.signup_validate import validate_email, validate_password, validate_username
from utils.security import hash_password, verify_password
from auth import create_access_token, get_current_user

app = FastAPI()

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup", description="Signup with email, username, and password")

def signup( user: dict = Body(
        ...,
        example={
            "email": "user@example.com",
            "username": "exampleuser",
            "password": "securepassword123"
        }
    ), db: Session = Depends(get_db)):

    email = user.get("email", "")
    username = user.get("username", "")
    password = user.get("password", "")

    for error in [
        validate_email(email),
        validate_username(username),
        validate_password(password)
    ]:
        if error:
            raise HTTPException(status_code=400, detail=error)

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        email=email,
        username=username,
        hashed_password=hash_password(password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Signup successful"}



@app.post("/login", description="Login with email/username and password")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        (User.email == form_data.username) |
        (User.username == form_data.username)
    ).first()

    if not user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


    if not verify_password(form_data.password, user.hashed_password):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

   
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }



@app.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
   
