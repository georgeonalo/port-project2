import requests

# Replace with your actual Port API token
ACCESS_TOKEN = 'YOUR_PORT_API_TOKEN_HERE'  # Replace with your actual Port API tokenzNjksImV4cCI6MTc1NDgzNDE2OX0.coTJFWW5RBLVFleVQWBQRuf568c3auTevmIC3Cft5fI'

# API configuration
API_URL = 'https://api.getport.io/v1'
blueprint_name = 'githubRepository'  # Change this if your blueprint has a different name

# Scorecard configuration
scorecards = [
    {
        'identifier': 'pr_management',
        'title': 'Pull Request Management',
        'rules': [
            {
                'identifier': 'gold_pr_count',
                'title': 'Excellent PR Management',
                'level': 'Gold',
                'query': {
                    'combinator': 'and',
                    'conditions': [
                        {
                            'operator': '<',
                            'property': 'open_prs_count',
                            'value': 5
                        }
                    ]
                }
            },
            {
                'identifier': 'silver_pr_count',
                'title': 'Good PR Management',
                'level': 'Silver',
                'query': {
                    'combinator': 'and',
                    'conditions': [
                        {
                            'operator': '>=',
                            'property': 'open_prs_count',
                            'value': 5
                        },
                        {
                            'operator': '<',
                            'property': 'open_prs_count',
                            'value': 10
                        }
                    ]
                }
            },
            {
                'identifier': 'bronze_pr_count',
                'title': 'Acceptable PR Management',
                'level': 'Bronze',
                'query': {
                    'combinator': 'and',
                    'conditions': [
                        {
                            'operator': '>=',
                            'property': 'open_prs_count',
                            'value': 10
                        },
                        {
                            'operator': '<',
                            'property': 'open_prs_count',
                            'value': 15
                        }
                    ]
                }
            }
        ]
    }
]

# API request headers
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# Create the scorecard
print("Creating scorecard...")
response = requests.put(
    f'{API_URL}/blueprints/{blueprint_name}/scorecards',
    json=scorecards,
    headers=headers
)

if response.status_code == 200:
    print("✅ Scorecard created successfully!")
    print("You can now see it in your Port dashboard under the repository entities.")
else:
    print(f"❌ Error creating scorecard: {response.status_code}")
    print(f"Response: {response.text}")