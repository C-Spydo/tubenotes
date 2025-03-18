import os
import googleapiclient.discovery
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

class YouTubeVideoFinder:
    """
    A class to handle searching and retrieving YouTube videos.
    """
    
    def __init__(self):
        """Initialize the YouTube API client."""
        # Get API key from environment variable
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY environment variable not set")
            
        # Initialize the YouTube API client
        api_service_name = "youtube"
        api_version = "v3"
        self.youtube = googleapiclient.discovery.build(
            api_service_name, 
            api_version, 
            developerKey=self.api_key
        )
    
    def search_video(self, query, max_results=5):
        """
        Search for YouTube videos based on a query.
        
        Args:
            query (str): The search query (video title or description)
            max_results (int): Maximum number of results to return
            
        Returns:
            list: A list of video information dictionaries
        """
        try:
            # Call the search.list method to retrieve search results
            search_response = self.youtube.search().list(
                q=query,
                part="snippet",
                maxResults=max_results,
                type="video"  # Only search for videos, not playlists or channels
            ).execute()
            
            # Extract relevant information from search results
            videos = []
            for search_result in search_response.get("items", []):
                video_id = search_result["id"]["videoId"]
                video_info = {
                    "id": video_id,
                    "title": search_result["snippet"]["title"],
                    "channel": search_result["snippet"]["channelTitle"],
                    "publish_date": search_result["snippet"]["publishedAt"],
                    "description": search_result["snippet"]["description"],
                    "thumbnail": search_result["snippet"]["thumbnails"]["high"]["url"],
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                }
                videos.append(video_info)
                
            return videos
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    
    def get_video_details(self, video_id):
        """
        Get detailed information about a specific video.
        
        Args:
            video_id (str): The YouTube video ID
            
        Returns:
            dict: Detailed information about the video
        """
        try:
            # Call the videos.list method to retrieve video details
            video_response = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            ).execute()
            
            # Extract video information
            if not video_response.get("items"):
                return None
                
            video_data = video_response["items"][0]
            snippet = video_data["snippet"]
            content_details = video_data["contentDetails"]
            statistics = video_data["statistics"]
            
            # Format detailed video information
            video_details = {
                "id": video_id,
                "title": snippet["title"],
                "channel": snippet["channelTitle"],
                "publish_date": snippet["publishedAt"],
                "description": snippet["description"],
                "duration": content_details["duration"],
                "view_count": statistics.get("viewCount", 0),
                "like_count": statistics.get("likeCount", 0),
                "comment_count": statistics.get("commentCount", 0),
                "url": f"https://www.youtube.com/watch?v={video_id}"
            }
            
            return video_details
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
            
    def find_best_match(self, query):
        """
        Find the best matching video for a given query.
        
        Args:
            query (str): The search query (video title or description)
            
        Returns:
            dict: Information about the best matching video
        """
        videos = self.search_video(query, max_results=3)
        
        if not videos:
            return None
            
        # For now, simply return the top search result
        # In a more advanced implementation, we could use relevance scoring
        best_match = videos[0]
        
        # Get additional details for the best match
        detailed_info = self.get_video_details(best_match["id"])
        
        return detailed_info


# Example usage
if __name__ == "__main__":
    finder = YouTubeVideoFinder()
    
    # Example: Search for a specific video
    query = "Love in Every Word Omoni Oboli"
    result = finder.find_best_match(query)
    
    if result:
        print(json.dumps(result, indent=2))
    else:
        print(f"No results found for '{query}'")