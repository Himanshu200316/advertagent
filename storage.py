"""JSON-based storage system for tracking content history and preventing duplicates."""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

class ContentStorage:
    """Manages JSON-based storage for content history and duplicate prevention."""
    
    def __init__(self, storage_path: str = "./data"):
        """Initialize the storage system."""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # Storage files
        self.prompts_file = self.storage_path / "prompts_history.json"
        self.captions_file = self.storage_path / "captions_history.json"
        self.images_file = self.storage_path / "images_history.json"
        self.posts_file = self.storage_path / "posts_history.json"
        
        # Initialize storage files if they don't exist
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize storage files with empty structures if they don't exist."""
        files = [
            self.prompts_file,
            self.captions_file,
            self.images_file,
            self.posts_file
        ]
        
        for file_path in files:
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump([], f, indent=2)
    
    def _load_json(self, file_path: Path) -> List[Dict]:
        """Load JSON data from file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_json(self, file_path: Path, data: List[Dict]):
        """Save JSON data to file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_prompt(self, prompt: str, metadata: Dict[str, Any] = None) -> bool:
        """Add a new prompt to history and check for duplicates."""
        prompts = self._load_json(self.prompts_file)
        
        # Check for duplicates
        if self._is_duplicate_prompt(prompt, prompts):
            return False
        
        # Add new prompt
        prompt_entry = {
            "id": len(prompts) + 1,
            "prompt": prompt,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        prompts.append(prompt_entry)
        self._save_json(self.prompts_file, prompts)
        return True
    
    def add_caption(self, caption: str, prompt_id: int, metadata: Dict[str, Any] = None) -> int:
        """Add a new caption to history."""
        captions = self._load_json(self.captions_file)
        
        caption_entry = {
            "id": len(captions) + 1,
            "prompt_id": prompt_id,
            "caption": caption,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        captions.append(caption_entry)
        self._save_json(self.captions_file, captions)
        return caption_entry["id"]
    
    def add_image(self, image_path: str, prompt_id: int, metadata: Dict[str, Any] = None) -> int:
        """Add a new image to history."""
        images = self._load_json(self.images_file)
        
        image_entry = {
            "id": len(images) + 1,
            "prompt_id": prompt_id,
            "image_path": image_path,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        images.append(image_entry)
        self._save_json(self.images_file, images)
        return image_entry["id"]
    
    def add_post(self, post_data: Dict[str, Any]) -> int:
        """Add a new post to history."""
        posts = self._load_json(self.posts_file)
        
        post_entry = {
            "id": len(posts) + 1,
            "timestamp": datetime.now().isoformat(),
            "post_data": post_data
        }
        
        posts.append(post_entry)
        self._save_json(self.posts_file, posts)
        return post_entry["id"]
    
    def _is_duplicate_prompt(self, prompt: str, prompts: List[Dict]) -> bool:
        """Check if a prompt is a duplicate based on similarity."""
        # Simple similarity check - can be enhanced with more sophisticated algorithms
        for existing_prompt in prompts:
            similarity = self._calculate_similarity(prompt, existing_prompt["prompt"])
            # Only consider it a duplicate if similarity is very high (0.9+) to avoid false positives
            if similarity > 0.9:
                return True
        return False
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (simple implementation)."""
        # Convert to lowercase and split into words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def get_recent_prompts(self, limit: int = 10) -> List[Dict]:
        """Get recent prompts."""
        prompts = self._load_json(self.prompts_file)
        return sorted(prompts, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_recent_captions(self, limit: int = 10) -> List[Dict]:
        """Get recent captions."""
        captions = self._load_json(self.captions_file)
        return sorted(captions, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_recent_posts(self, limit: int = 10) -> List[Dict]:
        """Get recent posts."""
        posts = self._load_json(self.posts_file)
        return sorted(posts, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up data older than specified days."""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        files = [self.prompts_file, self.captions_file, self.images_file, self.posts_file]
        
        for file_path in files:
            data = self._load_json(file_path)
            filtered_data = [
                item for item in data 
                if datetime.fromisoformat(item["timestamp"]).timestamp() > cutoff_date
            ]
            self._save_json(file_path, filtered_data)