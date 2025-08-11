import requests

# Your Port API token (same as before)
ACCESS_TOKEN = 'YOUR_PORT_API_TOKEN_HERE'  # Replace with your actual Port API token4MDQsImV4cCI6MTc1NDg5MjYwNH0.tWSwkDvYbCvmPCtVlXDzExndYuDwxxs3ApRVczF1mzE'

API_URL = 'https://api.getport.io/v1'
blueprint_name = 'githubRepository'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# Test entities with different PR counts to test all scorecard levels
test_entities = [
    {
        "identifier": "test-repo-gold",
        "title": "Test Repository (Gold)",
        "properties": {
            "name": "test-repo-gold",
            "url": "https://github.com/georgeonalo/test-repo-gold",
            "language": "Python",
            "open_prs_count": 2  # Should get Gold (< 5 PRs)
        }
    },
    {
        "identifier": "test-repo-silver", 
        "title": "Test Repository (Silver)",
        "properties": {
            "name": "test-repo-silver",
            "url": "https://github.com/georgeonalo/test-repo-silver", 
            "language": "JavaScript",
            "open_prs_count": 7  # Should get Silver (5-9 PRs)
        }
    },
    {
        "identifier": "test-repo-bronze",
        "title": "Test Repository (Bronze)", 
        "properties": {
            "name": "test-repo-bronze",
            "url": "https://github.com/georgeonalo/test-repo-bronze",
            "language": "Java", 
            "open_prs_count": 12  # Should get Bronze (10-14 PRs)
        }
    },
    {
        "identifier": "port-project2",
        "title": "Port Project 2",
        "properties": {
            "name": "port-project2",
            "url": "https://github.com/georgeonalo/port-project2",
            "language": "Python",
            "open_prs_count": 1  # 1 open PR - should get GOLD
        }
    },
    {
        "identifier": "docker-projects",
        "title": "Docker Projects", 
        "properties": {
            "name": "docker-projects",
            "url": "https://github.com/georgeonalo/docker-projects",
            "language": "Docker",
            "open_prs_count": 1  # 1 open PR - should get GOLD
        }
    }
]

def create_entity(entity_data):
    """Create a repository entity in Port"""
    url = f'{API_URL}/blueprints/{blueprint_name}/entities'
    
    response = requests.post(url, json=entity_data, headers=headers)
    
    if response.status_code in [200, 201]:
        print(f"✅ Created entity: {entity_data['identifier']}")
        return True
    else:
        print(f"❌ Failed to create entity {entity_data['identifier']}: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def update_entity(entity_id, properties):
    """Update an existing entity's properties"""
    url = f'{API_URL}/blueprints/{blueprint_name}/entities/{entity_id}'
    
    payload = {"properties": properties}
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Updated entity: {entity_id}")
        return True
    else:
        print(f"❌ Failed to update entity {entity_id}: {response.status_code}")
        print(f"Response: {response.text}")
        return False

# Create test entities
print("Creating test entities to test the scorecard...")
print("=" * 50)

for entity in test_entities:
    create_entity(entity)

print("\n" + "=" * 50)
print("🎉 Test entities created!")
print("\nNow go to your Port dashboard and:")
print("1. Navigate to any of the repository entities")
print("2. Click on the 'Scorecards' tab")
print("3. You should see the 'Pull Request Management' scorecard")
print("4. Check the scores:")
print("   - test-repo-gold (2 PRs) → Should show GOLD")
print("   - test-repo-silver (7 PRs) → Should show SILVER") 
print("   - test-repo-bronze (12 PRs) → Should show BRONZE")
print("   - your-actual-repo (2 PRs) → Should show GOLD")

print("\n💡 If you want to test different PR counts, run:")
print("python3 update_pr_count.py")