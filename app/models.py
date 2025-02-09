from sqlalchemy import Integer, String, Boolean, ForeignKey, Column
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))