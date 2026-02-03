from fastapi import Body, HTTPException, FastAPI
from validators.signup_validate import validate_email, validate_password, validate_username
from users_db import users
from passlib.context import CryptContext 
import hashlib
import base64

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash_input(password: str) -> str:
    # 1. Hash with SHA-256 to get a fixed-length output
    sha_hash = hashlib.sha256(password.encode("utf-8")).digest()
    # 2. Base64 encode it so it's a string Bcrypt can handle
    return base64.b64encode(sha_hash).decode("ascii")

@app.post("/signup", description="Provide email, username, and password to signup")
async def signup(
    user: dict = Body(..., example={"email": "test@gmail.com","username":"debs_01","password":"Pass123!"})
):

    email=user.get("email","")
    username=user.get("username","")
    password=user.get("password","")

    email_error = validate_email(email)
    password_error = validate_password(password)
    username_error = validate_username(username)

    for error in [email_error, username_error, password_error]:
        if error:
            raise HTTPException(status_code=400, detail=error)

    
    for u in users.values():
        if u["email"] == email:
            raise HTTPException(status_code=400, detail="Email already exists")
        if u["username"] == username:
            raise HTTPException(status_code=400, detail="Username already exists")

    prep_password = get_password_hash_input(password)
    hashed_password = pwd_context.hash(prep_password)

    users[username]={
  "email": email,
  "username": username,
  "password": hashed_password
}
    
    return {"message": "Signup successful"}


@app.post("/login", description="Provide email/username and password to login")
async def login(
    user: dict = Body(
        ...,
        example={
            "login": "debs_01 or test@gmail.com",
            "password": "Pass123!"
        }
    )
):
    login_input=user.get("login","")
    password_input=user.get("password","")

    if not login_input:
        raise HTTPException(status_code=400, detail="Email/Username is required")
    if not password_input:
        raise HTTPException(status_code=400, detail="Password is required")

    found_user = None
    for u in users.values():
        if u["email"] == login_input or u["username"] == login_input:
            found_user = u
            break

    if not found_user:
        raise HTTPException(status_code=400, detail="Invalid email/username or password")

    prep_input = get_password_hash_input(password_input)
    if not pwd_context.verify(prep_input, found_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email/username or password")

    return {"message": "Login successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
   
