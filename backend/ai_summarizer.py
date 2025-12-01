import os
import json
import logging
from typing import Optional, List, Tuple
from openai import OpenAI

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class AISummarizer:
    def __init__(self):
        if not OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set - AI summaries will be disabled")
            self.client = None
        else:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def generate_summary(
        self, 
        title: str, 
        content: str, 
        source_name: str,
        max_content_length: int = 4000
    ) -> Tuple[Optional[str], Optional[List[str]]]:
        if not self.client:
            return None, None
        
        if not content or len(content.strip()) < 100:
            return None, None
        
        truncated_content = content[:max_content_length]
        if len(content) > max_content_length:
            truncated_content += "..."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a tech news summarizer. Given an article, provide:
1. A concise 2-sentence TL;DR summary
2. 3-5 key points as bullet points

Respond in JSON format:
{
  "summary": "Two sentence summary here.",
  "key_points": ["Point 1", "Point 2", "Point 3"]
}

Be concise, factual, and focus on the most important information.
For research papers, highlight the main contribution and findings.
For news, focus on the key facts and implications."""
                    },
                    {
                        "role": "user",
                        "content": f"""Article Title: {title}
Source: {source_name}

Content:
{truncated_content}"""
                    }
                ],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            summary = result.get("summary", "")
            key_points = result.get("key_points", [])
            
            if summary and len(summary) > 10:
                logger.info(f"Generated summary for: {title[:50]}...")
                return summary, key_points
            
            return None, None
            
        except Exception as e:
            logger.error(f"Failed to generate summary for '{title[:50]}': {str(e)}")
            return None, None
    
    def generate_summary_from_title_only(
        self, 
        title: str, 
        source_name: str
    ) -> Tuple[Optional[str], Optional[List[str]]]:
        if not self.client:
            return None, None
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """Based on the article title and source, provide a brief description of what this article likely covers.

Respond in JSON format:
{
  "summary": "Brief one-sentence description based on the title.",
  "key_points": []
}

Be concise and don't make up specific details not implied by the title."""
                    },
                    {
                        "role": "user",
                        "content": f"""Article Title: {title}
Source: {source_name}"""
                    }
                ],
                temperature=0.3,
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            summary = result.get("summary", "")
            
            if summary and len(summary) > 10:
                return summary, []
            
            return None, None
            
        except Exception as e:
            logger.error(f"Failed to generate title-based summary: {str(e)}")
            return None, None


summarizer = AISummarizer()


def generate_article_summary(
    title: str, 
    content: Optional[str], 
    source_name: str
) -> Tuple[Optional[str], Optional[List[str]]]:
    if content and len(content.strip()) > 100:
        return summarizer.generate_summary(title, content, source_name)
    else:
        return summarizer.generate_summary_from_title_only(title, source_name)

