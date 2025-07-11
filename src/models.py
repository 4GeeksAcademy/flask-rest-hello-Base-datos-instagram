from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Enum, Table,Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from enum import Enum as PyEnum

db = SQLAlchemy()

class Mediatype(PyEnum):
    png = "PNG"
    mp4 = "mp4"
class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)

    seguidor: Mapped[List["Seguidor"]] = relationship(secondary="user_seguidor", back_populates="user")



    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="author")
    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="user_posts")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "lastname": self.lastname,
            "firstname": self.firstname
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id), nullable=False)

    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="post_comments")
    user_posts: Mapped["User"] = relationship("User", back_populates="posts")
    media: Mapped["Media"] = relationship("Media", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"))

    author: Mapped["User"] = relationship(
            "User", back_populates="comments")
    post_comments: Mapped["Post"] = relationship(
            "Post", back_populates="comments")


    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
            # do not serialize the password, its a security breach
        }
user_seguidor = Table(
    "user_seguidor",
    db.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("seguidor_id", ForeignKey("seguidor.id"))
)



class Media(db.Model):
    __tablename__ = "media"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Mediatype] = mapped_column(Enum(Mediatype,name="mediatype_enum"))
    url: Mapped[str] = mapped_column(String,nullable=False)
    post_id: Mapped[int] = mapped_column(Integer,ForeignKey("post.id"),nullable=False)

    post: Mapped["Post"] = relationship("Post",back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id,
            # do not serialize the password, its a security breach
        }
class Seguidor(db.Model):
    __tablename__ = "seguidor"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)

    user: Mapped[List["User"]] = relationship(secondary="user_seguidor", back_populates="seguidor")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "lastname": self.lastname,
            "firstname": self.firstname
            # do not serialize the password, its a security breach
        }

