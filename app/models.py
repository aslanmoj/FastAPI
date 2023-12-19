from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP ,text
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = "posts" ## this shows the table name

    id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id",
                                          ondelete="CASCADE"),nullable=False)
    owner = relationship("User")
    # created_at = Column(DateTime(timezone = True),
    #                 nullable= False, server_default='now()')
class User(Base):
    __tablename__ = "users" ## this shows the table name
    id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    # created_at = Column(TIMESTAMP(timezone = True),
    #                     nullable= False, server_default=text('now()'))
    

