from flask_user import UserMixin
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from configuration.persistence import Base

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    # User authentication information
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False, server_default='')
    reset_password_token = Column(String(100), nullable=False, server_default='')

    # User email information
    email = Column(String(255), nullable=True, unique=True)
    confirmed_at = Column(DateTime())

    # User information
    active = Column('is_active', Boolean(), nullable=False, server_default='0')
    first_name = Column(String(100), nullable=False, server_default='')
    last_name = Column(String(100), nullable=False, server_default='')

    team_id = Column(Integer, ForeignKey("team.id"))
    team = relationship("Team")

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True)

class UserRoles(Base):
    __tablename__ = 'user_role'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('role.id', ondelete='CASCADE'))