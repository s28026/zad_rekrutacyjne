from sqlalchemy import Column, Integer, String, select
from ..services.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    @classmethod
    async def add(cls, session, title: str, content: str):
        message = cls(title=title, content=content)
        session.add(message)
        await session.commit()

    @classmethod
    async def all(cls, session):
        result = await session.execute(select(cls))
        return result.scalars().all()
