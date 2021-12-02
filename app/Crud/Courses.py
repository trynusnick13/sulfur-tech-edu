from typing import Optional

import paginate_sqlalchemy
import pytz
import datetime as dt

from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from ..Schemas import Courses as CoursesSchemas
from ..Models import Courses as CoursesModel
from ..Models import Users as UsersModel
from ..tools.image_upload import image_upload, image_remove


def create_course(db: Session, course: CoursesSchemas.CourseCreate, creator_id: int):
    db_course = CoursesModel.Course(
        course_name=course.course_name,
        course_price=course.course_price,
        course_description=course.course_description,
        create_time=dt.datetime.now(pytz.utc).isoformat(timespec='milliseconds'),
        creator_id=creator_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    if course.image is not None:
        image_path = image_upload(course.image, 'course_images/', db_course.course_id)
        db_course.image = image_path

    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_course_by_id(db: Session, course_id: int):
    return db.query(CoursesModel.Course).get(course_id)


def get_all_courses(db: Session,
                    page: Optional[int],
                    per_page: Optional[int],
                    name: Optional[str],
                    minimal_rating: Optional[int],
                    min_price: Optional[float],
                    max_price: Optional[float]):
    array = db.query(CoursesModel.Course).\
        filter(CoursesModel.Course.course_name.startswith(name),
               CoursesModel.Course.rating >= minimal_rating,
               CoursesModel.Course.course_price >= min_price,
               CoursesModel.Course.course_price <= max_price).\
        order_by(desc(CoursesModel.Course.create_time))
    array_page = paginate_sqlalchemy.SqlalchemyOrmPage(array,
                                                       page=page,
                                                       items_per_page=per_page,
                                                       db_session=db)
    pagination_info = {'items_total': array_page.item_count,
                       'page_count': array_page.page_count,
                       'courses': array_page}
    return pagination_info


def get_courses_by_creator_id(db: Session,
                              creator_id: int,
                              page: Optional[int],
                              per_page: Optional[int]):
    array = db.query(CoursesModel.Course). \
        filter_by(creator_id=creator_id). \
        order_by(desc(CoursesModel.Course.create_time))
    array_page = paginate_sqlalchemy.SqlalchemyOrmPage(array,
                                                       page=page,
                                                       items_per_page=per_page,
                                                       db_session=db)
    pagination_info = {'items_total': array_page.item_count,
                       'page_count': array_page.page_count,
                       'courses': array_page}
    return pagination_info


# TODO: add deletion all subscriptions and ratings with course delete
def delete_course(db: Session,
                  user_id,
                  course_id):
    db_course = db.query(CoursesModel.Course).get(course_id)
    if db_course is None:
        return None
    if db_course.creator_id != user_id:
        return False

    # rates remove
    db_course_rates = db.query(CoursesModel.CourseRates).filter_by(course_fk_id=course_id)
    for rate in db_course_rates:
        db.delete(rate)

    # Subscription remove
    db_course_subs = db.query(CoursesModel.CourseSubscriptions).filter_by(course_fk_id=course_id)
    for sub in db_course_subs:
        db.delete(sub)

    db.delete(db_course)
    db.commit()
    image_remove(db_course.image)
    return True


def update_course(db: Session,
                  user_id,
                  course_id,
                  course):
    db_course = db.query(CoursesModel.Course).get(course_id)
    if db_course is None:
        return None
    if db_course.creator_id != user_id:
        return False

    if course.image is not None:
        image_path = image_upload(course.image, 'course_images/', db_course.course_id)
        db_course.image = image_path
    if course.course_name is not None:
        db_course.course_name = course.course_name
    if course.course_price is not None:
        db_course.course_price = course.course_price
    if course.course_description is not None:
        db_course.course_description = course.course_description
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def subscribe_course(db: Session, user_id, course_id):
    db_subscription = db.query(CoursesModel.CourseSubscriptions).get((course_id, user_id))
    if db_subscription is None:
        db_subscription = CoursesModel.CourseSubscriptions(course_fk_id=course_id, user_fk_id=user_id)
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return True
    return False


def unsubscribe_course(db: Session, user_id, course_id):
    db_subscription = db.query(CoursesModel.CourseSubscriptions).get((course_id, user_id))
    if db_subscription is not None:
        db.delete(db_subscription)
        db.commit()
        return True
    return False


def get_my_courses(db: Session, user_id, page: int, per_page: int):
    courses_ids = [id.course_fk_id for id in db.query(CoursesModel.CourseSubscriptions).
        with_entities(CoursesModel.CourseSubscriptions.course_fk_id).
        filter_by(user_fk_id=user_id).distinct()]
    pk = CoursesModel.Course.__mapper__.primary_key[0]
    courses = db.query(CoursesModel.Course).filter(pk.in_(courses_ids))
    courses_pages = paginate_sqlalchemy.SqlalchemyOrmPage(courses,
                                                          page=page,
                                                          items_per_page=per_page,
                                                          db_session=db)
    pagination_info = {'items_total': courses_pages.item_count,
                       'page_count': courses_pages.page_count,
                       'courses': courses_pages}
    return pagination_info


def get_course_students(db: Session, course_id, current_user_id, page: int, per_page: int):
    course = get_course_by_id(db=db, course_id=course_id)
    if course is None:
        return False
    if course.creator_id != current_user_id:
        return True
    students_ids = [id.user_fk_id for id in db.query(CoursesModel.CourseSubscriptions).
        with_entities(CoursesModel.CourseSubscriptions.user_fk_id).
        filter_by(course_fk_id=course_id).distinct()]
    pk = UsersModel.User.__mapper__.primary_key[0]
    users = db.query(UsersModel.User).filter(pk.in_(students_ids))
    users_pages = paginate_sqlalchemy.SqlalchemyOrmPage(users,
                                                        page=page,
                                                        items_per_page=per_page,
                                                        db_session=db)
    users_array = []
    for user in users_pages:
        users_array.append(user.user_dict())
    pagination_info = {'items_total': users_pages.item_count,
                       'page_count': users_pages.page_count,
                       'users': users_array}
    return pagination_info


def rate_course(db: Session, course_id, current_user_id, rate):
    course = get_course_by_id(db=db, course_id=course_id)
    if course is None:
        return False
    record = db.query(CoursesModel.CourseRates).filter_by(course_fk_id=course_id,
                                                          user_fk_id=current_user_id).first()
    if record is None:
        record = CoursesModel.CourseRates(course_fk_id=course_id,
                                          user_fk_id=current_user_id,
                                          rate=rate)
    else:
        record.rate = rate
    db.add(record)
    db.commit()
    db.refresh(record)

    rates_sum = db.query(CoursesModel.CourseRates).with_entities(
        func.sum(CoursesModel.CourseRates.rate).label('rates_total')
    ).filter_by(course_fk_id=course_id).scalar() or 0

    rates_count = db.query(CoursesModel.CourseRates).filter_by(course_fk_id=course_id).count()
    course.rate = rates_sum / rates_count
    db.add(course)
    db.commit()
    db.refresh(course)
    return True
