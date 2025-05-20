import unittest
from unittest.mock import AsyncMock, MagicMock
import unittest
import uuid
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import src.repository.user as user_repository
from src.entity import User

test_create_user = {
    'email': 'test@gmail.com',
    'password': '12345678'
}

class TestContactRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=str(uuid.uuid4()), **test_create_user)

    async def test_create_user(self):
        user = User(**test_create_user, id=str(uuid.uuid4()))

        self.session.add = MagicMock()
        self.session.commit.return_value = AsyncMock()
        self.session.refresh.return_value = AsyncMock()

        result = await user_repository.create_user(
            test_create_user, db=self.session
        )

        self.assertEqual(result.email, user.email)
        self.assertEqual(result.password, user.password)

    async def test_get_user(self):
        self.session.execute = AsyncMock()
        self.session.execute.return_value = MagicMock()
        self.session.execute.return_value.scalar_one_or_none.return_value = self.user

        result = await user_repository.get_user(
            id=self.user.id, db=self.session
        )

        self.assertEqual(result, self.user)
        self.session.execute.assert_awaited()


    async def test_get_user_by_email(self):
        self.session.execute = AsyncMock()
        self.session.execute.return_value = MagicMock()
        self.session.execute.return_value.scalar_one_or_none.return_value = self.user

        result = await user_repository.get_user_by_email(
            email=self.user.email, db=self.session
        )

        self.assertEqual(result, self.user)
        self.session.execute.assert_awaited()

    async def test_confirm_user(self):
        self.session.add = MagicMock()
        self.session.commit.return_value = AsyncMock()
        self.session.refresh.return_value = AsyncMock()

        result = await user_repository.confirm_user(
            user=self.user, db=self.session
        )

        self.assertEqual(result.is_confirmed, True)

    async def test_set_avatar(self):
        self.session.execute = AsyncMock()
        self.session.execute.return_value = MagicMock()
        self.session.execute.return_value.scalar_one_or_none.return_value = self.user

        self.session.add = MagicMock()
        self.session.commit.return_value = AsyncMock()
        self.session.refresh.return_value = AsyncMock()

        avatar = 'new_avatar'

        result = await user_repository.set_avatar(
            id=self.user.id, avatar=avatar, db=self.session
        )

        self.assertEqual(result.avatar, avatar)

if __name__ == '__main__':
    unittest.main()