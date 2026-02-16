from fastapi import Body, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from validators.signup_validate import validate_email, validate_password, validate_username
from utils.security import hash_password, verify_password
from auth import create_access_token, get_current_user
from routes.tasks import router as task_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app.include_router(task_router)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup", description="Signup with email, username, password, and optional role")
def signup(
    user: dict = Body(
        ...,
        example={
            "email": "user@example.com",
            "username": "exampleuser",
            "password": "securepassword123",
            "role": "user"  # optional, only 'user' or 'manager'
        }
    ),
    db: Session = Depends(get_db)
):
    email = user.get("email", "")
    username = user.get("username", "")
    password = user.get("password", "")
    role = user.get("role", "user")  # default to 'user'

    # Validate role
    if role not in ["user", "manager"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid role. Only 'user' or 'manager' can be chosen."
        )

    # Validation checks
    for error in [
        validate_email(email),
        validate_username(username),
        validate_password(password)
    ]:
        if error:
            raise HTTPException(status_code=400, detail=error)

    # Check duplicates
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create user
    new_user = User(
        email=email,
        username=username,
        hashed_password=hash_password(password),
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"Signup successful as {role}"}



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
from fastapi import Depends

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import User

@app.post("/assign-manager")
def assign_manager_endpoint(
    user_username: str,
    manager_username: str,
    db: Session = Depends(get_db)
):
    # Find the user
    user = db.query(User).filter(
        User.username == user_username
    ).first()

    manager = db.query(User).filter(
        User.username == manager_username,
        User.role == "manager"
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not manager:
        raise HTTPException(
            status_code=404,
            detail="Manager not found or not a manager"
        )

    user.manager_id = manager.id
    db.commit()

    return {
        "message": f"{manager.username} assigned as manager to {user.username}"
    }



def create_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.role == "admin").first()
        if not admin:
            admin_user = User(
                email="admin@example.com",
                username="admin",
                hashed_password=hash_password("Admin@pas123"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created")
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    create_admin()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
   
