# Getting Frontend Access URL

## Azure LoadBalancer External IP

After the pipeline completes, the frontend service will get an external IP from Azure LoadBalancer.

### Method 1: From Jenkins Pipeline Output

The pipeline will automatically show the external IP/hostname in the logs. Look for:
```
🌐 Frontend Access URL:
   ✅ http://<IP_OR_HOSTNAME>
```

### Method 2: Using kubectl Command

Run this command to get the external IP:

```bash
kubectl get svc frontend -n idurar-crm
```

Look for the `EXTERNAL-IP` column. It may show:
- An IP address (e.g., `20.123.45.67`)
- `<pending>` (still provisioning - wait a few minutes)
- A hostname (e.g., `idurar-crm.eastus.cloudapp.azure.com`)

### Method 3: Get Detailed Info

```bash
kubectl get svc frontend -n idurar-crm -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
kubectl get svc frontend -n idurar-crm -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

### Method 4: Azure DNS Label

The service is configured with Azure DNS label: `idurar-crm`

If your Azure region supports it, you can access via:
```
http://idurar-crm.<region>.cloudapp.azure.com
```

For example:
- East US: `http://idurar-crm.eastus.cloudapp.azure.com`
- West Europe: `http://idurar-crm.westeurope.cloudapp.azure.com`

### Wait Time

Azure LoadBalancer provisioning typically takes:
- **1-3 minutes** for IP allocation
- **3-5 minutes** for DNS propagation (if using DNS label)

### Troubleshooting

**If EXTERNAL-IP shows `<pending>`:**
1. Wait 2-3 minutes
2. Check again: `kubectl get svc frontend -n idurar-crm`
3. Check events: `kubectl describe svc frontend -n idurar-crm`

**If you get timeout/connection refused:**
1. Verify pods are running: `kubectl get pods -n idurar-crm`
2. Check pod logs: `kubectl logs -n idurar-crm <pod-name>`
3. Verify service selector matches pod labels

### Quick Check Script

```bash
# Get frontend URL
kubectl get svc frontend -n idurar-crm -o jsonpath='http://{.status.loadBalancer.ingress[0].ip}{"\n"}'
```
