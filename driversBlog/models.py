from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean, Table
from sqlalchemy.orm import relationship
from driversBlog import Base


tags_for_posts_table = Table(
    "tags_for_posts",
    Base.metadata,
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True)
)


class WritersLevel(Base):
    __tablename__ = "writerlevels"
    id = Column(Integer, primary_key=True)
    level_name = Column(String(35), nullable=False, unique=True)

    user = relationship("User", back_populates="level")

    def __str__(self):
        return str(self.level_name)

    def __repr__(self):
        return str(self)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    nickname = Column(String(20), nullable=False)
    fullname = Column(String(50), nullable=False)
    level_id = Column(Integer, ForeignKey(WritersLevel.id), nullable=False, default=0, server_default="0")
    date_registration = Column(DateTime, nullable=False, default=func.now())
    # datetime.utcnow or func.now()
    active = Column(Boolean, nullable=False, default=True, server_default="1")

    posts = relationship("Post", back_populates="user")
    level = relationship(WritersLevel, back_populates="user")

    def __str__(self):
        return str(self.nickname)

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    post_title = Column(String(80), nullable=False, unique=True)
    post_text = Column(Text, nullable=False)
    date_creation = Column(DateTime, nullable=False, default=func.now())
    is_published = Column(Boolean, nullable=False, default=False, server_default="0")

    user = relationship(User, back_populates="posts")
    tags = relationship("Tag", secondary=tags_for_posts_table, back_populates="posts")

    def __str__(self):
        return str(self.post_title)

    def __repr__(self):
        return str(self)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(20), nullable=False, unique=True)

    posts = relationship("Post", secondary=tags_for_posts_table, back_populates="tags")

    def __str__(self):
        return str(self.tag_name)

    def __repr__(self):
        return str(self)
