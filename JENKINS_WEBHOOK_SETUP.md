# Jenkins Webhook Setup for Instant Builds

## Problem
Jenkins is using `pollSCM` which checks for changes every 5 minutes, causing delays.

## Solution: GitHub Webhook (Instant Triggers)

### Step 1: Configure GitHub Plugin in Jenkins

1. Go to **Jenkins Dashboard** → **Manage Jenkins** → **Manage Plugins**
2. Install **GitHub plugin** (if not already installed)
3. Go to **Manage Jenkins** → **Configure System**
4. Scroll to **GitHub** section
5. Click **Add GitHub Server**
6. Name: `GitHub`
7. API URL: `https://api.github.com`
8. Click **Save**

### Step 2: Add GitHub Webhook in Your Repository

1. Go to your GitHub repository
2. Click **Settings** → **Webhooks** → **Add webhook**
3. **Payload URL**: `http://YOUR_JENKINS_URL/github-webhook/`
   - Example: `http://jenkins.example.com:8080/github-webhook/`
   - Or: `http://your-ip:8080/github-webhook/`
4. **Content type**: `application/json`
5. **Secret**: (optional, leave empty for now)
6. **Which events**: Select **Just the push event**
7. **Active**: ✅ Checked
8. Click **Add webhook**

### Step 3: Update Jenkinsfile

The Jenkinsfile already has webhook support. After setting up the webhook:

1. Remove the `pollSCM` line from Jenkinsfile (line 18)
2. Or keep it as a fallback (it will poll every 1 minute now)

### Step 4: Test

1. Make a small change to your repository
2. Push to GitHub
3. Check Jenkins - it should trigger **immediately** (within seconds)

## Alternative: More Frequent Polling

If you can't set up webhooks, the Jenkinsfile now polls every **1 minute** instead of 5 minutes.

To change polling frequency, edit line 18 in Jenkinsfile:
- Every 1 minute: `pollSCM('H/1 * * * *')`
- Every 2 minutes: `pollSCM('H/2 * * * *')`
- Every 5 minutes: `pollSCM('H/5 * * * *')`

## Troubleshooting

**Webhook not triggering?**
1. Check Jenkins logs: **Manage Jenkins** → **System Log**
2. Verify webhook URL is accessible from GitHub
3. Check if Jenkins is behind a firewall (may need to expose port)
4. Verify GitHub webhook shows "Recent Deliveries" with 200 status

**Still using polling?**
- Make sure you've pushed the updated Jenkinsfile
- The webhook setup is optional - polling every 1 minute is still faster than 5 minutes

## Current Configuration

- **Polling**: Every 1 minute (fallback)
- **Webhook**: Configure manually for instant triggers
