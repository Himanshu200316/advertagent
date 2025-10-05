"""TestSprite-compatible test file for Instagram Advertisement Agent."""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestInstagramAgent(unittest.TestCase):
    """Test cases for the Instagram Advertisement Agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'CEREBRUS_API_KEY': 'test_cerebrus_key',
            'CEREBRUS_BASE_URL': 'https://test.cerebrus.com',
            'GEMINI_API_KEY': 'test_gemini_key',
            'INSTAGRAM_ACCESS_TOKEN': 'test_instagram_token',
            'INSTAGRAM_APP_ID': 'test_app_id',
            'INSTAGRAM_APP_SECRET': 'test_app_secret',
            'STORAGE_PATH': './test_data'
        })
        self.env_patcher.start()
        
        # Create test data directory
        os.makedirs('./test_data', exist_ok=True)
    
    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()
        # Clean up test data
        import shutil
        if os.path.exists('./test_data'):
            shutil.rmtree('./test_data')
    
    def test_config_validation(self):
        """Test configuration validation."""
        try:
            from config import Config
            Config.validate()
            self.assertTrue(True, "Configuration validation passed")
        except Exception as e:
            self.fail(f"Configuration validation failed: {str(e)}")
    
    def test_storage_system(self):
        """Test the storage system."""
        try:
            from storage import ContentStorage
            
            storage = ContentStorage('./test_data')
            
            # Test adding a prompt
            prompt_id = storage.add_prompt("Test prompt for coffee beans", {"test": True})
            self.assertIsNotNone(prompt_id)
            
            # Test adding a caption
            caption_id = storage.add_caption("Test caption", prompt_id, {"test": True})
            self.assertIsNotNone(caption_id)
            
            # Test adding an image
            image_id = storage.add_image("./test_image.jpg", prompt_id, {"test": True})
            self.assertIsNotNone(image_id)
            
            # Test adding a post
            post_id = storage.add_post({"test": "post data"})
            self.assertIsNotNone(post_id)
            
            # Test duplicate prevention
            is_duplicate = storage.add_prompt("Test prompt for coffee beans", {"test": True})
            self.assertFalse(is_duplicate, "Duplicate prevention should work")
            
        except Exception as e:
            self.fail(f"Storage system test failed: {str(e)}")
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_gemini_client(self, mock_model_class, mock_configure):
        """Test Gemini client with mocked API."""
        try:
            # Mock the Gemini API response
            mock_model = Mock()
            mock_model.generate_content.return_value.text = "Test caption for coffee beans #coffee #premium"
            mock_model_class.return_value = mock_model
            
            from gemini_client import GeminiClient
            
            gemini = GeminiClient()
            
            product_details = {
                "description": "Premium coffee beans from Colombia",
                "target_audience": "coffee enthusiasts"
            }
            
            # Test caption generation
            caption = gemini.generate_caption(product_details, "professional")
            self.assertIsNotNone(caption)
            self.assertIsInstance(caption, str)
            
            # Test hashtag generation
            hashtags = gemini.generate_hashtags(product_details, caption)
            self.assertIsNotNone(hashtags)
            self.assertIsInstance(hashtags, list)
            
        except Exception as e:
            self.fail(f"Gemini client test failed: {str(e)}")
    
    @patch('requests.post')
    @patch('requests.get')
    def test_instagram_client(self, mock_get, mock_post):
        """Test Instagram client with mocked API."""
        try:
            # Mock API responses
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"id": "test_media_id"}
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"id": "test_account", "username": "test_user"}
            
            from instagram_client import InstagramClient
            
            instagram = InstagramClient()
            
            # Test account info
            account_info = instagram.get_account_info()
            self.assertIsNotNone(account_info)
            self.assertIn("id", account_info)
            
        except Exception as e:
            self.fail(f"Instagram client test failed: {str(e)}")
    
    @patch('cerebrus_client.CerebrusClient')
    @patch('gemini_client.GeminiClient')
    @patch('instagram_client.InstagramClient')
    def test_instagram_agent(self, mock_instagram, mock_gemini, mock_cerebrus):
        """Test the main Instagram agent."""
        try:
            # Mock the clients
            mock_cerebrus_instance = Mock()
            mock_cerebrus_instance.collect_user_input.return_value = {
                "product_details": {
                    "tone": "professional",
                    "target_audience": "coffee enthusiasts",
                    "description": "Premium coffee beans"
                },
                "image_preferences": {
                    "use_ai_generated": True,
                    "style": "modern"
                },
                "posting_preferences": {
                    "post_to_feed": True,
                    "post_to_stories": True
                }
            }
            mock_cerebrus.return_value = mock_cerebrus_instance
            
            mock_gemini_instance = Mock()
            mock_gemini_instance.generate_caption.return_value = "Test caption"
            mock_gemini_instance.generate_hashtags.return_value = ["#coffee", "#premium"]
            mock_gemini_instance.generate_image.return_value = "./test_image.jpg"
            mock_gemini.return_value = mock_gemini_instance
            
            mock_instagram_instance = Mock()
            mock_instagram_instance.post_to_feed.return_value = {"success": True, "media_id": "test_id"}
            mock_instagram_instance.post_to_stories.return_value = {"success": True, "media_id": "test_id"}
            mock_instagram.return_value = mock_instagram_instance
            
            from instagram_agent import InstagramAdvertisementAgent
            
            agent = InstagramAdvertisementAgent()
            
            # Test analytics
            analytics = agent.get_analytics()
            self.assertIsNotNone(analytics)
            self.assertIn("total_prompts", analytics)
            
        except Exception as e:
            self.fail(f"Instagram agent test failed: {str(e)}")
    
    def test_health_check(self):
        """Test health check endpoint."""
        try:
            from health_check import app
            
            with app.test_client() as client:
                response = client.get('/health')
                self.assertEqual(response.status_code, 200)
                
                data = json.loads(response.data)
                self.assertIn('status', data)
                self.assertIn('timestamp', data)
                
        except Exception as e:
            self.fail(f"Health check test failed: {str(e)}")
    
    def test_duplicate_prevention(self):
        """Test duplicate prevention logic."""
        try:
            from storage import ContentStorage
            
            storage = ContentStorage('./test_data')
            
            # Add first prompt
            prompt1 = storage.add_prompt("Premium coffee beans from Colombia", {"test": True})
            self.assertTrue(prompt1)
            
            # Try to add similar prompt (should be detected as duplicate)
            prompt2 = storage.add_prompt("Premium coffee from Colombia", {"test": True})
            self.assertFalse(prompt2, "Similar prompt should be detected as duplicate")
            
            # Add different prompt (should not be duplicate)
            prompt3 = storage.add_prompt("Fresh organic vegetables", {"test": True})
            self.assertTrue(prompt3, "Different prompt should not be duplicate")
            
        except Exception as e:
            self.fail(f"Duplicate prevention test failed: {str(e)}")
    
    def test_data_cleanup(self):
        """Test data cleanup functionality."""
        try:
            from storage import ContentStorage
            
            storage = ContentStorage('./test_data')
            
            # Add some test data
            storage.add_prompt("Test prompt 1", {"test": True})
            storage.add_prompt("Test prompt 2", {"test": True})
            
            # Test cleanup
            storage.cleanup_old_data(0)  # Clean up everything
            
            # Verify data is cleaned up
            recent_prompts = storage.get_recent_prompts(10)
            self.assertEqual(len(recent_prompts), 0, "Data should be cleaned up")
            
        except Exception as e:
            self.fail(f"Data cleanup test failed: {str(e)}")

def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestInstagramAgent)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return test results
    return {
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "success": result.wasSuccessful(),
        "failure_details": [str(f[1]) for f in result.failures],
        "error_details": [str(e[1]) for e in result.errors]
    }

if __name__ == "__main__":
    print("🧪 Running Instagram Advertisement Agent Tests with TestSprite compatibility")
    print("=" * 70)
    
    try:
        results = run_tests()
        
        print("\n" + "=" * 70)
        print("📊 Test Results Summary:")
        print(f"   Tests Run: {results['tests_run']}")
        print(f"   Failures: {results['failures']}")
        print(f"   Errors: {results['errors']}")
        print(f"   Success: {results['success']}")
        
        if results['failures'] > 0:
            print("\n❌ Failures:")
            for failure in results['failure_details']:
                print(f"   {failure}")
        
        if results['errors'] > 0:
            print("\n💥 Errors:")
            for error in results['error_details']:
                print(f"   {error}")
        
        if results['success']:
            print("\n🎉 All tests passed! The Instagram Advertisement Agent is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Please check the issues above.")
        
        sys.exit(0 if results['success'] else 1)
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {str(e)}")
        sys.exit(1)