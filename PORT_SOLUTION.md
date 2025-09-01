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

**Explanation**: This pattern navigates to the `spec` object and extracts the `replicas` field, which contains the desired number of pod replicas for the deployment.

#### b. Deployment Strategy
```bash
jq '.spec.strategy.type' k8s-deploy.json
```
**Output**: `"RollingUpdate"`

![alt text](<Screenshot 2025-09-01 at 04.29.03.png>)

**Explanation**: This pattern accesses the deployment strategy configuration within the spec, specifically the `type` field that indicates whether the deployment uses RollingUpdate or Recreate strategy.

#### c. Service-Environment Label Concatenation
```bash
jq -r '(.metadata.labels.service + "-" + .metadata.labels.environment)' k8s-deploy.json
```
**Output**: `authorization-production-gcp-1`

![alt text](<Screenshot 2025-09-01 at 04.29.55.png>)

**Explanation**: This pattern extracts two labels from the metadata section and concatenates them with a hyphen. The `-r` flag provides raw output without quotes. The parentheses ensure proper string concatenation order.




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

**Explanation**: 
- `.fields.subtasks[]` iterates through each subtask object in the subtasks array
- `.key` extracts the issue identifier from each subtask
- The outer `[]` brackets collect all the keys into a single array
- This pattern handles any number of subtasks dynamically

#### Alternative Approaches:

**Using map() function:**
```bash
jq '.fields.subtasks | map(.key)' issue-response.json
```

**Raw output (without array brackets):**
```bash
jq -r '.fields.subtasks[].key' issue-response.json
```

---


## Understanding the JQ Dot (.) Operator

The dot (`.`) operator in JQ is fundamental for navigating and extracting data from JSON objects:

- `.` by itself refers to the entire input JSON object.
- `.fieldname` accesses a field within the object (e.g., `.fields` gets the `fields` object).
- Chaining fields (e.g., `.fields.subtasks`) traverses deeper into the hierarchy.
- For arrays, `.fields.subtasks[]` iterates over each item in the array.
- To extract a property from each item, use `.fields.subtasks[].key` (gets the `key` from every subtask).
- Parentheses can be used for grouping and operations, such as concatenation: `(.metadata.labels.service + "-" + .metadata.labels.environment)`.

This navigation allows you to flexibly extract, transform, and combine data from complex JSON structures.

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
    title: Repository
    target: repository
    required: false
    many: true  # Issue can relate to multiple repositories
```

#### Component Mapping Strategy
- Create Jira components matching GitHub repository names
- Map components to repositories in Port integration
- Support multiple component-to-repository relationships per issue

#### GitHub Actions Workflow
The provided `.github/workflows/deploy.yaml` implements the Jira integration:

```yaml
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
              with:
                type: jira
                port_client_id: ${{ secrets.PORT_CLIENT_ID }}
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
  "icon": "Github",
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


