from db import Base, session
from sqlalchemy import Column, Integer, String
from auth import login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class User(Base, UserMixin):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  username = Column(String)
  password = Column(String, nullable=True)
  email = Column(String, nullable=True)
  githubId = Column(String, nullable=True)
  googleId = Column(String, nullable=True)
  images = relationship("Image", backref="users")

  def __repr__(self):
    return f"<User {self.username}>"

  @login_manager.user_loader
  def load_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user

class Image(Base):
  __tablename__ = "images"
  id = Column(Integer, primary_key=True)
  image_path = Column(String)
  user_id = Column(Integer, ForeignKey("users.id"))
