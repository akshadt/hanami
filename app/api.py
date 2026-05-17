import requests

JIKAN_BASE_URL = "https://api.jikan.moe/v4"

def search_anime(query, limit=5):
    """
    Search for anime using Jikan API.
    Returns a list of dictionaries with extracted information.
    Handles exceptions to prevent app crashes.
    """
    try:
        url = f"{JIKAN_BASE_URL}/anime"
        params = {"q": query, "limit": limit}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('data', []):
            anime_data = {
                'mal_id': item.get('mal_id'),
                'title': item.get('title'),
                'synopsis': item.get('synopsis'),
                'image_url': item.get('images', {}).get('jpg', {}).get('large_image_url'),
                'rating': item.get('score') or 'N/A'
            }
            # Stringify score if it's a number
            if isinstance(anime_data['rating'], (int, float)):
                anime_data['rating'] = str(anime_data['rating'])
                
            results.append(anime_data)
        return results
    except Exception as e:
        print(f"Error fetching from Jikan API: {e}")
        return []

def get_anime_details(mal_id):
    """
    Fetch details for a specific anime by ID if needed.
    """
    try:
        url = f"{JIKAN_BASE_URL}/anime/{mal_id}/full"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json().get('data', {})
        
        return {
            'mal_id': data.get('mal_id'),
            'title': data.get('title'),
            'synopsis': data.get('synopsis'),
            'image_url': data.get('images', {}).get('jpg', {}).get('large_image_url'),
            'rating': str(data.get('score') or 'N/A')
        }
    except Exception as e:
        print(f"Error fetching details from Jikan API: {e}")
        return None
