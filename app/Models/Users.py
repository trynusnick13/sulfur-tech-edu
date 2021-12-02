from werkzeug.security import generate_password_hash, check_password_hash

from app.Config.database import Base

from sqlalchemy import Boolean, Column, Integer, String


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean)
    registration_date = Column(String)
    image = Column(String, default=None)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password_given):
        return check_password_hash(self.hashed_password, password_given)

    def user_dict(self):
        user = {'user_id': self.user_id,
                'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'disabled': self.disabled,
                'registration_date': self.registration_date,
                'image': self.image}
        return user
