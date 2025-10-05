"""Gemini API client for content generation."""

import google.generativeai as genai
from typing import Dict, Any, List, Optional
from config import Config
import base64
import io
from PIL import Image

class GeminiClient:
    """Client for interacting with the Gemini API for content generation."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        self.api_key = Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        
        # Initialize models
        self.text_model = genai.GenerativeModel('gemini-pro')
        self.image_model = genai.GenerativeModel('gemini-pro-vision')
    
    def generate_caption(self, product_details: Dict[str, Any], tone: str = "professional") -> str:
        """Generate an engaging Instagram caption based on product details."""
        try:
            prompt = self._build_caption_prompt(product_details, tone)
            
            response = self.text_model.generate_content(prompt)
            
            if response.text:
                # Clean up the response
                caption = response.text.strip()
                
                # Ensure caption length is within Instagram limits
                if len(caption) > Config.MAX_CAPTION_LENGTH:
                    caption = caption[:Config.MAX_CAPTION_LENGTH-3] + "..."
                
                return caption
            else:
                raise Exception("No caption generated")
                
        except Exception as e:
            raise Exception(f"Failed to generate caption: {str(e)}")
    
    def generate_image(self, product_details: Dict[str, Any], style: str = "modern") -> str:
        """Generate an AI-based ad image using Gemini."""
        try:
            prompt = self._build_image_prompt(product_details, style)
            
            # Generate image using text-to-image (this would need to be adapted based on actual Gemini capabilities)
            # For now, we'll simulate image generation
            response = self.text_model.generate_content(prompt)
            
            # In a real implementation, this would generate an actual image
            # For now, we'll return a placeholder path
            image_path = f"./generated_images/image_{hash(prompt)}.jpg"
            
            # Create the image directory if it doesn't exist
            import os
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # Create a placeholder image (in production, this would be the actual generated image)
            self._create_placeholder_image(image_path, product_details)
            
            return image_path
            
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")
    
    def generate_hashtags(self, product_details: Dict[str, Any], caption: str) -> List[str]:
        """Generate relevant hashtags for the post."""
        try:
            prompt = f"""
            Generate {Config.MAX_HASHTAGS} relevant hashtags for an Instagram post about:
            Product: {product_details.get('description', '')}
            Target Audience: {product_details.get('target_audience', '')}
            Caption: {caption}
            
            Return only the hashtags, one per line, without the # symbol.
            """
            
            response = self.text_model.generate_content(prompt)
            
            if response.text:
                hashtags = [
                    f"#{tag.strip()}" 
                    for tag in response.text.strip().split('\n') 
                    if tag.strip()
                ]
                return hashtags[:Config.MAX_HASHTAGS]
            else:
                return []
                
        except Exception as e:
            print(f"Failed to generate hashtags: {str(e)}")
            return []
    
    def _build_caption_prompt(self, product_details: Dict[str, Any], tone: str) -> str:
        """Build a prompt for caption generation."""
        description = product_details.get('description', '')
        target_audience = product_details.get('target_audience', '')
        
        tone_instructions = {
            "professional": "Write in a professional, business-like tone",
            "casual": "Write in a casual, friendly tone",
            "friendly": "Write in a warm, approachable tone",
            "energetic": "Write in an energetic, exciting tone"
        }
        
        tone_instruction = tone_instructions.get(tone, tone_instructions["professional"])
        
        prompt = f"""
        {tone_instruction} for an Instagram advertisement.
        
        Product/Service: {description}
        Target Audience: {target_audience}
        
        Create an engaging Instagram caption that:
        1. Captures attention in the first line
        2. Describes the product/service benefits
        3. Includes a call-to-action
        4. Is optimized for Instagram engagement
        5. Stays within {Config.MAX_CAPTION_LENGTH} characters
        
        Make it compelling and authentic.
        """
        
        return prompt
    
    def _build_image_prompt(self, product_details: Dict[str, Any], style: str) -> str:
        """Build a prompt for image generation."""
        description = product_details.get('description', '')
        target_audience = product_details.get('target_audience', '')
        
        style_instructions = {
            "modern": "modern, clean, minimalist design",
            "vintage": "vintage, retro aesthetic",
            "luxury": "luxury, premium, high-end look",
            "playful": "fun, colorful, playful design"
        }
        
        style_instruction = style_instructions.get(style, style_instructions["modern"])
        
        prompt = f"""
        Create a high-quality Instagram advertisement image for:
        Product: {description}
        Target Audience: {target_audience}
        Style: {style_instruction}
        
        The image should be:
        - Instagram-ready (square format, high resolution)
        - Visually appealing and professional
        - Relevant to the product description
        - Optimized for social media engagement
        """
        
        return prompt
    
    def _create_placeholder_image(self, image_path: str, product_details: Dict[str, Any]):
        """Create a placeholder image (in production, this would be replaced with actual AI-generated image)."""
        try:
            # Create a simple placeholder image
            img = Image.new('RGB', (1080, 1080), color='lightblue')
            
            # Add some text to the image
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            
            # Try to use a default font
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            text = product_details.get('description', 'Product Advertisement')[:50]
            draw.text((50, 500), text, fill='black', font=font)
            
            img.save(image_path)
            
        except Exception as e:
            print(f"Failed to create placeholder image: {str(e)}")
            # Create a simple colored rectangle as fallback
            img = Image.new('RGB', (1080, 1080), color='lightgray')
            img.save(image_path)
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze an uploaded image to understand its content."""
        try:
            with open(image_path, 'rb') as image_file:
                image = Image.open(image_file)
                
                response = self.image_model.generate_content([
                    "Analyze this image and describe what you see. Focus on:",
                    "1. Main subject/object",
                    "2. Colors and mood",
                    "3. Style and composition",
                    "4. Potential for Instagram advertising"
                ], image)
                
                return {
                    "description": response.text,
                    "analysis": "Image analysis completed"
                }
                
        except Exception as e:
            raise Exception(f"Failed to analyze image: {str(e)}")