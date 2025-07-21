# tests/test_app.py

import unittest
import os

# Ensure the app runs in testing mode
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Tia Marie Gordon</title>" in html
        assert "Greetings! My name is Tia Marie Gordon" in html
        assert "Nintendo" in html
        assert "Green River College" in html
        assert "States I've Visited" in html

    def test_hobbies(self):
        response = self.client.get("/hobbies")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Hobbies" in html
        assert "Gaming" in html
        assert "Cross-Stitching" in html
        assert "Legos" in html
        assert "Reading" in html
        assert "Web Development" in html

    def test_timeline(self):
        # Timeline should be empty initially
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert "timeline_posts" in json_data
        assert len(json_data["timeline_posts"]) == 0

        # Add a timeline post
        post = {"name": "Unit Tester", "email": "unit@test.com", "content": "Automated test post"}
        post_resp = self.client.post("/api/timeline_post", data=post)
        assert post_resp.status_code == 200
        post_json = post_resp.get_json()
        for key in post:
            assert post_json[key] == post[key]

        # Confirm the post is now present
        updated = self.client.get("/api/timeline_post").get_json()
        assert len(updated["timeline_posts"]) >= 1
        assert updated["timeline_posts"][0]["name"] == "Unit Tester"

    def test_timeline_page(self):
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h1>Timeline</h1>" in html
        assert "form" in html
        assert "Name:" in html
        assert "Email:" in html
        assert "Content:" in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com", "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "john@example.com", "content": ""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
