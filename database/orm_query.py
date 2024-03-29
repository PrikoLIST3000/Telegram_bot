from sqlalchemy import select, update, delete, column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import FromClause

from database.models import User


async def orm_add_user(session: AsyncSession, user_id: int, full_name: str, username: str):
    obj = User(
        id=user_id,
        full_name=full_name,
        username=username
    )
    session.add(obj)
    await session.commit()


async def orm_get_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_user_quiz_state(session: AsyncSession, user_id: int):
    query = update(User).where(User.id == user_id).values(complete_quiz=True)
    await session.execute(query)
    await session.commit()


async def orm_is_quiz_completed(session: AsyncSession, user_id: int) -> bool:
    query = select(User.complete_quiz).where(User.complete_quiz == True, User.id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_delete_user(session: AsyncSession, user_id: int):
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()
