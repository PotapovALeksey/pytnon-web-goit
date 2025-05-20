import datetime
import unittest
from unittest.mock import AsyncMock, MagicMock
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity import Contact, User
import src.repository.contact as contact_repository
from src.schemas.contacts import ContactBaseSchema


test_contact = {
    'name': 'test',
    'surname': 'test',
    'phone': 'test',
    'email': 'test@gmail.com',
    'birthday': datetime.date.today()
}

class TestContactRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=str(uuid.uuid4()))

    async def test_get_found_contact(self):
        contact = Contact(id=1, user_id=str(self.user.id))

        self.session.execute = AsyncMock()
        self.session.execute.return_value = MagicMock()
        self.session.execute.return_value.scalar_one_or_none.return_value = contact

        result = await contact_repository.get_contact(
            contact_id=contact.id, user_id=str(self.user.id), db=self.session
        )

        self.assertEqual(result, contact)
        self.session.execute.assert_awaited()

    async def test_get_not_found_contact(self):
        self.session.execute = AsyncMock()
        self.session.execute.return_value = MagicMock()
        self.session.execute.return_value.scalar_one_or_none.return_value = None

        result = await contact_repository.get_contact(
            contact_id=1, user_id=str(self.user.id), db=self.session
        )

        self.assertIsNone(result)
        self.session.execute.assert_awaited()

    async def test_get_contacts(self):
        contacts = [
            Contact(id=1, user_id=str(self.user.id)),
            Contact(id=2, user_id=str(self.user.id)),
            Contact(id=3, user_id=str(self.user.id))
        ]

        self.session.execute = AsyncMock()
        self.session.execute.return_value = MagicMock()
        self.session.execute.return_value.scalars().all.return_value = contacts
        self.session.execute.return_value.scalar_one_or_none.return_value = len(contacts)

        [result_contacts, count] = await contact_repository.get_contacts(
            offset=0, limit=10, search=None, user_id=str(self.user.id), db=self.session
        )

        self.assertEqual(result_contacts, contacts)
        self.assertEqual(count, len(contacts))
        self.session.execute.assert_awaited()

    async def test_create_contact(self):
        contact = Contact(**test_contact,id=1, user_id=str(self.user.id))

        self.session.add = MagicMock()
        self.session.commit = AsyncMock()
        self.session.refresh = AsyncMock()

        result = await contact_repository.create_contact(
            body=ContactBaseSchema(**test_contact, user_id=self.user.id), user_id=self.user.id, db=self.session
        )

        self.assertEqual(contact.email, result.email)
        self.assertEqual(contact.name, result.name)

    async def test_update_contact(self):
        contact = Contact(**test_contact,id=1, user_id=str(self.user.id))

        self.session.commit = AsyncMock()
        self.session.refresh = AsyncMock()

        self.session.execute = AsyncMock()
        self.session.execute.return_value = MagicMock()
        self.session.execute.return_value.scalar_one_or_none.return_value = contact

        result = await contact_repository.update_contact(
            body=ContactBaseSchema(**test_contact, user_id=self.user.id), contact_id=contact.id, user_id=self.user.id, db=self.session
        )

        self.assertEqual(contact.email, result.email)
        self.assertEqual(contact.name, result.name)


    async def test_delete_contact(self):
        contact = Contact(**test_contact,id=1, user_id=str(self.user.id))

        self.session.commit = AsyncMock()
        self.session.refresh = AsyncMock()

        self.session.execute = AsyncMock()
        self.session.execute.return_value = MagicMock()
        self.session.execute.return_value.scalar_one_or_none.return_value = contact

        result = await contact_repository.delete_contact(
            contact_id=contact.id, user_id=self.user.id, db=self.session
        )

        self.assertEqual(contact.email, result.email)
        self.assertEqual(contact.name, result.name)


if __name__ == '__main__':
    unittest.main()