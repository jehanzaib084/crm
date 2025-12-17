# Docker Hub Login Fix

## Issue
```
Error response from daemon: Get "https://registry-1.docker.io/v2/": unauthorized: incorrect username or password
```

## Root Cause
Your Jenkins credential has username `Jehanzaib08` (capital J), but Docker Hub usernames are **case-sensitive** and typically lowercase.

## Solutions

### Option 1: Update Credential Username (Recommended)

1. Go to **Jenkins** → **Manage Jenkins** → **Credentials**
2. Find credential: `fd9b973e-1c72-4698-b6dd-5030492cbfa4`
3. Click **Update**
4. Change **Username** from `Jehanzaib08` to `jehanzaib08` (lowercase)
5. Click **Save**

### Option 2: Use Docker Hub Access Token

Instead of password, use an access token:

1. Go to **Docker Hub** → **Account Settings** → **Security**
2. Click **New Access Token**
3. Name it: "Jenkins CI/CD"
4. Copy the token
5. In Jenkins credential, use:
   - **Username**: `jehanzaib08` (lowercase)
   - **Password**: The access token (not your account password)

### Option 3: Verify Your Actual Docker Hub Username

1. Login to Docker Hub website
2. Check your profile URL: `https://hub.docker.com/u/YOUR_USERNAME`
3. The username in the URL is your actual username (usually lowercase)
4. Update Jenkins credential to match exactly

## Why This Happens

Docker Hub authentication is case-sensitive:
- ✅ `jehanzaib08` (lowercase) - correct
- ❌ `Jehanzaib08` (capital J) - will fail
- ❌ `JEHANZAIB08` (all caps) - will fail

## After Fixing

1. Re-run the Jenkins pipeline
2. The Docker login should succeed
3. Images will be pushed to: `jehanzaib08/crm-*`
