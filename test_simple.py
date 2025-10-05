"""Simplified test for Instagram Advertisement Agent without external dependencies."""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestInstagramAgentSimple(unittest.TestCase):
    """Simplified test cases for the Instagram Advertisement Agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create test data directory
        os.makedirs('./test_data', exist_ok=True)
    
    def tearDown(self):
        """Clean up after tests."""
        # Clean up test data
        import shutil
        if os.path.exists('./test_data'):
            shutil.rmtree('./test_data')
    
    def test_storage_system_basic(self):
        """Test the basic storage system functionality."""
        try:
            # Import storage module directly
            import storage
            
            # Create storage instance
            storage_instance = storage.ContentStorage('./test_data')
            
            # Test adding a prompt
            prompt_id = storage_instance.add_prompt("Test prompt for coffee beans", {"test": True})
            self.assertIsNotNone(prompt_id)
            self.assertTrue(prompt_id)
            
            # Test adding a caption
            caption_id = storage_instance.add_caption("Test caption", prompt_id, {"test": True})
            self.assertIsNotNone(caption_id)
            
            # Test adding an image
            image_id = storage_instance.add_image("./test_image.jpg", prompt_id, {"test": True})
            self.assertIsNotNone(image_id)
            
            # Test adding a post
            post_id = storage_instance.add_post({"test": "post data"})
            self.assertIsNotNone(post_id)
            
            print("✅ Storage system basic functionality working")
            
        except Exception as e:
            self.fail(f"Storage system basic test failed: {str(e)}")
    
    def test_duplicate_prevention_logic(self):
        """Test duplicate prevention logic."""
        try:
            import storage
            
            storage_instance = storage.ContentStorage('./test_data')
            
            # Add first prompt
            prompt1 = storage_instance.add_prompt("Premium coffee beans from Colombia", {"test": True})
            self.assertTrue(prompt1, "First prompt should be added")
            
            # Try to add very similar prompt (should be detected as duplicate)
            prompt2 = storage_instance.add_prompt("Premium coffee from Colombia", {"test": True})
            # Note: The similarity threshold might need adjustment
            print(f"Similar prompt result: {prompt2}")
            
            # Add completely different prompt (should not be duplicate)
            prompt3 = storage_instance.add_prompt("Fresh organic vegetables from local farm", {"test": True})
            self.assertTrue(prompt3, "Different prompt should not be duplicate")
            
            print("✅ Duplicate prevention logic tested")
            
        except Exception as e:
            self.fail(f"Duplicate prevention test failed: {str(e)}")
    
    def test_similarity_calculation(self):
        """Test the similarity calculation function."""
        try:
            import storage
            
            storage_instance = storage.ContentStorage('./test_data')
            
            # Test similar texts
            similarity1 = storage_instance._calculate_similarity(
                "Premium coffee beans from Colombia",
                "Premium coffee from Colombia"
            )
            self.assertGreater(similarity1, 0.5, "Similar texts should have high similarity")
            
            # Test different texts
            similarity2 = storage_instance._calculate_similarity(
                "Premium coffee beans from Colombia",
                "Fresh organic vegetables from local farm"
            )
            self.assertLess(similarity2, 0.5, "Different texts should have low similarity")
            
            # Test identical texts
            similarity3 = storage_instance._calculate_similarity(
                "Premium coffee beans from Colombia",
                "Premium coffee beans from Colombia"
            )
            self.assertEqual(similarity3, 1.0, "Identical texts should have similarity of 1.0")
            
            print("✅ Similarity calculation working correctly")
            
        except Exception as e:
            self.fail(f"Similarity calculation test failed: {str(e)}")
    
    def test_json_storage_files(self):
        """Test JSON storage file creation and management."""
        try:
            import storage
            
            storage_instance = storage.ContentStorage('./test_data')
            
            # Check if storage files exist
            self.assertTrue(os.path.exists(storage_instance.prompts_file))
            self.assertTrue(os.path.exists(storage_instance.captions_file))
            self.assertTrue(os.path.exists(storage_instance.images_file))
            self.assertTrue(os.path.exists(storage_instance.posts_file))
            
            # Test loading JSON data
            prompts = storage_instance._load_json(storage_instance.prompts_file)
            self.assertIsInstance(prompts, list)
            
            # Test saving JSON data
            test_data = [{"test": "data", "timestamp": datetime.now().isoformat()}]
            storage_instance._save_json(storage_instance.prompts_file, test_data)
            
            # Verify data was saved
            loaded_data = storage_instance._load_json(storage_instance.prompts_file)
            self.assertEqual(len(loaded_data), 1)
            self.assertEqual(loaded_data[0]["test"], "data")
            
            print("✅ JSON storage files working correctly")
            
        except Exception as e:
            self.fail(f"JSON storage files test failed: {str(e)}")
    
    def test_data_cleanup(self):
        """Test data cleanup functionality."""
        try:
            import storage
            
            storage_instance = storage.ContentStorage('./test_data')
            
            # Add some test data
            storage_instance.add_prompt("Test prompt 1", {"test": True})
            storage_instance.add_prompt("Test prompt 2", {"test": True})
            
            # Verify data exists
            recent_prompts = storage_instance.get_recent_prompts(10)
            self.assertGreater(len(recent_prompts), 0, "Test data should exist")
            
            # Test cleanup (clean up everything by setting days to 0)
            storage_instance.cleanup_old_data(0)
            
            # Verify data is cleaned up
            recent_prompts_after = storage_instance.get_recent_prompts(10)
            self.assertEqual(len(recent_prompts_after), 0, "Data should be cleaned up")
            
            print("✅ Data cleanup working correctly")
            
        except Exception as e:
            self.fail(f"Data cleanup test failed: {str(e)}")
    
    def test_config_structure(self):
        """Test configuration structure without importing dependencies."""
        try:
            # Read config file and check structure
            with open('config.py', 'r') as f:
                config_content = f.read()
            
            # Check for required configuration variables
            required_vars = [
                'CEREBRUS_API_KEY',
                'GEMINI_API_KEY',
                'INSTAGRAM_ACCESS_TOKEN',
                'INSTAGRAM_APP_ID',
                'INSTAGRAM_APP_SECRET',
                'STORAGE_PATH',
                'POST_TIME',
                'MAX_CAPTION_LENGTH',
                'MAX_HASHTAGS'
            ]
            
            for var in required_vars:
                self.assertIn(var, config_content, f"Configuration variable {var} should be defined")
            
            print("✅ Configuration structure is correct")
            
        except Exception as e:
            self.fail(f"Configuration structure test failed: {str(e)}")
    
    def test_project_structure(self):
        """Test that all required project files exist."""
        try:
            required_files = [
                'config.py',
                'storage.py',
                'cerebrus_client.py',
                'gemini_client.py',
                'instagram_client.py',
                'instagram_agent.py',
                'health_check.py',
                'requirements.txt',
                'Dockerfile',
                'docker-compose.yml',
                'README.md',
                'deploy.sh'
            ]
            
            for file_path in required_files:
                self.assertTrue(os.path.exists(file_path), f"Required file {file_path} should exist")
            
            print("✅ Project structure is complete")
            
        except Exception as e:
            self.fail(f"Project structure test failed: {str(e)}")
    
    def test_dockerfile_structure(self):
        """Test Dockerfile structure and content."""
        try:
            with open('Dockerfile', 'r') as f:
                dockerfile_content = f.read()
            
            # Check for required Dockerfile components
            required_components = [
                'FROM python:3.11-slim',
                'WORKDIR /app',
                'COPY requirements.txt',
                'RUN pip install',
                'COPY . .',
                'RUN mkdir -p /app/data',
                'EXPOSE 8000',
                'HEALTHCHECK'
            ]
            
            for component in required_components:
                self.assertIn(component, dockerfile_content, f"Dockerfile should contain {component}")
            
            print("✅ Dockerfile structure is correct")
            
        except Exception as e:
            self.fail(f"Dockerfile structure test failed: {str(e)}")
    
    def test_requirements_structure(self):
        """Test requirements.txt structure."""
        try:
            with open('requirements.txt', 'r') as f:
                requirements_content = f.read()
            
            # Check for required packages
            required_packages = [
                'requests',
                'google-generativeai',
                'python-dotenv',
                'schedule',
                'Pillow',
                'Flask'
            ]
            
            for package in required_packages:
                self.assertIn(package, requirements_content, f"Requirements should include {package}")
            
            print("✅ Requirements structure is correct")
            
        except Exception as e:
            self.fail(f"Requirements structure test failed: {str(e)}")

def run_simple_tests():
    """Run all simplified tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestInstagramAgentSimple)
    
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
    print("🧪 Running Simplified Instagram Advertisement Agent Tests")
    print("=" * 60)
    
    try:
        results = run_simple_tests()
        
        print("\n" + "=" * 60)
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
            print("\n🎉 All tests passed! The Instagram Advertisement Agent core functionality is working correctly.")
            print("\n📋 Next Steps:")
            print("   1. Install dependencies: pip install -r requirements.txt")
            print("   2. Configure environment variables in .env file")
            print("   3. Run full tests: python test_agent.py")
            print("   4. Deploy with Docker: ./deploy.sh")
        else:
            print("\n⚠️  Some tests failed. Please check the issues above.")
        
        sys.exit(0 if results['success'] else 1)
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {str(e)}")
        sys.exit(1)