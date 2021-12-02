from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from typing import Optional

from sqlalchemy.orm import Session

from app.tools.get_database import get_db

from app.Schemas import Courses as CoursesSchemas
from app.Crud import Courses as CoursesCrud
from app.Models import Users as UserModels


from app.tools.jwt_tool import get_current_active_user

course_route = APIRouter()


@course_route.post('/create',
                   responses={
                       200: {
                           'description': 'Course created',
                           'content': {
                               'application/json': {
                                   'example': {'success': True,
                                               'course': {
                                                  'course_id': 1,
                                                  'course_name': 'Name',
                                                  'course_price': 10.0,
                                                  'course_description': 'Some Description bla bla',
                                                  'create_time': '2005-08-09T18:31:42.000+02:00',
                                                  'rating': 0,
                                                  'creator_id': 1,
                                                  'image': 'images/1.png'
                                                            }
                                               }
                               }
                           },
                       },
                       400: {
                           'description': 'Validation error',
                           'model': CoursesSchemas.FailResponse
                       }
                   })
def create_course(course: CoursesSchemas.CourseCreate,
                  db: Session = Depends(get_db),
                  current_user: UserModels.User = Depends(get_current_active_user)):
    if course.course_name == '':
        return JSONResponse(status_code=400, content={'success': False, 'message': 'Name cannot be an empty string'})
    course_db = CoursesCrud.create_course(db=db, course=course, creator_id=current_user.user_id)
    response_object = {'course': course_db, 'success': True}
    return response_object


@course_route.get('/get-id/{course_id}',
                  responses={
                      200: {
                          'description': 'Course show',
                          'content': {
                              'application/json': {
                                  'example': {'success': True,
                                              'course': {
                                                  'course_id': 1,
                                                  'course_name': 'Name',
                                                  'course_price': 10.0,
                                                  'course_description': 'Some Description bla bla',
                                                  'create_time': '2005-08-09T18:31:42.000+02:00',
                                                  'rating': 0,
                                                  'creator_id': 1,
                                                  'image': 'images/1.png'
                                              }
                                              }
                              }
                          },
                      },
                      404: {
                          'description': 'Validation error',
                          'model': CoursesSchemas.FailResponse
                      }
                  })
def show_course_by_id(course_id: int, db: Session = Depends(get_db)):
    course_db = CoursesCrud.get_course_by_id(db=db, course_id=course_id)
    if course_db is None:
        return JSONResponse(status_code=404, content={'success': False, 'message': 'Course with this ID not found'})
    response_object = {'course': course_db, 'success': True}
    return response_object


@course_route.get('/all',
                  responses={
                      200: {
                          'description': 'Courses show',
                          'content': {
                              'application/json': {
                                  'example': {
                                      'success': True,
                                      'items_total': 10,
                                      'page_count': 1,
                                      'courses': [
                                          {
                                              'course_id': 1,
                                              'course_name': 'Name',
                                              'course_price': 10.0,
                                              'course_description': 'Some Description bla bla',
                                              'create_time': '2005-08-09T18:31:42.000+02:00',
                                              'rating': 0,
                                              'creator_id': 1,
                                              'image': 'images/1.png'
                                            },
                                          {
                                              'course_id': 2,
                                              'course_name': 'Name',
                                              'course_price': 10.0,
                                              'course_description': 'Some Description bla bla',
                                              'create_time': '2005-08-09T18:31:42.000+02:00',
                                              'rating': 0,
                                              'creator_id': 1,
                                              'image': 'images/1.png'
                                          }
                                      ]
                                  }
                              }
                          },
                      }
                  })
def show_all_courses(name: Optional[str] = '',
                     minimal_rating: Optional[int] = 0,
                     min_price: Optional[float] = 0,
                     max_price: Optional[float] = 999999,
                     page: Optional[int] = 1,
                     per_page: Optional[int] = 20,
                     db: Session = Depends(get_db)):
    response_object = CoursesCrud.get_all_courses(db, page, per_page, name, minimal_rating, min_price, max_price)
    response_object.update({'success': True})
    return response_object


@course_route.get('/get-by-creator-id/{creator_id}',
                  responses={
                      200: {
                          'description': 'Course show',
                          'content': {
                              'application/json': {
                                  'example': {
                                      'success': True,
                                      'course': {
                                          'course_id': 1,
                                          'course_name': 'Name',
                                          'course_price': 10.0,
                                          'course_description': 'Some Description bla bla',
                                          'create_time': '2005-08-09T18:31:42.000+02:00',
                                          'rating': 0,
                                          'creator_id': 1,
                                          'image': 'images/1.png'
                                      }
                                  }
                              }
                          },
                      },
                      404: {
                          'description': 'Validation error',
                          'model': CoursesSchemas.FailResponse
                      }
                  })
def show_by_creator_id(creator_id: int,
                       page: Optional[int] = 1,
                       per_page: Optional[int] = 20,
                       db: Session = Depends(get_db)):
    response_object = CoursesCrud.get_courses_by_creator_id(db, creator_id=creator_id, page=page, per_page=per_page)
    response_object.update({'success': True})
    return response_object


@course_route.delete('/delete/{course_id}',
                     responses={
                         400: {
                           'description': 'User did not create this course',
                           'model': CoursesSchemas.FailResponse
                         },
                         200: {
                           'description': 'Course deleted',
                           'model': CoursesSchemas.FailResponse                 # Not actually fail but
                         },                                                     # structure is same
                         404: {
                           'description': 'Course Not Found',
                           'model': CoursesSchemas.FailResponse
                         }
                     })
def delete_course(course_id: int,
                  db: Session = Depends(get_db),
                  current_user: UserModels.User = Depends(get_current_active_user)):
    result = CoursesCrud.delete_course(db, current_user.user_id, course_id)
    if result is None:
        return JSONResponse(status_code=404, content={'success': False, 'message': 'Course with this ID not found'})
    if result is False:
        return JSONResponse(status_code=400, content={'success': False, 'message': 'User did not create this course'})
    return JSONResponse(status_code=200, content={'success': True, 'message': 'Course deleted'})


@course_route.patch('/update/{course_id}',
                    responses={
                        400: {
                           'description': 'User did not create this course',
                           'model': CoursesSchemas.FailResponse
                        },
                        404: {
                           'description': 'Course Not Found',
                           'model': CoursesSchemas.FailResponse
                        },
                        200: {
                          'description': 'Course show',
                          'content': {
                              'application/json': {
                                  'example': {
                                      'success': True,
                                      'course': {
                                          'course_id': 1,
                                          'course_name': 'Name',
                                          'course_price': 10.0,
                                          'course_description': 'Some Description bla bla',
                                          'create_time': '2005-08-09T18:31:42.000+02:00',
                                          'rating': 0,
                                          'creator_id': 1,
                                          'image': 'images/1.png'
                                      }
                                  }
                              }
                          },
                        },
                    })
def update_course(course_id: int,
                  course: CoursesSchemas.CourseUpdate,
                  db: Session = Depends(get_db),
                  current_user: UserModels.User = Depends(get_current_active_user)):
    result = CoursesCrud.update_course(db=db, user_id=current_user.user_id, course_id=course_id, course=course)
    if result is None:
        return JSONResponse(status_code=404, content={'success': False, 'message': 'Course with this ID not found'})
    if result is False:
        return JSONResponse(status_code=400, content={'success': False, 'message': 'User did not create this course'})
    response_object = {'success': True, 'course': result}
    return response_object


@course_route.post('/subscribe',
                   responses={
                       409: {
                           'description': 'Already subscribed',
                           'model': CoursesSchemas.FailResponse
                       },
                       200: {
                           'description': 'Subscribed',
                           'model': CoursesSchemas.FailResponse  # Not actually fail but
                       },
                   })
def subscribe_course(course_id: CoursesSchemas.CourseSubscribe,
                     db: Session = Depends(get_db),
                     current_user: UserModels.User = Depends(get_current_active_user)):
    result = CoursesCrud.subscribe_course(db=db, course_id=course_id.course_id, user_id=current_user.user_id)
    if result is False:
        return JSONResponse(status_code=409, content={'success': False, 'message': 'Already subscribed'})
    return JSONResponse(status_code=200, content={'success': True, 'message': 'Subscribed'})


@course_route.delete('/unsubscribe',
                     responses={
                       404: {
                           'description': 'Not subscribed',
                           'model': CoursesSchemas.FailResponse
                       },
                       200: {
                           'description': 'Unsubscribed',
                           'model': CoursesSchemas.FailResponse  # Not actually fail but
                       },
                   })
def subscribe_course(course_id: CoursesSchemas.CourseSubscribe,
                     db: Session = Depends(get_db),
                     current_user: UserModels.User = Depends(get_current_active_user)):
    result = CoursesCrud.unsubscribe_course(db=db, course_id=course_id.course_id, user_id=current_user.user_id)
    if result is False:
        return JSONResponse(status_code=404, content={'success': False, 'message': 'Not subscribed'})
    return JSONResponse(status_code=200, content={'success': True, 'message': 'Unsubscribed'})


@course_route.get('/my-subscribed',
                  responses={
                        200: {
                          'description': 'Courses show',
                          'content': {
                              'application/json': {
                                  'example': {
                                      'success': True,
                                      'items_total': 10,
                                      'page_count': 1,
                                      'courses': [
                                          {
                                              'course_id': 1,
                                              'course_name': 'Name',
                                              'course_price': 10.0,
                                              'course_description': 'Some Description bla bla',
                                              'create_time': '2005-08-09T18:31:42.000+02:00',
                                              'rating': 0,
                                              'creator_id': 1,
                                              'image': 'images/1.png'
                                          },
                                          {
                                              'course_id': 2,
                                              'course_name': 'Name',
                                              'course_price': 10.0,
                                              'course_description': 'Some Description bla bla',
                                              'create_time': '2005-08-09T18:31:42.000+02:00',
                                              'rating': 0,
                                              'creator_id': 1,
                                              'image': 'images/1.png'
                                          }
                                      ]
                                  }
                              }
                          },
                      }
                  })
def get_my_courses(page: Optional[int] = 1,
                   per_page: Optional[int] = 20,
                   db: Session = Depends(get_db),
                   current_user: UserModels.User = Depends(get_current_active_user)):
    response_object = CoursesCrud.get_my_courses(db=db, user_id=current_user.user_id, page=page, per_page=per_page)
    response_object.update({'success': True})
    return response_object


@course_route.get('/students/{course_id}',
                  responses={
                        400: {
                           'description': 'User did not create this course',
                           'model': CoursesSchemas.FailResponse
                        },
                        404: {
                           'description': 'Course Not Found',
                           'model': CoursesSchemas.FailResponse
                        },
                        200: {
                          'description': 'Image upload successfully',
                          'content': {
                              'application/json': {
                                  'example': {'success': True,
                                              'items_total': 1,
                                              'page_count': 1,
                                              'users': [
                                                  {
                                                      'user_id': 1,
                                                      'email': 'something@smt.com',
                                                      'first_name': 'Name',
                                                      'last_name': 'Surname',
                                                      'disabled': False,
                                                      'image': 'images/1.png',
                                                      'registration_date': '2005-08-09T18:31:42.000+02:00'
                                                  }
                                                ]
                                              }
                              }
                          }
                        }
                  })
def get_course_students(course_id: int,
                        page: Optional[int] = 1,
                        per_page: Optional[int] = 20,
                        db: Session = Depends(get_db),
                        current_user: UserModels.User = Depends(get_current_active_user)):
    users = CoursesCrud.get_course_students(db=db, course_id=course_id, current_user_id=current_user.user_id,
                                            page=page, per_page=per_page)
    if users is False:
        return JSONResponse(status_code=404, content={'success': False, 'message': 'Course with this ID not found'})
    if users is True:
        return JSONResponse(status_code=400, content={'success': False, 'message': 'User did not create this course'})
    users.update({'success': True})
    return users


@course_route.post('/rate/{course_id}',
                   responses={
                       404: {
                           'description': 'Course Not Found',
                           'model': CoursesSchemas.FailResponse},
                       200: {
                           'description': 'Course rated',
                           'model': CoursesSchemas.FailResponse}
                   })
def rate_course(course_id: int, rate: CoursesSchemas.CourseRate,
                db: Session = Depends(get_db),
                current_user: UserModels.User = Depends(get_current_active_user)):
    rate = CoursesCrud.rate_course(db=db, course_id=course_id, current_user_id=current_user.user_id, rate=rate.rate)
    if rate is False:
        return JSONResponse(status_code=404, content={'success': False, 'message': 'Course with this ID not found'})
    return JSONResponse(status_code=200, content={'success': True, 'message': 'Course rated'})