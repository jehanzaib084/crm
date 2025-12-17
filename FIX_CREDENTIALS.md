# Fix Jenkins Credentials ID

## Current Issue

Your Jenkins credential has a UUID ID, but the Jenkinsfile expects: `dockerhub-credentials`

## Solution: Update Credential ID

### Option 1: Update Existing Credential (Recommended)

1. Go to **Jenkins** → **Manage Jenkins** → **Credentials**
2. Find your credential: `Jehanzaib08/******`
3. Click on it, then click **Update**
4. In the **ID** field, change it to: `dockerhub-credentials`
5. Click **Save**

### Option 2: Create New Credential with Correct ID

1. Go to **Jenkins** → **Manage Jenkins** → **Credentials**
2. Click **Add Credentials**
3. Fill in:
   - **Kind**: Username with password
   - **Scope**: Global
   - **Username**: `jehanzaib08` (lowercase)
   - **Password**: Your Docker Hub password
   - **ID**: `dockerhub-credentials` ⚠️ **MUST BE EXACTLY THIS**
   - **Description**: Docker Hub credentials for CI/CD
4. Click **OK**

### Option 3: Use Your Existing Credential ID

If you want to keep your UUID, I can update the Jenkinsfile to use it. Just let me know the full UUID.

## Verify

After updating, the pipeline should:
- ✅ Successfully login to Docker Hub
- ✅ Push images without errors

## Note

The username in your credential shows `Jehanzaib08` (capital J), but Docker Hub usernames are case-sensitive. Make sure it matches your actual Docker Hub username exactly.
