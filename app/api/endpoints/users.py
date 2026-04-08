from fastapi import APIRouter,Depends
from core import get_db,hash_password,verify_password
from sqlalchemy.orm import Session
from models import create_user,get_users,get_user_by_email,update_password
from schemas import UserRegister,UserLogin,EmailRequest,ResetPasswordRequest,VerifyOTPRequest
from services import save_otp,verify_otp,generate_otp,send_email

router=APIRouter()

@router.post("/register")
def add_user(user:UserRegister,db: Session = Depends(get_db)):
    create_user(db,user.name,user.email,hash_password(user.password))
    return {"message":"User registered successfully."}

@router.get("/users")
def getUsers(db=Depends(get_db)):
    return get_users(db)    

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(user.email, db)

    if not db_user:
        return {"error": "User not found"}
    
    if verify_password(user.password, db_user.password):
        return {"message": "Login successful","user":db_user}
    
    return {"error": "Invalid password"}


@router.post("/send-otp")
def send_otp(request: EmailRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_email(request.email, db)

    if not db_user:
        return {"error": "Enter registered email address."}
    
    otp = generate_otp()
    save_otp(request.email, otp)

    print(f"OTP for {request.email}: {otp}")
    send_email(request.email, otp)
    
    return {
        "message": "OTP sent successfully"
    }

@router.post("/verify-otp")
def verify_otp_route(request: VerifyOTPRequest):
    result = verify_otp(request.email, request.otp)

    if result == "OTP verified successfully":
        return {"message": result}
    
    return {"error":result}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    
    db_user = get_user_by_email(request.email, db)

    if not db_user:
        return {"error": "Enter registered email address."}

    hashed = hash_password(request.new_password)
    update_password(db_user.email, hashed, db)

    return {"message": "Password reset successfully"}