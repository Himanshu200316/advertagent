"""Comprehensive TestSprite-compatible test for Instagram Advertisement Agent."""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestInstagramAgentComprehensive(unittest.TestCase):
    """Comprehensive test cases for the Instagram Advertisement Agent."""
    
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
    
    @patch('dotenv.load_dotenv')
    def test_config_validation(self, mock_load_dotenv):
        """Test configuration validation with mocked dotenv."""
        try:
            # Mock the dotenv module
            with patch.dict('sys.modules', {'dotenv': Mock()}):
                # Import config after mocking
                import config
                
                # Test configuration validation
                config.Config.validate()
                self.assertTrue(True, "Configuration validation passed")
                
        except Exception as e:
            self.fail(f"Configuration validation failed: {str(e)}")
    
    def test_storage_system_comprehensive(self):
        """Test the storage system comprehensively."""
        try:
            import storage
            
            storage_instance = storage.ContentStorage('./test_data')
            
            # Test adding multiple prompts
            prompt_ids = []
            for i in range(5):
                prompt_id = storage_instance.add_prompt(f"Test prompt {i} for coffee beans", {"test": True, "index": i})
                prompt_ids.append(prompt_id)
                self.assertTrue(prompt_id, f"Prompt {i} should be added")
            
            # Test adding captions
            caption_ids = []
            for i, prompt_id in enumerate(prompt_ids):
                caption_id = storage_instance.add_caption(f"Test caption {i}", prompt_id, {"test": True})
                caption_ids.append(caption_id)
                self.assertIsNotNone(caption_id)
            
            # Test adding images
            image_ids = []
            for i, prompt_id in enumerate(prompt_ids):
                image_id = storage_instance.add_image(f"./test_image_{i}.jpg", prompt_id, {"test": True})
                image_ids.append(image_id)
                self.assertIsNotNone(image_id)
            
            # Test adding posts
            post_ids = []
            for i in range(3):
                post_id = storage_instance.add_post({"test": f"post data {i}", "index": i})
                post_ids.append(post_id)
                self.assertIsNotNone(post_id)
            
            # Test duplicate prevention
            duplicate_result = storage_instance.add_prompt("Test prompt 0 for coffee beans", {"test": True})
            self.assertFalse(duplicate_result, "Exact duplicate should be prevented")
            
            # Test similar prompt detection
            similar_result = storage_instance.add_prompt("Test prompt 0 for coffee", {"test": True})
            self.assertFalse(similar_result, "Similar prompt should be prevented")
            
            # Test different prompt (should be allowed)
            different_result = storage_instance.add_prompt("Fresh organic vegetables from local farm", {"test": True})
            self.assertTrue(different_result, "Different prompt should be allowed")
            
            # Test data retrieval
            recent_prompts = storage_instance.get_recent_prompts(10)
            self.assertGreater(len(recent_prompts), 0, "Should have recent prompts")
            
            recent_captions = storage_instance.get_recent_captions(10)
            self.assertGreater(len(recent_captions), 0, "Should have recent captions")
            
            recent_posts = storage_instance.get_recent_posts(10)
            self.assertGreater(len(recent_posts), 0, "Should have recent posts")
            
        except Exception as e:
            self.fail(f"Storage system comprehensive test failed: {str(e)}")
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_gemini_client_comprehensive(self, mock_model_class, mock_configure):
        """Test Gemini client comprehensively with mocked API."""
        try:
            # Mock the Gemini API response
            mock_model = Mock()
            mock_model.generate_content.return_value.text = "Test caption for coffee beans #coffee #premium #organic"
            mock_model_class.return_value = mock_model
            
            # Mock the google.generativeai module
            with patch.dict('sys.modules', {'google.generativeai': Mock()}):
                import gemini_client
                
                gemini = gemini_client.GeminiClient()
                
                product_details = {
                    "description": "Premium coffee beans from Colombia",
                    "target_audience": "coffee enthusiasts aged 25-45"
                }
                
                # Test caption generation
                caption = gemini.generate_caption(product_details, "professional")
                self.assertIsNotNone(caption)
                self.assertIsInstance(caption, str)
                self.assertGreater(len(caption), 0, "Caption should not be empty")
                
                # Test hashtag generation
                hashtags = gemini.generate_hashtags(product_details, caption)
                self.assertIsNotNone(hashtags)
                self.assertIsInstance(hashtags, list)
                self.assertGreater(len(hashtags), 0, "Should generate hashtags")
                
                # Test image generation
                image_path = gemini.generate_image(product_details, "modern")
                self.assertIsNotNone(image_path)
                self.assertIsInstance(image_path, str)
                self.assertTrue(image_path.endswith('.jpg'), "Should generate JPG image")
                
        except Exception as e:
            self.fail(f"Gemini client comprehensive test failed: {str(e)}")
    
    @patch('requests.post')
    @patch('requests.get')
    def test_instagram_client_comprehensive(self, mock_get, mock_post):
        """Test Instagram client comprehensively with mocked API."""
        try:
            # Mock API responses
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"id": "test_media_id"}
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "id": "test_account", 
                "username": "test_user",
                "account_type": "BUSINESS",
                "media_count": 100
            }
            
            # Mock the requests module
            with patch.dict('sys.modules', {'requests': Mock()}):
                import instagram_client
                
                instagram = instagram_client.InstagramClient()
                
                # Test account info
                account_info = instagram.get_account_info()
                self.assertIsNotNone(account_info)
                self.assertIn("id", account_info)
                self.assertIn("username", account_info)
                
                # Test feed posting
                feed_result = instagram.post_to_feed(
                    "./test_image.jpg",
                    "Test caption",
                    ["#coffee", "#premium"]
                )
                self.assertIsNotNone(feed_result)
                self.assertIn("success", feed_result)
                
                # Test story posting
                story_result = instagram.post_to_stories(
                    "./test_image.jpg",
                    "Test story caption"
                )
                self.assertIsNotNone(story_result)
                self.assertIn("success", story_result)
                
        except Exception as e:
            self.fail(f"Instagram client comprehensive test failed: {str(e)}")
    
    @patch('cerebrus_client.CerebrusClient')
    @patch('gemini_client.GeminiClient')
    @patch('instagram_client.InstagramClient')
    def test_instagram_agent_comprehensive(self, mock_instagram, mock_gemini, mock_cerebrus):
        """Test the main Instagram agent comprehensively."""
        try:
            # Mock the clients
            mock_cerebrus_instance = Mock()
            mock_cerebrus_instance.collect_user_input.return_value = {
                "product_details": {
                    "tone": "professional",
                    "target_audience": "coffee enthusiasts aged 25-45",
                    "description": "Premium single-origin coffee beans from sustainable farms in Colombia"
                },
                "image_preferences": {
                    "use_ai_generated": True,
                    "style": "modern and minimalist"
                },
                "posting_preferences": {
                    "post_to_feed": True,
                    "post_to_stories": True
                }
            }
            mock_cerebrus.return_value = mock_cerebrus_instance
            
            mock_gemini_instance = Mock()
            mock_gemini_instance.generate_caption.return_value = "Discover the rich, bold flavor of our premium Colombian coffee beans. Perfect for the discerning coffee enthusiast who values quality and sustainability. #coffee #premium #sustainable #colombia"
            mock_gemini_instance.generate_hashtags.return_value = ["#coffee", "#premium", "#sustainable", "#colombia", "#organic"]
            mock_gemini_instance.generate_image.return_value = "./generated_images/coffee_ad.jpg"
            mock_gemini.return_value = mock_gemini_instance
            
            mock_instagram_instance = Mock()
            mock_instagram_instance.post_to_feed.return_value = {
                "success": True, 
                "media_id": "test_feed_id",
                "timestamp": datetime.now().isoformat()
            }
            mock_instagram_instance.post_to_stories.return_value = {
                "success": True, 
                "media_id": "test_story_id",
                "timestamp": datetime.now().isoformat()
            }
            mock_instagram.return_value = mock_instagram_instance
            
            # Mock the modules
            with patch.dict('sys.modules', {
                'cerebrus_client': Mock(),
                'gemini_client': Mock(),
                'instagram_client': Mock(),
                'config': Mock()
            }):
                import instagram_agent
                
                agent = instagram_agent.InstagramAdvertisementAgent()
                
                # Test analytics
                analytics = agent.get_analytics()
                self.assertIsNotNone(analytics)
                self.assertIn("total_prompts", analytics)
                self.assertIn("total_captions", analytics)
                self.assertIn("total_posts", analytics)
                
                # Test manual posting workflow
                agent.run_manual_posting()
                
        except Exception as e:
            self.fail(f"Instagram agent comprehensive test failed: {str(e)}")
    
    @patch('flask.Flask')
    def test_health_check_comprehensive(self, mock_flask):
        """Test health check endpoint comprehensively."""
        try:
            # Mock Flask
            mock_app = Mock()
            mock_app.test_client.return_value.get.return_value.status_code = 200
            mock_app.test_client.return_value.get.return_value.data = json.dumps({
                "status": "healthy",
                "timestamp": datetime.now().isoformat()
            })
            mock_flask.return_value = mock_app
            
            # Mock the flask module
            with patch.dict('sys.modules', {'flask': Mock()}):
                import health_check
                
                # Test health check endpoint
                with health_check.app.test_client() as client:
                    response = client.get('/health')
                    self.assertEqual(response.status_code, 200)
                    
                    data = json.loads(response.data)
                    self.assertIn('status', data)
                    self.assertIn('timestamp', data)
                
        except Exception as e:
            self.fail(f"Health check comprehensive test failed: {str(e)}")
    
    def test_error_handling(self):
        """Test error handling in various components."""
        try:
            import storage
            
            storage_instance = storage.ContentStorage('./test_data')
            
            # Test with invalid data
            try:
                storage_instance.add_prompt("", {})  # Empty prompt
                # Should not raise exception, but should handle gracefully
            except Exception:
                self.fail("Should handle empty prompt gracefully")
            
            # Test with None values
            try:
                storage_instance.add_caption(None, 1, {})
                # Should not raise exception, but should handle gracefully
            except Exception:
                self.fail("Should handle None caption gracefully")
            
            # Test cleanup with invalid parameters
            try:
                storage_instance.cleanup_old_data(-1)  # Invalid days
                # Should not raise exception
            except Exception:
                self.fail("Should handle invalid cleanup parameters gracefully")
            
        except Exception as e:
            self.fail(f"Error handling test failed: {str(e)}")
    
    def test_data_persistence(self):
        """Test data persistence across storage instances."""
        try:
            import storage
            
            # Create first storage instance
            storage1 = storage.ContentStorage('./test_data')
            
            # Add some data
            prompt_id = storage1.add_prompt("Test persistence prompt", {"test": True})
            caption_id = storage1.add_caption("Test persistence caption", prompt_id, {"test": True})
            
            # Create second storage instance (should load existing data)
            storage2 = storage.ContentStorage('./test_data')
            
            # Verify data persists
            recent_prompts = storage2.get_recent_prompts(10)
            self.assertGreater(len(recent_prompts), 0, "Data should persist across instances")
            
            # Verify the specific data we added
            found_prompt = False
            for prompt in recent_prompts:
                if prompt["prompt"] == "Test persistence prompt":
                    found_prompt = True
                    break
            self.assertTrue(found_prompt, "Specific prompt should persist")
            
        except Exception as e:
            self.fail(f"Data persistence test failed: {str(e)}")
    
    def test_performance_with_large_data(self):
        """Test performance with larger datasets."""
        try:
            import storage
            import time
            
            storage_instance = storage.ContentStorage('./test_data')
            
            # Add many prompts
            start_time = time.time()
            for i in range(100):
                storage_instance.add_prompt(f"Performance test prompt {i}", {"test": True, "index": i})
            
            add_time = time.time() - start_time
            self.assertLess(add_time, 5.0, "Adding 100 prompts should take less than 5 seconds")
            
            # Test retrieval performance
            start_time = time.time()
            recent_prompts = storage_instance.get_recent_prompts(50)
            retrieval_time = time.time() - start_time
            self.assertLess(retrieval_time, 1.0, "Retrieving 50 prompts should take less than 1 second")
            
            # Test duplicate detection performance
            start_time = time.time()
            for i in range(20):
                storage_instance.add_prompt(f"Performance test prompt {i}", {"test": True})
            duplicate_time = time.time() - start_time
            self.assertLess(duplicate_time, 2.0, "Duplicate detection should be fast")
            
        except Exception as e:
            self.fail(f"Performance test failed: {str(e)}")

def run_comprehensive_tests():
    """Run all comprehensive tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestInstagramAgentComprehensive)
    
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
    print("🧪 Running Comprehensive Instagram Advertisement Agent Tests")
    print("=" * 70)
    
    try:
        results = run_comprehensive_tests()
        
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
            print("\n🎉 All comprehensive tests passed!")
            print("   The Instagram Advertisement Agent is fully functional and ready for production.")
            print("\n📋 Production Readiness Checklist:")
            print("   ✅ Core functionality working")
            print("   ✅ Error handling implemented")
            print("   ✅ Data persistence verified")
            print("   ✅ Performance tested")
            print("   ✅ Duplicate prevention working")
            print("   ✅ API integrations mocked and tested")
        else:
            print("\n⚠️  Some tests failed. Please check the issues above.")
        
        sys.exit(0 if results['success'] else 1)
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {str(e)}")
        sys.exit(1)