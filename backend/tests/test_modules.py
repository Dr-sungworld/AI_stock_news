import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.news_fetcher import fetch_news
from modules.ai_analyzer import analyze_news

class TestModules(unittest.TestCase):

    @patch('modules.news_fetcher.requests.post')
    def test_fetch_news_success(self, mock_post):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "news": [
                {"title": "Test News", "link": "http://test.com"}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        results = fetch_news("test query")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Test News")

    @patch('modules.news_fetcher.requests.post')
    def test_fetch_news_failure(self, mock_post):
        # Mock failure
        mock_post.side_effect = Exception("API Error")
        
        results = fetch_news("test query")
        self.assertEqual(results, [])

    @patch('modules.ai_analyzer._call_gemini_api')
    def test_analyze_news_low_importance(self, mock_gemini):
        # Mock Gemini response for Step 1
        mock_gemini.return_value = '''
        {
            "importance": "Low",
            "reason": "Not important",
            "themes": [],
            "search_query": ""
        }
        '''
        
        news_item = {"title": "Boring News", "snippet": "Nothing happened"}
        result = analyze_news(news_item)
        
        self.assertEqual(result['importance'], "Low")
        self.assertEqual(result['historical_reaction'], "N/A (Low Importance)")

if __name__ == '__main__':
    unittest.main()
