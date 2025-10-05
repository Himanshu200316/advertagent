"""Main Instagram Advertisement Agent orchestrator."""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import schedule
import time

from config import Config
from storage import ContentStorage
from cerebrus_client import CerebrusClient
from gemini_client import GeminiClient
from instagram_client import InstagramClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class InstagramAdvertisementAgent:
    """Main orchestrator for the Instagram Advertisement Agent."""
    
    def __init__(self):
        """Initialize the Instagram Advertisement Agent."""
        try:
            # Validate configuration
            Config.validate()
            
            # Initialize components
            self.storage = ContentStorage(Config.STORAGE_PATH)
            self.cerebrus = CerebrusClient()
            self.gemini = GeminiClient()
            self.instagram = InstagramClient()
            
            logger.info("Instagram Advertisement Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Instagram Advertisement Agent: {str(e)}")
            raise
    
    def run_daily_posting(self):
        """Run the daily posting process."""
        try:
            logger.info("Starting daily posting process")
            
            # Step 1: Collect user input (in production, this would be from Cerebrus)
            user_data = self._collect_user_input()
            
            # Step 2: Generate content
            content = self._generate_content(user_data)
            
            if not content:
                logger.warning("No content generated, skipping posting")
                return
            
            # Step 3: Post to Instagram
            self._post_content(content)
            
            logger.info("Daily posting process completed successfully")
            
        except Exception as e:
            logger.error(f"Daily posting process failed: {str(e)}")
            raise
    
    def _collect_user_input(self) -> Dict[str, Any]:
        """Collect user input for content generation."""
        try:
            # In production, this would interact with Cerebrus API
            # For now, we'll use a simulated user input
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            user_data = {
                "instagram_credentials": {
                    "username": "demo_account",
                    "password": "demo_password"
                },
                "product_details": {
                    "tone": "professional",
                    "target_audience": "coffee enthusiasts aged 25-45",
                    "description": "Premium single-origin coffee beans from sustainable farms in Colombia"
                },
                "image_preferences": {
                    "use_ai_generated": True,
                    "uploaded_images": [],
                    "style": "modern and minimalist"
                },
                "posting_preferences": {
                    "post_to_feed": True,
                    "post_to_stories": True,
                    "schedule_time": "00:00"
                }
            }
            
            # Store user input in storage
            self.storage.add_prompt(
                f"Product: {user_data['product_details']['description']}",
                user_data
            )
            
            return user_data
            
        except Exception as e:
            logger.error(f"Failed to collect user input: {str(e)}")
            raise
    
    def _generate_content(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate content using Gemini API."""
        try:
            product_details = user_data["product_details"]
            image_preferences = user_data["image_preferences"]
            
            # Generate caption
            caption = self.gemini.generate_caption(
                product_details, 
                product_details.get("tone", "professional")
            )
            
            # Generate hashtags
            hashtags = self.gemini.generate_hashtags(product_details, caption)
            
            # Generate or use uploaded image
            if image_preferences.get("use_ai_generated", True):
                image_path = self.gemini.generate_image(
                    product_details,
                    image_preferences.get("style", "modern")
                )
            else:
                # Use uploaded images
                uploaded_images = image_preferences.get("uploaded_images", [])
                if uploaded_images:
                    image_path = uploaded_images[0]
                else:
                    logger.warning("No images available, generating AI image")
                    image_path = self.gemini.generate_image(
                        product_details,
                        image_preferences.get("style", "modern")
                    )
            
            # Store content in history
            prompt_id = len(self.storage._load_json(self.storage.prompts_file))
            caption_id = self.storage.add_caption(caption, prompt_id, product_details)
            image_id = self.storage.add_image(image_path, prompt_id, image_preferences)
            
            content = {
                "caption": caption,
                "hashtags": hashtags,
                "image_path": image_path,
                "prompt_id": prompt_id,
                "caption_id": caption_id,
                "image_id": image_id,
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "product_details": product_details,
                    "image_preferences": image_preferences
                }
            }
            
            logger.info("Content generated successfully")
            return content
            
        except Exception as e:
            logger.error(f"Failed to generate content: {str(e)}")
            return None
    
    def _post_content(self, content: Dict[str, Any]):
        """Post content to Instagram."""
        try:
            posting_preferences = content["metadata"]["product_details"]
            results = {}
            
            # Post to feed
            if posting_preferences.get("post_to_feed", True):
                feed_result = self.instagram.post_to_feed(
                    content["image_path"],
                    content["caption"],
                    content["hashtags"]
                )
                results["feed"] = feed_result
                logger.info(f"Feed post result: {feed_result}")
            
            # Post to stories
            if posting_preferences.get("post_to_stories", True):
                story_result = self.instagram.post_to_stories(
                    content["image_path"],
                    content["caption"]
                )
                results["stories"] = story_result
                logger.info(f"Story post result: {story_result}")
            
            # Store posting results
            post_data = {
                "content": content,
                "results": results,
                "posted_at": datetime.now().isoformat()
            }
            
            self.storage.add_post(post_data)
            
            logger.info("Content posted successfully")
            
        except Exception as e:
            logger.error(f"Failed to post content: {str(e)}")
            raise
    
    def schedule_daily_posting(self):
        """Schedule daily posting at 12 AM."""
        try:
            schedule.every().day.at(Config.POST_TIME).do(self.run_daily_posting)
            logger.info(f"Daily posting scheduled for {Config.POST_TIME}")
            
            # Keep the scheduler running
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except Exception as e:
            logger.error(f"Failed to schedule daily posting: {str(e)}")
            raise
    
    def run_manual_posting(self):
        """Run a manual posting process (for testing)."""
        try:
            logger.info("Running manual posting process")
            self.run_daily_posting()
            
        except Exception as e:
            logger.error(f"Manual posting failed: {str(e)}")
            raise
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics and statistics."""
        try:
            recent_prompts = self.storage.get_recent_prompts(10)
            recent_captions = self.storage.get_recent_captions(10)
            recent_posts = self.storage.get_recent_posts(10)
            
            return {
                "total_prompts": len(recent_prompts),
                "total_captions": len(recent_captions),
                "total_posts": len(recent_posts),
                "recent_prompts": recent_prompts,
                "recent_captions": recent_captions,
                "recent_posts": recent_posts
            }
            
        except Exception as e:
            logger.error(f"Failed to get analytics: {str(e)}")
            return {}
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old data."""
        try:
            self.storage.cleanup_old_data(days)
            logger.info(f"Cleaned up data older than {days} days")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {str(e)}")

def main():
    """Main entry point for the Instagram Advertisement Agent."""
    try:
        # Initialize the agent
        agent = InstagramAdvertisementAgent()
        
        # Check command line arguments
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == "manual":
                # Run manual posting
                agent.run_manual_posting()
            elif command == "schedule":
                # Run scheduled posting
                agent.schedule_daily_posting()
            elif command == "analytics":
                # Show analytics
                analytics = agent.get_analytics()
                print(json.dumps(analytics, indent=2))
            elif command == "cleanup":
                # Cleanup old data
                days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
                agent.cleanup_old_data(days)
            else:
                print("Usage: python instagram_agent.py [manual|schedule|analytics|cleanup]")
        else:
            # Default: run manual posting
            agent.run_manual_posting()
            
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()