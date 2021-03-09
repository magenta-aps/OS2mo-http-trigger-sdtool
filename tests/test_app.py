from unittest import TestCase

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app


class AppTests(TestCase):
    def setUp(self):
        self.app = app
        self.client = TestClient(app)

    def test_triggers():
        response = client.get("/triggers")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        trigger = payload[0]
        self.assertEqual(trigger["url"], "/triggers/ou/edit")
        self.assertEqual(trigger["role_type"], "org_unit")

    def test_triggers():
        response = client.post("/triggers/ou/edit", json={
                "event_type": "ON_BEFORE",
                "request": {},
                "request_type": "EDIT",
                "role_type": "org_unit",
                "uuid": "fb2d158f-114e-5f67-8365-2c520cf10b58",
            }
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload, {
            "configured_value": "TriggerExample"
        })
