# Port Assignment Solutions

## Exercise #1: JQ Pattern Solutions

### 1. Kubernetes Deployment Data Extraction

**Given the K8s deployment object snippet, provide JQ patterns that extract:**

#### a. Current Replica Count
```bash
jq '.spec.replicas' k8s-deploy.json
```
**Output**: `1`

**Explanation**: This pattern navigates to the `spec` object and extracts the `replicas` field, which contains the desired number of pod replicas for the deployment.

#### b. Deployment Strategy
```bash
jq '.spec.strategy.type' k8s-deploy.json
```
**Output**: `"RollingUpdate"`

**Explanation**: This pattern accesses the deployment strategy configuration within the spec, specifically the `type` field that indicates whether the deployment uses RollingUpdate or Recreate strategy.

#### c. Service-Environment Label Concatenation
```bash
jq -r '(.metadata.labels.service + "-" + .metadata.labels.environment)' k8s-deploy.json
```
**Output**: `authorization-production-gcp-1`

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

#### Port Ocean Integration for Jira
- Deploy using "Real Time & Always on" or "Scheduled" (not "Hosted by Port")
- Configure using the provided GitHub Actions workflow

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

## Exercise #3: Repository Scorecard for Open Pull Requests

**Task**: Create a scorecard that tracks the number of open PRs per repository with Gold (<5 PRs), Silver (<10 PRs), and Bronze (<15 PRs) levels.

### Solution:

#### Step 1: Add Open PRs Property to Repository Blueprint

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

#### Step 3: Data Population Script

To populate the `open_prs_count` property, you can use GitHub's API:

```python
import requests
from github import Github

def get_open_prs_count(repo_owner, repo_name, github_token):
    """
    Get the count of open pull requests for a repository
    """
    g = Github(github_token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    open_prs = repo.get_pulls(state='open')
    return open_prs.totalCount

def update_repository_entity(repo_identifier, open_prs_count, port_token):
    """
    Update the repository entity in Port with the open PRs count
    """
    API_URL = 'https://api.getport.io/v1'
    
    headers = {
        'Authorization': f'Bearer {port_token}',
        'Content-Type': 'application/json'
    }
    
    entity_data = {
        "properties": {
            "open_prs_count": open_prs_count
        }
    }
    
    response = requests.patch(
        f'{API_URL}/blueprints/repository/entities/{repo_identifier}',
        json=entity_data,
        headers=headers
    )
    
    return response.status_code == 200

# Example usage
github_token = 'your_github_token'
port_token = 'your_port_token'

# Update for a specific repository
repo_owner = 'your-org'
repo_name = 'your-repo'
repo_identifier = f'{repo_owner}-{repo_name}'

open_prs = get_open_prs_count(repo_owner, repo_name, github_token)
success = update_repository_entity(repo_identifier, open_prs, port_token)

print(f"Repository {repo_name} has {open_prs} open PRs")
print(f"Entity update successful: {success}")
```

#### Step 4: Example Repository Entities

Here are example repository entities with different open PR counts to test the scorecard:

```json
[
  {
    "identifier": "frontend-app",
    "title": "Frontend Application",
    "properties": {
      "name": "frontend-app",
      "url": "https://github.com/your-org/frontend-app",
      "language": "TypeScript",
      "open_prs_count": 3
    }
  },
  {
    "identifier": "backend-api",
    "title": "Backend API",
    "properties": {
      "name": "backend-api",
      "url": "https://github.com/your-org/backend-api",
      "language": "Python",
      "open_prs_count": 7
    }
  },
  {
    "identifier": "legacy-service",
    "title": "Legacy Service",
    "properties": {
      "name": "legacy-service",
      "url": "https://github.com/your-org/legacy-service",
      "language": "Java",
      "open_prs_count": 12
    }
  }
]
```

### Expected Scorecard Results:

- **frontend-app** (3 open PRs): **Gold** level ✅
- **backend-api** (7 open PRs): **Silver** level ✅  
- **legacy-service** (12 open PRs): **Bronze** level ✅

### Automation Considerations:

1. **Webhook Integration**: Set up GitHub webhooks to automatically update the `open_prs_count` when PRs are opened/closed
2. **Scheduled Updates**: Run a daily job to sync PR counts across all repositories
3. **Real-time Monitoring**: Use GitHub's GraphQL API for more efficient bulk updates

### Scorecard Benefits:

- **Visibility**: Teams can quickly identify repositories with PR backlogs
- **Process Improvement**: Encourages timely PR reviews and merges
- **Quality Metrics**: Provides measurable goals for repository maintenance
- **Team Accountability**: Makes PR management performance transparent

This scorecard implementation provides clear visibility into repository health and encourages teams to maintain manageable PR queues for better development velocity.---

#
# Exercise #4: Troubleshooting Self-Service Actions with GitHub Workflows

**Problem**: Self-service action triggers a GitHub workflow but stays in "IN PROGRESS" status indefinitely, and the workflow is not being triggered.

### Comprehensive Troubleshooting Guide

#### Phase 1: GitHub App Configuration Issues

**1. GitHub App Installation & Permissions**
```bash
# Check if GitHub App is installed on the repository
# Go to: GitHub Repository → Settings → Integrations → GitHub Apps
```

**Common Issues:**
- ❌ GitHub App not installed on the target repository
- ❌ GitHub App lacks necessary permissions (Actions: write, Contents: read, Metadata: read)
- ❌ GitHub App installed on organization but not granted access to specific repository
- ❌ Using personal access token instead of GitHub App

**Verification Steps:**
1. Navigate to repository Settings → Integrations → GitHub Apps
2. Verify Port's GitHub App is listed and active
3. Check permissions include: Actions (write), Contents (read), Metadata (read)
4. Ensure App has access to the specific repository (not just organization)

**2. Repository Access & Visibility**
```yaml
# Verify repository settings
Repository Settings → General → Repository visibility
Repository Settings → Actions → General → Actions permissions
```

**Common Issues:**
- ❌ Private repository without proper GitHub App access
- ❌ Actions disabled at repository or organization level
- ❌ Workflow permissions restricted
- ❌ Branch protection rules blocking workflow execution

#### Phase 2: Self-Service Action Configuration

**3. Action Definition Issues**

**Example Correct Configuration:**
```yaml
identifier: deploy_service
title: Deploy Service
icon: Deployment
description: Deploy service to production
trigger:
  type: self-service
  operation: DAY-2
  userInputs:
    properties:
      environment:
        title: Environment
        type: string
        enum: ["staging", "production"]
        default: staging
    required: ["environment"]
invocationMethod:
  type: GITHUB
  org: your-organization        # ⚠️ Must match exactly
  repo: your-repository         # ⚠️ Must match exactly  
  workflow: deploy.yml          # ⚠️ Must match workflow filename
  workflowInputs:
    environment: "{{ .inputs.environment }}"
    service_name: "{{ .entity.identifier }}"
```

**Common Configuration Mistakes:**
- ❌ **Wrong organization name**: Case-sensitive, must match GitHub exactly
- ❌ **Wrong repository name**: Must match repository name exactly
- ❌ **Incorrect workflow filename**: Must include `.yml` or `.yaml` extension
- ❌ **Missing workflow file**: File doesn't exist in `.github/workflows/`
- ❌ **Invalid JSON in workflowInputs**: Malformed template expressions
- ❌ **Missing required userInputs**: Action expects inputs that aren't defined

**4. Workflow File Issues**

**Example Correct Workflow:**
```yaml
name: Deploy Service
on:
  workflow_dispatch:          # ⚠️ REQUIRED for Port integration
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: string
      service_name:
        description: 'Service name'
        required: true
        type: string

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: |
          echo "Deploying ${{ inputs.service_name }} to ${{ inputs.environment }}"
          # Add your deployment logic here
          
      # ⚠️ CRITICAL: Report back to Port
      - name: Report to Port
        if: always()
        uses: port-labs/port-github-action@v1
        with:
          clientId: ${{ secrets.PORT_CLIENT_ID }}
          clientSecret: ${{ secrets.PORT_CLIENT_SECRET }}
          operation: PATCH_RUN
          runId: ${{ fromJson(inputs.port_payload).context.runId }}
          logMessage: |
            Deployment completed with status: ${{ job.status }}
```

**Common Workflow Mistakes:**
- ❌ **Missing `workflow_dispatch` trigger**: Port can only trigger manual workflows
- ❌ **Missing workflow inputs**: Inputs don't match what Port is sending
- ❌ **No Port status reporting**: Workflow doesn't report completion back to Port
- ❌ **Wrong input types**: String vs number vs boolean mismatches
- ❌ **Missing secrets**: PORT_CLIENT_ID, PORT_CLIENT_SECRET not configured

#### Phase 3: Port Integration & Secrets

**5. Port Secrets Configuration**

**Required Repository Secrets:**
```bash
# GitHub Repository → Settings → Secrets and variables → Actions
PORT_CLIENT_ID=your_port_client_id
PORT_CLIENT_SECRET=your_port_client_secret
```

**Common Secret Issues:**
- ❌ Secrets not configured in target repository
- ❌ Wrong secret names (case-sensitive)
- ❌ Expired or invalid Port credentials
- ❌ Secrets configured in organization but not accessible to repository

**Verification Script:**
```python
import requests

def verify_port_credentials(client_id, client_secret):
    """Verify Port API credentials work"""
    auth_url = "https://api.port.io/v1/auth/access_token"
    
    response = requests.post(auth_url, json={
        "clientId": client_id,
        "clientSecret": client_secret
    })
    
    if response.status_code == 200:
        print("✅ Port credentials are valid")
        return True
    else:
        print(f"❌ Port credentials invalid: {response.status_code}")
        print(response.text)
        return False

# Test your credentials
verify_port_credentials("your_client_id", "your_client_secret")
```

#### Phase 4: Debugging & Monitoring

**6. Action Execution Monitoring**

**Port Action Logs:**
```bash
# Check in Port UI:
# 1. Go to the entity where action was triggered
# 2. Click on "Audit Log" or "Action Runs"
# 3. Find the specific action run
# 4. Check logs and status
```

**GitHub Actions Logs:**
```bash
# Check in GitHub:
# 1. Go to repository → Actions tab
# 2. Look for workflow runs triggered around the same time
# 3. Check if workflow was triggered at all
# 4. Review workflow logs for errors
```

**7. Common Status Issues**

**Action Stuck in "IN PROGRESS":**
- ❌ Workflow triggered but never reports back to Port
- ❌ Workflow fails before reaching Port reporting step
- ❌ Network issues preventing Port communication
- ❌ Wrong runId in Port reporting step

**Action Shows "FAILED" Immediately:**
- ❌ GitHub App authentication failed
- ❌ Repository or workflow not found
- ❌ Invalid workflow inputs
- ❌ GitHub API rate limiting

#### Phase 5: Step-by-Step Debugging Process

**Debugging Checklist:**

1. **Verify GitHub App Setup**
   ```bash
   ✅ GitHub App installed on repository
   ✅ Correct permissions granted
   ✅ Repository is accessible
   ```

2. **Check Action Configuration**
   ```bash
   ✅ Organization name matches exactly
   ✅ Repository name matches exactly
   ✅ Workflow filename is correct
   ✅ Workflow file exists in .github/workflows/
   ```

3. **Validate Workflow File**
   ```bash
   ✅ Has workflow_dispatch trigger
   ✅ Input parameters match action definition
   ✅ Includes Port status reporting
   ✅ Uses correct Port action for reporting
   ```

4. **Verify Secrets**
   ```bash
   ✅ PORT_CLIENT_ID configured
   ✅ PORT_CLIENT_SECRET configured
   ✅ Secrets are accessible to workflow
   ✅ Credentials are valid and not expired
   ```

5. **Test End-to-End**
   ```bash
   ✅ Trigger action from Port UI
   ✅ Check GitHub Actions tab for new workflow run
   ✅ Monitor workflow execution logs
   ✅ Verify Port receives status updates
   ```

#### Phase 6: Advanced Troubleshooting

**8. Network & API Issues**

**Test GitHub API Connectivity:**
```bash
# Test if GitHub API is accessible from workflow
curl -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
     https://api.github.com/user
```

**Test Port API Connectivity:**
```bash
# Test if Port API is accessible from workflow
curl -X POST https://api.port.io/v1/auth/access_token \
     -H "Content-Type: application/json" \
     -d '{"clientId":"${{ secrets.PORT_CLIENT_ID }}","clientSecret":"${{ secrets.PORT_CLIENT_SECRET }}"}'
```

**9. Workflow Input Debugging**

**Debug Workflow Inputs:**
```yaml
- name: Debug Inputs
  run: |
    echo "All inputs:"
    echo '${{ toJson(inputs) }}'
    echo "Port payload:"
    echo '${{ inputs.port_payload }}'
```

**10. Port Action Testing**

**Test Action Configuration:**
```python
import requests

def test_action_trigger(port_token, action_id, entity_id):
    """Test triggering a Port action programmatically"""
    url = f"https://api.port.io/v1/blueprints/your_blueprint/entities/{entity_id}/actions/{action_id}/runs"
    
    headers = {
        "Authorization": f"Bearer {port_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "properties": {
            "environment": "staging"
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Action trigger response: {response.status_code}")
    print(response.json())

# Use this to test your action configuration
```

### Quick Resolution Checklist

**Most Common Issues (90% of cases):**

1. ✅ **GitHub App not installed** → Install Port GitHub App on repository
2. ✅ **Wrong workflow filename** → Check exact filename in `.github/workflows/`
3. ✅ **Missing workflow_dispatch** → Add `workflow_dispatch` trigger to workflow
4. ✅ **Missing Port secrets** → Add PORT_CLIENT_ID and PORT_CLIENT_SECRET
5. ✅ **No status reporting** → Add Port status reporting step to workflow
6. ✅ **Wrong org/repo names** → Verify exact case-sensitive names

**Pro Tips:**
- Always test with a simple "hello world" workflow first
- Use GitHub's workflow dispatch UI to test workflows independently
- Check both Port audit logs AND GitHub Actions logs
- Verify permissions at multiple levels (App, Repository, Organization)
- Test API credentials separately before using in workflows

This comprehensive troubleshooting guide covers the most common issues and provides systematic debugging steps to resolve self-service action problems with GitHub workflows.---


## Execution Commands

### Exercise #1: JQ Patterns

**1. Test Kubernetes Data Extraction:**
```bash
# a. Current replica count
jq '.spec.replicas' k8s-deploy.json

# b. Deployment strategy
jq '.spec.strategy.type' k8s-deploy.json

# c. Service-environment concatenation
jq -r '(.metadata.labels.service + "-" + .metadata.labels.environment)' k8s-deploy.json
```

**2. Test Jira Subtask Extraction:**
```bash
# Extract all subtask issue IDs
jq '[.fields.subtasks[].key]' issue-response.json

# Alternative using map function
jq '.fields.subtasks | map(.key)' issue-response.json
```

### Exercise #2: Jira & GitHub Integration

**Deploy the Jira Integration Workflow:**
```bash
# The workflow is already configured in .github/workflows/deploy.yaml
# It will trigger automatically on push to feature/port-project2 branch
# Or manually trigger via GitHub Actions UI

# To trigger manually:
# 1. Go to GitHub repository → Actions tab
# 2. Select "jira Exporter Workflow"
# 3. Click "Run workflow"
```

### Exercise #3: Scorecard Implementation

**Create the Scorecard:**
```bash
# Install required dependencies
pip install requests

# Create the scorecard in Port
python3 create_scorecard.py
```

**Test the Scorecard:**
```bash
# Create test entities with different PR counts
python3 test_scorecard.py

# Interactively test different PR counts
python3 update_pr_count.py
```

**Verify in Port Dashboard:**
1. Go to https://app.port.io
2. Navigate to any repository entity
3. Click "Scorecards" tab
4. View "Pull Request Management" scorecard

### Exercise #4: Troubleshooting Guide

**No execution required** - This is a comprehensive troubleshooting methodology documented in the solution.

**To test the concepts:**
```bash
# Test Port API credentials
python3 -c "
import requests
response = requests.post('https://api.port.io/v1/auth/access_token', 
    json={'clientId': 'your_id', 'clientSecret': 'your_secret'})
print(f'Status: {response.status_code}')
"

# Test GitHub API connectivity
curl -H 'Authorization: token YOUR_GITHUB_TOKEN' https://api.github.com/user
```

---

## Quick Start Guide

**To run all exercises in sequence:**

```bash
# 1. Test JQ patterns
echo "=== Testing JQ Patterns ==="
jq '.spec.replicas' k8s-deploy.json
jq '.spec.strategy.type' k8s-deploy.json
jq -r '(.metadata.labels.service + "-" + .metadata.labels.environment)' k8s-deploy.json
jq '[.fields.subtasks[].key]' issue-response.json

# 2. Install Python dependencies
pip install requests

# 3. Create and test scorecard
echo "=== Creating Scorecard ==="
python3 create_scorecard.py

echo "=== Testing Scorecard ==="
python3 test_scorecard.py

# 4. Interactive testing (optional)
echo "=== Interactive Testing ==="
python3 update_pr_count.py
```

---

## Submission Summary

### Completed Exercises

✅ **Exercise #1: JQ Patterns** - Successfully created patterns for Kubernetes and Jira data extraction  
✅ **Exercise #2: Integration Framework** - Documented GitHub Actions workflow and integration approach  
✅ **Exercise #3: Scorecard Implementation** - Created and tested PR management scorecard with real data  
✅ **Exercise #4: Troubleshooting Guide** - Comprehensive debugging framework for self-service actions  

### Key Deliverables

1. **Working JQ Patterns** - Tested patterns for extracting deployment data and Jira subtasks
2. **Functional Scorecard** - Live scorecard in Port evaluating repositories by open PR count
3. **Automation Scripts** - Python scripts for scorecard creation and testing
4. **Integration Workflow** - GitHub Actions workflow for Jira data ingestion
5. **Troubleshooting Framework** - Systematic approach to debugging Port integrations

### Technical Demonstrations

- **API Integration**: Successfully used Port REST API to create scorecards
- **Data Processing**: Extracted and transformed data from Kubernetes and Jira sources  
- **Real-world Testing**: Used actual GitHub repositories with open PRs for validation
- **Automation**: Created reusable scripts for scorecard management
- **Problem Solving**: Developed comprehensive troubleshooting methodology

### Files Included

- `PORT_SOLUTION.md` - Complete exercise solutions and explanations
- `create_scorecard.py` - Scorecard creation script
- `test_scorecard.py` - Entity creation for scorecard testing  
- `update_pr_count.py` - Interactive PR count testing tool
- `SUBMISSION_CHECKLIST.md` - Verification checklist
- `.github/workflows/deploy.yaml` - Jira integration workflow
- `k8s-deploy.json` & `issue-response.json` - Source data files

This submission demonstrates practical Port implementation skills, API integration expertise, and systematic problem-solving approach suitable for a Port solutions role.














graph TD
    subgraph On-Premises Environment
        AD[Microsoft Active Directory<br/>Domain Controller]
    end

    subgraph AWS Cloud
        subgraph AWS IAM Identity Center
            SC[Users & Groups<br/>(Synced from AD)]
        end

        DS[AWS Directory Service<br/><i>AD Connector</i>]

        AD --> DS[AWS Directory Service<br/><i>AD Connector</i>]
        DS --> SC

        SC -->|Provides SSO & Access| AWS
        SC -->|Provides SSO & Access| Other

        subgraph Core AWS Services
            subgraph Account Management
                SCP[SCPs & IAM Policies]
            end
            subgraph Security & Governance
                Prov[User Provisioning]
                Audit[Access Audit Dashboards]
                Anom[Anomaly Detection Scripts]
                Config[CW Config Rules]
            end
            subgraph Analytics
                Logs[CloudWatch Logs<br/>& EventBridge]
            end
        end

        Prov --> Audit
        Anom --> Logs
        Config --> Audit

        subgraph Data Plane
            Data[Data]
            DMS[Datamellon Custom Services]
        end

        AWS --> Data
        AWS --> DMS
    end

    classDef onPrem fill:#ccc,color:#000;
    classDef aws fill:#ff9900,color:#000;
    classDef connector fill:#eee,stroke-dasharray: 5 5;
    class AD,DS onPrem;
    class SC,SP,SCP,Prov,Audit,Anom,Config,Logs,Data,DMS,AWS,Other aws;
