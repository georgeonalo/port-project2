import requests

# Your Port API token
ACCESS_TOKEN = 'YOUR_PORT_API_TOKEN_HERE'  # Replace with your actual Port API token1NDEsImV4cCI6MTc1NDc2NTM0MX0.Q1eKZF7LwKTS7K-YiEiNMVsLoQ3fomJiYdEkxiAsR5c'

API_URL = 'https://api.getport.io/v1'
blueprint_name = 'githubRepository'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def update_pr_count(entity_id, new_count):
    """Update the open_prs_count for an entity"""
    url = f'{API_URL}/blueprints/{blueprint_name}/entities/{entity_id}'
    
    payload = {
        "properties": {
            "open_prs_count": new_count
        }
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Updated {entity_id} to {new_count} open PRs")
        
        # Determine expected scorecard level
        if new_count < 5:
            level = "GOLD"
        elif new_count < 10:
            level = "SILVER"
        elif new_count < 15:
            level = "BRONZE"
        else:
            level = "NO SCORE (>= 15 PRs)"
            
        print(f"   Expected scorecard level: {level}")
        return True
    else:
        print(f"❌ Failed to update {entity_id}: {response.status_code}")
        print(f"Response: {response.text}")
        return False

# Interactive testing
print("🧪 Scorecard Testing Tool")
print("=" * 30)

while True:
    print("\nAvailable entities:")
    print("1. test-repo-gold")
    print("2. test-repo-silver") 
    print("3. test-repo-bronze")
    print("4. port-project2")
    print("5. docker-projects")
    print("6. Exit")
    
    choice = input("\nSelect entity to update (1-5): ").strip()
    
    if choice == '6':
        print("👋 Goodbye!")
        break
        
    entity_map = {
        '1': 'test-repo-gold',
        '2': 'test-repo-silver',
        '3': 'test-repo-bronze', 
        '4': 'port-project2',
        '5': 'docker-projects'
    }
    
    if choice in entity_map:
        entity_id = entity_map[choice]
        
        try:
            new_count = int(input(f"Enter new PR count for {entity_id}: ").strip())
            if new_count < 0:
                print("❌ PR count must be >= 0")
                continue
                
            update_pr_count(entity_id, new_count)
            print(f"\n💡 Go to Port dashboard → {entity_id} → Scorecards tab to see the updated score!")
            
        except ValueError:
            print("❌ Please enter a valid number")
    else:
        print("❌ Invalid choice")