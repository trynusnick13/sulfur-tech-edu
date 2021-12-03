from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.tools.get_database import get_db
from app.tools.jwt_tool import get_current_active_user
from app.Models import Users as UserModels
from app.Schemas import Users as UserSchemas
from app.Crud import Users as UsersCrud

user_route = APIRouter()


@user_route.get('/profile',
                responses={
                    200: {
                            'description': 'User requested by self',
                            'content': {
                                'application/json': {
                                    'example': {'success': True,
                                                'user': {
                                                        'user_id': 1,
                                                        'email': 'something@smt.com',
                                                        'first_name': 'Name',
                                                        'last_name': 'Surname',
                                                        'disabled': False,
                                                        'image': 'images/1.png',
                                                        'registration_date': '2005-08-09T18:31:42.000+02:00'
                                                    }
                                                }
                                    }
                                },
                            },
                })
def read_users_me(current_user: UserModels.User = Depends(get_current_active_user)):
    return {'user': current_user.user_dict(), 'success': True}


@user_route.put('/avatar-upload',
                responses={
                    200: {
                        'description': 'Image upload successfully',
                        'content': {
                            'application/json': {
                                'example': {'success': True,
                                            'user': {
                                                    'user_id': 1,
                                                    'email': 'something@smt.com',
                                                    'first_name': 'Name',
                                                    'last_name': 'Surname',
                                                    'disabled': False,
                                                    'image': 'images/1.png',
                                                    'registration_date': '2005-08-09T18:31:42.000+02:00'
                                                    }
                                            }
                            }
                        }
                    }
                })
def upload_avatar(image: UserSchemas.UserAvatar, current_user: UserModels.User = Depends(get_current_active_user),
                  db: Session = Depends(get_db)):
    response = UsersCrud.update_user_image(db=db, image=image.image, user_id=current_user.user_id)
    response_object = {'user': response,
                       'success': True}
    return response_object
