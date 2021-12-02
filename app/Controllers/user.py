from fastapi import APIRouter, Depends

from app.tools.jwt_tool import get_current_active_user
from app.Models import Users as UserModels
from app.Schemas import Users as UserSchemas
from app.tools.image_upload import image_upload
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
def upload_avatar(image: UserSchemas.UserAvatar, current_user: UserModels.User = Depends(get_current_active_user)):
    image_path = image_upload(image.image, 'avatars/', current_user.user_id)
    current_user.image = image_path
    response_object = {'user': current_user.user_dict(),
                       'success': True}
    return response_object
