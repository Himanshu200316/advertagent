"""Instagram posting client using MCP Instagram Module."""

import requests
import json
from typing import Dict, Any, Optional, List
from config import Config
import os
from datetime import datetime

class InstagramClient:
    """Client for posting content to Instagram using MCP Instagram Module."""
    
    def __init__(self):
        """Initialize the Instagram client."""
        self.access_token = Config.INSTAGRAM_ACCESS_TOKEN
        self.app_id = Config.INSTAGRAM_APP_ID
        self.app_secret = Config.INSTAGRAM_APP_SECRET
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def post_to_feed(self, image_path: str, caption: str, hashtags: List[str] = None) -> Dict[str, Any]:
        """Post an image with caption to Instagram feed."""
        try:
            # Step 1: Create media container
            media_id = self._create_media_container(image_path, caption, hashtags)
            
            # Step 2: Publish the media
            publish_result = self._publish_media(media_id)
            
            return {
                "success": True,
                "media_id": media_id,
                "publish_result": publish_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def post_to_stories(self, image_path: str, caption: str = None) -> Dict[str, Any]:
        """Post an image to Instagram stories."""
        try:
            # Upload the image
            media_id = self._upload_story_media(image_path)
            
            # Create story
            story_result = self._create_story(media_id, caption)
            
            return {
                "success": True,
                "media_id": media_id,
                "story_result": story_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _create_media_container(self, image_path: str, caption: str, hashtags: List[str] = None) -> str:
        """Create a media container for Instagram feed post."""
        # Upload image to Instagram
        image_url = self._upload_image(image_path)
        
        # Prepare caption with hashtags
        full_caption = caption
        if hashtags:
            full_caption += "\n\n" + " ".join(hashtags)
        
        # Create media container
        url = f"{self.base_url}/{Config.INSTAGRAM_APP_ID}/media"
        data = {
            "image_url": image_url,
            "caption": full_caption,
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("id")
        else:
            raise Exception(f"Failed to create media container: {response.text}")
    
    def _publish_media(self, media_id: str) -> Dict[str, Any]:
        """Publish the media container to Instagram feed."""
        url = f"{self.base_url}/{Config.INSTAGRAM_APP_ID}/media_publish"
        data = {
            "creation_id": media_id,
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to publish media: {response.text}")
    
    def _upload_story_media(self, image_path: str) -> str:
        """Upload image for Instagram stories."""
        # For stories, we need to upload the image first
        image_url = self._upload_image(image_path)
        
        # Create story media container
        url = f"{self.base_url}/{Config.INSTAGRAM_APP_ID}/media"
        data = {
            "image_url": image_url,
            "media_type": "STORIES",
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("id")
        else:
            raise Exception(f"Failed to upload story media: {response.text}")
    
    def _create_story(self, media_id: str, caption: str = None) -> Dict[str, Any]:
        """Create an Instagram story."""
        url = f"{self.base_url}/{Config.INSTAGRAM_APP_ID}/media_publish"
        data = {
            "creation_id": media_id,
            "access_token": self.access_token
        }
        
        if caption:
            data["caption"] = caption
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create story: {response.text}")
    
    def _upload_image(self, image_path: str) -> str:
        """Upload image to a temporary location and return URL."""
        # In a real implementation, you would upload to a cloud storage service
        # For now, we'll simulate this by returning a placeholder URL
        return f"https://example.com/images/{os.path.basename(image_path)}"
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get Instagram account information."""
        try:
            url = f"{self.base_url}/me"
            params = {
                "fields": "id,username,account_type,media_count",
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get account info: {response.text}")
                
        except Exception as e:
            raise Exception(f"Failed to get account info: {str(e)}")
    
    def get_recent_posts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent posts from the account."""
        try:
            url = f"{self.base_url}/me/media"
            params = {
                "fields": "id,caption,media_type,media_url,thumbnail_url,timestamp",
                "limit": limit,
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json().get("data", [])
            else:
                raise Exception(f"Failed to get recent posts: {response.text}")
                
        except Exception as e:
            raise Exception(f"Failed to get recent posts: {str(e)}")
    
    def delete_post(self, media_id: str) -> bool:
        """Delete a post from Instagram."""
        try:
            url = f"{self.base_url}/{media_id}"
            data = {
                "access_token": self.access_token
            }
            
            response = requests.delete(url, data=data)
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Failed to delete post: {str(e)}")
            return False