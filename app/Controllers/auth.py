from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.tools.email_validation import check_email

from app.tools.get_database import get_db
from app.tools.access_token import create_access_token
from app.Schemas import Users as UserSchemas
from app.Crud import Users as UsersCrud

from app.tools.password_validation import password_check

auth_route = APIRouter()


@auth_route.post('/login',
                 response_model=UserSchemas.UserLoginResponse,
                 responses={
                     404: {
                            'description': 'User with this email not found',
                            'model': UserSchemas.FailResponse
                        },
                     400: {
                            'description': 'Wrong password',
                            'model': UserSchemas.FailResponse}
                        }
                 )
def auth(user: UserSchemas.UserLogin, db: Session = Depends(get_db)):
    db_user = UsersCrud.get_user_by_email(db, email=user.email)
    if not db_user:
        return JSONResponse(status_code=404, content={'success': False, 'message': 'User with this email not found'})
    if db_user.verify_password(user.password):
        access_token = create_access_token(data=db_user.user_dict())
        response_object = {'access_token': access_token, 'token_type': 'bearer', 'success': True}
        return response_object
    else:
        return JSONResponse(status_code=400, content={'success': False, 'message': 'Wrong password'})


@auth_route.post('/register',
                 response_model=UserSchemas.UserLoginResponse,
                 responses={
                     400: {
                            'description': 'Validation error',
                            'model': UserSchemas.FailResponse
                        },
                     409: {
                            'description': 'User already exists',
                            'model': UserSchemas.FailResponse}
                        }
                 )
def create_user(user: UserSchemas.UserCreate, db: Session = Depends(get_db)):
    db_user = UsersCrud.get_user_by_email(db, email=user.email)
    if db_user:
        return JSONResponse(status_code=409, content={'message': 'Email already registered', 'success': False})
    if user.password != user.repeat_password:
        return JSONResponse(status_code=400, content={'message': 'Password and Repeat password do not match',
                                                      'success': False})
    if password_check(user.password):
        return JSONResponse(status_code=400, content={'message': 'Password must be at least 8 characters'})
    if check_email(user.email):
        return JSONResponse(status_code=400, content={'message': 'Email is not valid', 'success': False})
    user_dict = UsersCrud.create_user(db=db, user=user)
    access_token = create_access_token(data=user_dict)
    response_object = {'user_dict': user_dict, 'access_token': access_token, 'token_type': 'bearer', 'success': True}
    return response_object
