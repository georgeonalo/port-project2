# Port Assignment Solutions

## Exercise #1: JQ Pattern Solutions

### 1. Kubernetes Deployment Data Extraction

**Given the K8s deployment object snippet, provide JQ patterns that extract:**

#### a. Current Replica Count
```bash
jq '.spec.replicas' k8s-deploy.json
```
**Output**: `1`

![alt text](<Screenshot 2025-09-01 at 04.28.33.png>)

**Explanation**: This pattern uses the dot (`.`) operator, which is fundamental in JQ for navigating JSON objects. Here, `.` refers to the root of the JSON, `.spec` accesses the `spec` object, and `.spec.replicas` extracts the `replicas` field. This allows you to flexibly extract, transform, and combine data from complex JSON structures.

#### b. Deployment Strategy
```bash
jq '.spec.strategy.type' k8s-deploy.json
```
**Output**: `"RollingUpdate"`

![alt text](<Screenshot 2025-09-01 at 04.29.03.png>)

**Explanation**: The dot operator is used to access nested fields: `.spec.strategy.type` means start at the root, go into `spec`, then `strategy`, then get the `type` field. Chaining fields with the dot operator lets you traverse deeper into the hierarchy and extract specific values.

#### c. Service-Environment Label Concatenation
```bash
jq -r '(.metadata.labels.service + "-" + .metadata.labels.environment)' k8s-deploy.json
```
**Output**: `authorization-production-gcp-1`

![alt text](<Screenshot 2025-09-01 at 04.29.55.png>)

**Explanation**: This pattern uses the dot operator to access two label fields inside the `metadata.labels` object. Parentheses group the two field accesses and the string concatenation operation. The `-r` flag outputs the result as raw text. This demonstrates how JQ can combine values from different parts of a JSON object using the dot operator and string operations.




### 2. Jira Subtask Issue IDs Extraction

**Given the Jira API issue response, extract all subtask issue IDs in an array:**

```bash
jq '[.fields.subtasks[].key]' issue-response.json
```

**Output**:
```json
[
  "SAMPLE-3894",
  "SAMPLE-3895", 
  "SAMPLE-3896",
  "SAMPLE-3897",
  "SAMPLE-3898",
  "SAMPLE-3899",
  "SAMPLE-3900",
  "SAMPLE-3901",
  "SAMPLE-3902",
  "SAMPLE-3903",
  "SAMPLE-3904",
  "SAMPLE-3905",
  "SAMPLE-3906"
]
```

![alt text](<Screenshot 2025-09-01 at 04.31.16.png>)

**Explanation**: This pattern uses the dot operator to traverse the JSON hierarchy: `.fields` accesses the `fields` object, `.fields.subtasks` accesses the `subtasks` array, and `.fields.subtasks[]` iterates over each subtask. `.fields.subtasks[].key` extracts the `key` property from each subtask. The outer brackets `[ ... ]` collect all keys into an array, handling any number of subtasks dynamically.

#### Alternative Approaches:

**Using map() function:**
```bash
jq '.fields.subtasks | map(.key)' issue-response.json
```
This uses the dot operator to access the array, then `map(.key)` to extract the `key` from each item.

**Raw output (without array brackets):**
```bash
jq -r '.fields.subtasks[].key' issue-response.json
```
This outputs each key on a separate line, using the dot operator for navigation and `-r` for raw output.

---





## Exercise #1 Verification Steps

1. Open your terminal in the project directory.
2. Run each JQ command above against `k8s-deploy.json` and `issue-response.json`.
3. Confirm the output matches the expected value and screenshot.
4. If the output differs, check the JSON structure and field names for typos.

---

## Exercise #2: Jira & GitHub Integration

### Integration Setup Framework

**Note**: This exercise requires actual Jira and GitHub App setup. The framework and configuration are documented below:

#### GitHub App Installation
- Install Port's GitHub App from the Port dashboard
- Grant necessary permissions (Actions: write, Contents: read, Metadata: read)
- Ensure app has access to target repositories

#### Jira Account Setup
- Create Jira account (free tier)
- Create new project: Software Development → Scrum → Company-managed
- Access Components feature from left sidebar

![alt text](<Screenshot 2025-09-01 at 04.59.21.png>)
![alt text](<Screenshot 2025-09-01 at 04.53.49.png>)



#### Port Ocean Integration for Jira
- Deploy using "Real Time & Always on" or "Scheduled" (not "Hosted by Port")
- Configure using the provided GitHub Actions workflow

![alt text](<Screenshot 2025-09-01 at 06.15.59.png>)

#### Data Model Configuration
```yaml
# Jira Issue → Repository relation
relations:
  repository:
    many: true  # Issue can relate to multiple repositories
```
- Map components to repositories in Port integration
- Support multiple component-to-repository relationships per issue

#### GitHub Actions Workflow
The provided `.github/workflows/deploy.yaml` implements the Jira integration:
on:
    push:
        branches:
            - feature/port-project2
    workflow_dispatch:
    schedule:
        - cron: '0 */1 * * *'

jobs:
    run-integration:
        runs-on: ubuntu-latest
        timeout-minutes: 30
        steps:
            - name: Run jira Integration
              uses: port-labs/ocean-sail@v1
                port_client_secret: ${{ secrets.PORT_CLIENT_SECRET }}
                port_base_url: "https://api.port.io"
                config: |
                    jira_host: https://sample.atlassian.net
                    atlassian_user_email: ${{ secrets.ATLASSIANUSEREMIL }}
                    atlassian_user_token: ${{ secrets.ATLASSIANUSERTOKEN }}
```
-
--


![alt text](<Screenshot 2025-09-01 at 04.42.56.png>)

![alt text](<Screenshot 2025-09-01 at 04.43.40.png>)

## Exercise #3: Repository Scorecard for Open Pull Requests

**Task**: Create a scorecard that tracks the number of open PRs per repository with Gold (<5 PRs), Silver (<10 PRs), and Bronze (<15 PRs) levels.

### Solution:

#### Step 1: Add Open PRs Property to Repository Blueprint

![alt text](<Screenshot 2025-09-01 at 04.59.21-1.png>)

First, we need to add a property to the repository blueprint to track the number of open pull requests:

```json
{
  "identifier": "repository",
  "title": "Repository",
  "schema": {
    "properties": {
      "name": {
        "type": "string",
        "title": "Repository Name"
      },
      "url": {
        "type": "string",
        "title": "Repository URL",
        "format": "url"
      },
      "language": {
        "type": "string",
        "title": "Primary Language"
      },
      "open_prs_count": {
        "type": "number",
        "title": "Open Pull Requests Count",
        "description": "Number of currently open pull requests"
      }
    },
    "required": ["name", "url"]
  }
}
```
**How PR Data is Sourced and Mapped:**
- Port’s GitHub integration fetches repository metadata and open PR counts using the GitHub API.
- The integration automatically updates the `open_prs_count` property on each repository entity in Port.
- You can verify this by checking the entity details in Port after a sync.

![Blueprint with open_prs_count](ADD_SCREENSHOT_BLUEPRINT_OPEN_PRS.png)

---

#### Step 1 Verification Steps
1. Ensure Port’s GitHub integration is enabled and configured for your organization.
2. Go to Port dashboard → Repositories.
3. Select a repository entity and check the value of `open_prs_count`.
    - _Add screenshot here of Port entity showing open PRs count._
    - ![Repository entity open PRs](ADD_SCREENSHOT_ENTITY_OPEN_PRS.png)
4. Confirm the value matches the number of open PRs in GitHub.
5. If the value is incorrect, check the integration logs or script output for errors.


#### Step 2: Create the Scorecard via API

Using Python to create the scorecard:

```python
import requests

# API configuration
API_URL = 'https://api.getport.io/v1'
access_token = 'your_port_api_token_here'
blueprint_name = 'repository'

# Scorecard configuration
scorecards = [
    {
        'identifier': 'pr_management',
        'title': 'Pull Request Management',
        'description': 'Tracks repository health based on open PR count',
        'rules': [
            {
                'identifier': 'gold_pr_count',
                'title': 'Excellent PR Management',
                'description': 'Less than 5 open PRs',
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
                'description': 'Less than 10 open PRs',
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
                'description': 'Less than 15 open PRs',
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
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Create the scorecard
response = requests.put(
    f'{API_URL}/blueprints/{blueprint_name}/scorecards',
    json=scorecards,
    headers=headers
)

if response.status_code == 200:
    print("Scorecard created successfully!")
    print(response.json())
else:
    print(f"Error creating scorecard: {response.status_code}")
    print(response.text)
```

---

#### Step 2 Verification Steps
1. Use the Port API or dashboard to create a scorecard that evaluates repositories based on the `open_prs_count` property. The scorecard logic should assign Gold, Silver, or Bronze status depending on the PR count.
2. The scorecard uses the `open_prs_count` property on each repository entity.
3. Gold: <5 PRs, Silver: <10 PRs, Bronze: <15 PRs.
4. The scorecard is automatically updated as PR counts change via integration.
5. Go to a repository entity in Port and click the "Scorecards" tab.
6. Verify the scorecard status (Gold, Silver, Bronze) matches the open PR count.
    - _Add screenshot here of scorecard results for a repository._
    - ![Scorecard results](ADD_SCREENSHOT_SCORECARD_RESULTS.png)
7. Test with repositories having different open PR counts to confirm the scorecard logic.
![alt text](<Screenshot 2025-09-01 at 06.28.34.png>)

![alt text](<Screenshot 2025-09-01 at 06.28.03.png>)
![alt text](<Screenshot 2025-09-01 at 06.27.40.png>)



# Exercise #4: Troubleshooting Self-Service Actions with GitHub Workflows


![alt text](<Screenshot 2025-09-01 at 06.40.45.png>)

![alt text](<Screenshot 2025-09-01 at 06.41.06.png>)

![alt text](<Screenshot 2025-09-01 at 06.41.22.png>)

**Problem**: Self-service action triggers a GitHub workflow but stays in "IN PROGRESS" status indefinitely, and the workflow is not being triggered.





**Problem Recap:**
Customer’s self-service action in Port stays “IN PROGRESS” and does not trigger the GitHub workflow.

## Step-by-Step Debugging & Evidence

### 1. Check Port Action Logs
- Go to the entity in Port, open “Action Runs” or “Audit Log.”
![alt text](<Screenshot 2025-09-01 at 12.51.05.png>)
  

### 2. Verify GitHub Workflow Run
- Go to GitHub → Actions tab. Confirm if a workflow run was triggered.
![alt text](<Screenshot 2025-09-01 at 04.42.56-1.png>)
  

### 3. Review Workflow File
- Ensure `workflow_dispatch` is present in the workflow file.
- Reference: [Port Docs - GitHub Integration](https://docs.getport.io/docs/integrations/github-actions)

### 4. Check Secrets
- Confirm `PORT_CLIENT_ID` and `PORT_CLIENT_SECRET` are set in GitHub repository secrets.
![alt text](<Screenshot 2025-09-01 at 12.54.15.png>)
  

### 5. Attempt to Recreate the Issue
- Intentionally misconfigure (e.g., remove `workflow_dispatch` or a secret) and trigger the action.
- Observe Port stays “IN PROGRESS” and no workflow run appears in GitHub.


### 6. Resolution
- Add or fix `workflow_dispatch` in the workflow file.
- Retry the self-service action; workflow triggers and Port updates status.

  
 

### References
- [Port Docs: Self-Service Actions](https://docs.port.io/)


