from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config.config import config

engine = create_async_engine(config.DB_URL)
DBSession = async_sessionmaker(autocommit=False, bind=engine)


async def get_db():
    session = DBSession()

    try:
        yield session
    except Exception as error:
        print(error)
        await session.rollback()
        raise error
    finally:
        await session.close()
