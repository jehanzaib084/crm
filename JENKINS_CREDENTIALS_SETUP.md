# Jenkins Credentials Setup - REQUIRED

## ⚠️ Error: dockerhub-credentials not found

If you see this error:
```
ERROR: dockerhub-credentials
```

You need to add Docker Hub credentials to Jenkins.

## Step-by-Step Setup

### 1. Go to Jenkins Credentials

1. Open Jenkins
2. Click **Manage Jenkins** (left sidebar)
3. Click **Credentials**
4. Click **System** → **Global credentials (unrestricted)**
5. Click **Add Credentials** (left sidebar)

### 2. Add Docker Hub Credentials

Fill in the form:

- **Kind**: `Username with password`
- **Scope**: `Global (Jenkins, nodes, items, all child items, etc)`
- **Username**: `jehanzaib08`
- **Password**: Your Docker Hub password/token
- **ID**: `dockerhub-credentials` ⚠️ **MUST BE EXACTLY THIS**
- **Description**: `Docker Hub credentials for pushing images`

### 3. Click OK

### 4. Re-run Pipeline

Go back to your pipeline job and click **Build Now**

## Alternative: Using Docker Hub Access Token

Instead of password, you can use an access token:

1. Go to Docker Hub → Account Settings → Security
2. Click **New Access Token**
3. Name it (e.g., "Jenkins CI/CD")
4. Copy the token
5. Use the token as the password in Jenkins credentials

## Verification

After adding credentials, the pipeline should:
- ✅ Successfully login to Docker Hub
- ✅ Push images to `jehanzaib08/crm-frontend`, `jehanzaib08/crm-backend`, `jehanzaib08/crm-db`

## Troubleshooting

**Still getting error?**
- Verify the ID is exactly: `dockerhub-credentials` (case-sensitive)
- Check that credentials are in **Global** scope
- Verify Docker Hub username and password are correct
- Try creating a new access token if password doesn't work
