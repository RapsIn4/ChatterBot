from unittest import TestCase
from chatterbot.conversation.session import Session, SessionManager


class SessionTestCase(TestCase):

    def test_id_string(self):
        session = Session()
        self.assertEqual(str(session.uuid), session.id_string)

class SessionManagerTestCase(TestCase):

    def setUp(self):
        super(SessionManagerTestCase, self).setUp()
        self.manager = SessionManager()

    def test_new(self):
        session = self.manager.new()

        self.assertTrue(isinstance(session, Session))
        self.assertIn(session.id_string, self.manager.sessions)
        self.assertEqual(session, self.manager.sessions[session.id_string])

    def test_get(self):
        session = self.manager.new()
        returned_session = self.manager.get(session.id_string)

        self.assertEqual(session.id_string, returned_session.id_string)

    def test_update(self):
        session = self.manager.new()
        self.manager.update(session.id_string, ('A', 'B', ))

        session_ids = list(self.manager.sessions.keys())
        session_id = session_ids[0]

        self.assertEqual(len(session_ids), 1)
        self.assertEqual(len(self.manager.get(session_id).conversation), 1)
        self.assertEqual(('A', 'B', ), self.manager.get(session_id).conversation[0])

    def test_get_default(self):
        session = self.manager.new()
        returned_session = self.manager.get_default()

        self.assertEqual(session.id_string, returned_session.id_string)

    def test_update_default(self):
        self.manager.new()
        self.manager.update_default(('A', 'B', ))

        self.assertEqual(len(self.manager.sessions.keys()), 1)
        self.assertEqual(len(self.manager.get_default().conversation), 1)
        self.assertEqual(('A', 'B', ), self.manager.get_default().conversation[0])
