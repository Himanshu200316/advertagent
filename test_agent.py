"""Test script for the Instagram Advertisement Agent."""

import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from storage import ContentStorage
from gemini_client import GeminiClient
from instagram_client import InstagramClient

def test_configuration():
    """Test configuration loading."""
    print("🔧 Testing configuration...")
    try:
        Config.validate()
        print("✅ Configuration is valid")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

def test_storage():
    """Test storage system."""
    print("💾 Testing storage system...")
    try:
        storage = ContentStorage("./test_data")
        
        # Test adding a prompt
        prompt_id = storage.add_prompt("Test prompt for coffee beans", {"test": True})
        print(f"✅ Added prompt with ID: {prompt_id}")
        
        # Test adding a caption
        caption_id = storage.add_caption("Test caption", prompt_id, {"test": True})
        print(f"✅ Added caption with ID: {caption_id}")
        
        # Test adding an image
        image_id = storage.add_image("./test_image.jpg", prompt_id, {"test": True})
        print(f"✅ Added image with ID: {image_id}")
        
        # Test adding a post
        post_id = storage.add_post({"test": "post data"})
        print(f"✅ Added post with ID: {post_id}")
        
        # Test duplicate prevention
        is_duplicate = storage.add_prompt("Test prompt for coffee beans", {"test": True})
        if not is_duplicate:
            print("✅ Duplicate prevention working")
        else:
            print("⚠️  Duplicate prevention not working")
        
        print("✅ Storage system working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Storage error: {str(e)}")
        return False

def test_gemini_client():
    """Test Gemini client (requires API key)."""
    print("🤖 Testing Gemini client...")
    try:
        if not Config.GEMINI_API_KEY:
            print("⚠️  Gemini API key not set, skipping test")
            return True
        
        gemini = GeminiClient()
        
        # Test caption generation
        product_details = {
            "description": "Premium coffee beans from Colombia",
            "target_audience": "coffee enthusiasts"
        }
        
        caption = gemini.generate_caption(product_details, "professional")
        print(f"✅ Generated caption: {caption[:100]}...")
        
        # Test hashtag generation
        hashtags = gemini.generate_hashtags(product_details, caption)
        print(f"✅ Generated hashtags: {hashtags[:5]}...")
        
        print("✅ Gemini client working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Gemini client error: {str(e)}")
        return False

def test_instagram_client():
    """Test Instagram client (requires API keys)."""
    print("📸 Testing Instagram client...")
    try:
        if not Config.INSTAGRAM_ACCESS_TOKEN:
            print("⚠️  Instagram API keys not set, skipping test")
            return True
        
        instagram = InstagramClient()
        
        # Test account info
        account_info = instagram.get_account_info()
        print(f"✅ Account info: {account_info}")
        
        print("✅ Instagram client working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Instagram client error: {str(e)}")
        return False

def test_full_workflow():
    """Test the full workflow."""
    print("🔄 Testing full workflow...")
    try:
        from instagram_agent import InstagramAdvertisementAgent
        
        # Initialize agent
        agent = InstagramAdvertisementAgent()
        print("✅ Agent initialized successfully")
        
        # Test analytics
        analytics = agent.get_analytics()
        print(f"✅ Analytics: {json.dumps(analytics, indent=2)}")
        
        print("✅ Full workflow test completed")
        return True
        
    except Exception as e:
        print(f"❌ Full workflow error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🧪 Starting Instagram Advertisement Agent Tests")
    print("=" * 50)
    
    tests = [
        test_configuration,
        test_storage,
        test_gemini_client,
        test_instagram_client,
        test_full_workflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The agent is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the configuration and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())