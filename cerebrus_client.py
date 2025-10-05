"""Cerebrus API client for user interaction and credential collection."""

import requests
import json
from typing import Dict, Any, Optional
from config import Config

class CerebrusClient:
    """Client for interacting with the Cerebrus API."""
    
    def __init__(self):
        """Initialize the Cerebrus client."""
        self.api_key = Config.CEREBRUS_API_KEY
        self.base_url = Config.CEREBRUS_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def collect_user_input(self, session_id: str) -> Dict[str, Any]:
        """Collect user input for Instagram ad generation."""
        try:
            # This would typically be a conversational flow
            # For now, we'll simulate the data collection
            user_data = {
                "instagram_credentials": {
                    "username": "user_input_username",
                    "password": "user_input_password"  # In production, this should be encrypted
                },
                "product_details": {
                    "tone": "professional",  # professional, casual, friendly, etc.
                    "target_audience": "young adults aged 18-35",
                    "description": "Premium coffee beans from sustainable farms"
                },
                "image_preferences": {
                    "use_ai_generated": True,
                    "uploaded_images": [],  # List of uploaded image paths
                    "style": "modern and minimalist"
                },
                "posting_preferences": {
                    "post_to_feed": True,
                    "post_to_stories": True,
                    "schedule_time": "00:00"
                }
            }
            
            return self._send_to_cerebrus(session_id, "collect_user_input", user_data)
            
        except Exception as e:
            raise Exception(f"Failed to collect user input: {str(e)}")
    
    def confirm_posting_preferences(self, session_id: str, preferences: Dict[str, Any]) -> bool:
        """Confirm posting preferences with the user."""
        try:
            response = self._send_to_cerebrus(session_id, "confirm_posting", preferences)
            return response.get("confirmed", False)
        except Exception as e:
            raise Exception(f"Failed to confirm posting preferences: {str(e)}")
    
    def upload_image(self, session_id: str, image_path: str) -> str:
        """Upload an image via Cerebrus API."""
        try:
            with open(image_path, 'rb') as image_file:
                files = {'image': image_file}
                headers = {"Authorization": f"Bearer {self.api_key}"}
                
                response = requests.post(
                    f"{self.base_url}/upload/image",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    return response.json().get("image_url")
                else:
                    raise Exception(f"Image upload failed: {response.text}")
                    
        except Exception as e:
            raise Exception(f"Failed to upload image: {str(e)}")
    
    def _send_to_cerebrus(self, session_id: str, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send data to Cerebrus API."""
        payload = {
            "session_id": session_id,
            "action": action,
            "data": data
        }
        
        response = requests.post(
            f"{self.base_url}/conversation",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Cerebrus API error: {response.text}")
    
    def get_conversation_state(self, session_id: str) -> Dict[str, Any]:
        """Get the current conversation state."""
        try:
            response = requests.get(
                f"{self.base_url}/conversation/{session_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get conversation state: {response.text}")
                
        except Exception as e:
            raise Exception(f"Failed to get conversation state: {str(e)}")
    
    def end_conversation(self, session_id: str) -> bool:
        """End the conversation session."""
        try:
            response = requests.delete(
                f"{self.base_url}/conversation/{session_id}",
                headers=self.headers
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Failed to end conversation: {str(e)}")
            return False