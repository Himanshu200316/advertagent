"""Health check endpoint for the Instagram Advertisement Agent."""

from flask import Flask, jsonify
import os
import json
from datetime import datetime
from config import Config

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint."""
    try:
        # Check if data directory exists
        data_dir = Config.STORAGE_PATH
        if not os.path.exists(data_dir):
            return jsonify({
                "status": "unhealthy",
                "message": "Data directory not found",
                "timestamp": datetime.now().isoformat()
            }), 500
        
        # Check if storage files exist
        storage_files = [
            "prompts_history.json",
            "captions_history.json", 
            "images_history.json",
            "posts_history.json"
        ]
        
        for file_name in storage_files:
            file_path = os.path.join(data_dir, file_name)
            if not os.path.exists(file_path):
                return jsonify({
                    "status": "unhealthy",
                    "message": f"Storage file {file_name} not found",
                    "timestamp": datetime.now().isoformat()
                }), 500
        
        # Check API configurations
        required_configs = [
            'CEREBRUS_API_KEY',
            'GEMINI_API_KEY', 
            'INSTAGRAM_ACCESS_TOKEN',
            'INSTAGRAM_APP_ID',
            'INSTAGRAM_APP_SECRET'
        ]
        
        missing_configs = []
        for config in required_configs:
            if not getattr(Config, config):
                missing_configs.append(config)
        
        if missing_configs:
            return jsonify({
                "status": "unhealthy",
                "message": f"Missing configuration: {', '.join(missing_configs)}",
                "timestamp": datetime.now().isoformat()
            }), 500
        
        return jsonify({
            "status": "healthy",
            "message": "All systems operational",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        })
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "message": f"Health check failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/status')
def status():
    """Detailed status endpoint."""
    try:
        from storage import ContentStorage
        
        storage = ContentStorage(Config.STORAGE_PATH)
        
        # Get recent activity
        recent_prompts = storage.get_recent_prompts(5)
        recent_captions = storage.get_recent_captions(5)
        recent_posts = storage.get_recent_posts(5)
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "storage": {
                "prompts_count": len(recent_prompts),
                "captions_count": len(recent_captions),
                "posts_count": len(recent_posts)
            },
            "recent_activity": {
                "prompts": recent_prompts,
                "captions": recent_captions,
                "posts": recent_posts
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Status check failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)