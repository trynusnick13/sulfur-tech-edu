from app.Config.database import Base
from sqlalchemy import Boolean, Column, Integer, String, Float, Text, ForeignKey


class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    course_price = Column(Float, default=0.0)
    course_description = Column(Text)
    create_time = Column(String)
    rating = Column(Float, default=0.0)
    image = Column(String)
    creator_id = Column(Integer, ForeignKey('users.user_id'))

    def course_dict(self):
        course = {'course_id': self.course_id,
                  'course_name': self.course_name,
                  'course_price': self.course_price,
                  'course_description': self.course_description,
                  'create_time': self.create_time,
                  'rating': self.rating,
                  'creator_id': self.creator_id,
                  'image': self.image}
        return course


class CourseSubscriptions(Base):
    __tablename__ = 'course_subscription'

    course_fk_id = Column(Integer, ForeignKey('courses.course_id'), primary_key=True)
    user_fk_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)


class CourseRates(Base):
    __tablename__ = 'course_ratings'

    course_fk_id = Column(Integer, ForeignKey('courses.course_id'), primary_key=True)
    user_fk_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    rate = Column(Integer)