import pytest
import requests

BASE_URL = "https://ovcharski.com/shop/"

def test_get_website_title():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert "Automation Demo Site &#8211; Website for demo purposes." in response.text

def test_get_pages():
    response = requests.get(BASE_URL + "/wp-json/wp/v2/pages?_fields=id,link,slug")
    assert response.status_code == 200

    # Parse the response body as JSON
    body = response.json()

    # Check that the body is an array
    assert isinstance(body, list)

def test_get_categories():
    # Make GET request with query parameters
    response = requests.get(
        f"{BASE_URL}/wp-json/wp/v2/categories",
        params={'_fields': 'id,name,slug'}
    )
    assert response.status_code == 200

    # Parse JSON response
    categories = response.json()

    # Verify response is a list
    assert isinstance(categories, list)

    # If categories exist, verify structure of first item
    if categories:
        first_category = categories[0]
        assert 'id' in first_category
        assert 'name' in first_category
        assert 'slug' in first_category

def test_get_specific_post():
    post_id = 147 # Calid Post ID
    expected_slug = "how-to-blog-post"
    
    # Make GET request for specific post
    response = requests.get(f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}")

    # Check for 404 before proceeding
    if response.status_code == 404:
        pytest.skip(f"Post {post_id} not found")
    
    # Parse JSON response
    post_data = response.json()
    
    # Verify post properties
    assert post_data['id'] == post_id

    assert post_data['slug'] == expected_slug
    assert post_data['type'] == 'post'

def test_get_invalid_post_id_returns_404():
    invalid_post_id = 2255  # Known invalid ID
    response = requests.get(f"{BASE_URL}/wp-json/wp/v2/posts/{invalid_post_id}")
    
    # Directly assert the expected 404 status
    assert response.status_code == 404, f"Expected 404 for invalid post ID {invalid_post_id}"
    
    # Verify error response structure if API returns JSON errors
    error_data = response.json()
    assert error_data.get("code") == "rest_post_invalid_id"
    assert "Invalid post ID" in error_data.get("message", "")

import pytest

@pytest.mark.parametrize("post_id, expected_status", [
    (147, 200),        # Valid post ID
    (2255, 404),       # Invalid post ID
    ("string", 404),   # Non-numeric ID
])
def test_post_id_validation(post_id, expected_status):
    response = requests.get(f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}")
    assert response.status_code == expected_status
    
    if expected_status == 200:
        data = response.json()
        assert data['id'] == post_id
    else:
        error = response.json()
        assert "code" in error
        assert "message" in error

def test_get_post_comments():
    post_id = 1 # Valid post ID with comments. Note: Should investigate does the test really work
    response = requests.get(
        f"{BASE_URL}/wp-json/wp/v2/comments",
        params={'post': post_id}
    )
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}"
    
    # Parse and verify response structure
    comments = response.json()
    assert isinstance(comments, list), \
        "Response should be a list of comments"
    
    # Verify comment structure if comments exist
    if comments:
        first_comment = comments[0]
        assert 'id' in first_comment
        assert 'content' in first_comment
        assert 'post' in first_comment
        assert first_comment['post'] == post_id

def test_get_media_items():
    """Verify media items endpoint returns valid structure"""
    # Make request with query parameters
    response = requests.get(
        f"{BASE_URL}/wp-json/wp/v2/media",
        params={'_fields': 'id,source_url,alt_text'}
    )
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}"
    media_items = response.json()
    assert isinstance(media_items, list), \
        "Response should be a list of media items"
    
    # Validate fields if any media items exist
    if media_items:
        first_media = media_items[0]
        required_fields = {'id', 'source_url', 'alt_text'}
        
        # Verify all required fields exist
        missing_fields = required_fields - set(first_media.keys())
        assert not missing_fields, \
            f"Missing fields in media item: {missing_fields}"

        # Additional type checks
        assert isinstance(first_media['id'], int), "ID should be integer"
        assert isinstance(first_media['source_url'], str), "URL should be string"
        assert isinstance(first_media['alt_text'], str), "Alt text should be string"

def test_search_posts():
    search_term = "hello"
    expected_slug = "hello-world"
    expected_id = 1
    expected_link = "https://ovcharski.com/shop/hello-world/"

    # Make GET request with query parameters
    response = requests.get(
        f"{BASE_URL}/wp-json/wp/v2/posts",
        params={
            'search': search_term,
            '_fields': 'id,link,slug'
        }
    )
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}"
    posts = response.json()
    assert isinstance(posts, list), \
        "Response should be a list of posts"

    # Search for specific post if results exist
    if posts:
        # Find first post matching expected slug
        found_post = next(
            (p for p in posts if p.get('slug') == expected_slug),
            None
        )
        
        # Verify post exists in results
        assert found_post is not None, \
            f"Post with slug '{expected_slug}' not found in search results"

        # Validate post properties
        assert found_post['id'] == expected_id, \
            f"Expected ID {expected_id}, got {found_post['id']}"
            
        assert found_post['link'] == expected_link, \
            f"Expected link '{expected_link}', got '{found_post['link']}'"

        # Additional type validations
        assert isinstance(found_post['id'], int), "ID should be integer"
        assert isinstance(found_post['slug'], str), "Slug should be string"
        assert found_post['link'].startswith('http'), "Link should be valid URL"

def test_get_users():
    """Verify users endpoint returns valid user data structure"""
    response = requests.get(
        f"{BASE_URL}/wp-json/wp/v2/users",
        params={'_fields': 'id,name,slug'}
    )
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}"
    users = response.json()
    assert isinstance(users, list), \
        "Response should be a list of user objects"
    
    # Validate user object structure if users exist
    if users:
        first_user = users[0]
        required_fields = {'id', 'name', 'slug'}
        
        # Check for presence of all required fields
        missing_fields = required_fields - set(first_user.keys())
        assert not missing_fields, \
            f"Missing fields in user object: {missing_fields}"

        # Additional type validations (optional)
        assert isinstance(first_user['id'], int), "User ID should be integer"
        assert isinstance(first_user['name'], str), "Name should be string"
        assert isinstance(first_user['slug'], str), "Slug should be string"

        # Content validation for first user (optional)
        assert first_user['id'] > 0, "User ID should be positive integer"
        assert len(first_user['name']) > 0, "Name should not be empty"
        assert len(first_user['slug']) > 0, "Slug should not be empty"