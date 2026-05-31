import requests
import json

BASE_URL = "http://127.0.0.1:8000/app2/"

def test_api():
    print("=== Testing ReviewSphere API ===\n")
    
    # First check if server is running
    print("1. Checking server connectivity...")
    try:
        test = requests.get("http://127.0.0.1:8000/app2/reviews/", timeout=3)
        print(f"   Server status: {test.status_code}")
    except:
        print("   ❌ Server not running!")
        print("   Run: python manage.py runserver")
        return
    
    # Test POST to create review
    print("\n2. Creating a new review via API...")
    review_data = {
        "title": "Inception - Mind Blowing",
        "content": "Christopher Nolan's masterpiece with amazing visuals and plot.",
        "author": "API User",
        "review_type": "movie",
        "sentiment": "positive"
    }
    
    try:
        post_response = requests.post(f"{BASE_URL}reviews/", json=review_data)
        print(f"   POST Status: {post_response.status_code}")
        
        if post_response.status_code in [200, 201]:
            print(f"   Response: {post_response.json()}")
        else:
            print(f"   Error: {post_response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test GET all reviews
    print("\n3. Fetching all reviews via API...")
    try:
        get_response = requests.get(f"{BASE_URL}reviews/")
        print(f"   GET Status: {get_response.status_code}")
        
        if get_response.status_code == 200:
            data = get_response.json()
            print(f"   Found {len(data)} review(s):")
            for i, review in enumerate(data, 1):
                print(f"   {i}. {review.get('title', 'No title')} - {review.get('sentiment', 'Unknown')}")
        else:
            print(f"   Response: {get_response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n=== API Testing Complete ===")

if __name__ == "__main__":
    test_api()

