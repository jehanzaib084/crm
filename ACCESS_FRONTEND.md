# Access Your Frontend Application

## ✅ Your Frontend is Live!

**External IP:** `20.239.224.248`  
**Access URL:** `http://20.239.224.248`

## Current Status

Your LoadBalancer is working and has an external IP assigned. You can access your application right now at:

```
http://20.239.224.248
```

## Why DNS Label Might Not Work

The Azure DNS label (`idurar-crm`) might not show a hostname because:

1. **Region Support**: Not all Azure regions support DNS labels
2. **AKS Configuration**: DNS labels need to be enabled in AKS
3. **Naming Restrictions**: DNS labels must be unique across Azure

## Solutions

### Option 1: Use the IP Address (Current - Works Now!)

Simply access:
```
http://20.239.224.248
```

### Option 2: Create Azure Public IP with DNS Name

If you want a proper domain name, you can:

1. **Create a Static Public IP with DNS name:**
   ```bash
   az network public-ip create \
     --resource-group <your-resource-group> \
     --name idurar-crm-ip \
     --dns-name idurar-crm \
     --allocation-method Static
   ```

2. **Update the service to use it:**
   ```yaml
   spec:
     loadBalancerIP: <static-ip-address>
   ```

### Option 3: Use Azure Application Gateway or Ingress

For a proper domain with SSL, consider:
- Azure Application Gateway
- NGINX Ingress Controller
- Azure Front Door

## Verify Access

Test if your frontend is accessible:

```bash
curl http://20.239.224.248
```

Or open in browser:
```
http://20.239.224.248
```

## Check Service Status

```bash
kubectl get svc frontend -n idurar-crm
```

You should see:
```
NAME       TYPE           EXTERNAL-IP      PORT(S)
frontend   LoadBalancer   20.239.224.248  80:32432/TCP
```

## Troubleshooting

**If you can't access the IP:**

1. **Check if pods are running:**
   ```bash
   kubectl get pods -n idurar-crm
   ```

2. **Check pod logs:**
   ```bash
   kubectl logs -n idurar-crm <frontend-pod-name>
   ```

3. **Check service endpoints:**
   ```bash
   kubectl get endpoints frontend -n idurar-crm
   ```

4. **Test from inside cluster:**
   ```bash
   kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://frontend.idurar-crm.svc.cluster.local
   ```

## Next Steps

Your application is deployed and accessible at:
- **Frontend:** http://20.239.224.248
- **Backend API:** Internal only (ClusterIP)
- **MongoDB:** Internal only (ClusterIP)

The IP address is stable and will remain the same unless you delete the service.
