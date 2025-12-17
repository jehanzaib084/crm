# Ansible Configuration for IDURAR ERP CRM

Simple Ansible setup for configuring servers for the IDURAR ERP CRM project.

## 📋 Files

- `hosts.ini` - Inventory with 4 servers (2 web servers, 2 app servers)
- `playbook.yml` - Main playbook
- `ansible.cfg` - Ansible configuration

## 🎯 Server Configuration

### Web Servers (2 servers)
- **web-01, web-02**
- Installs: Nginx, Docker, Python3
- Purpose: Frontend hosting and reverse proxy

### Application Servers (2 servers)
- **app-01, app-02**
- Installs: Node.js, npm, PM2, Docker, Python3
- Purpose: Backend API hosting

## 🚀 Quick Start

### 1. Install Ansible

```bash
sudo apt update
sudo apt install -y ansible
```

### 2. Test Connection

```bash
cd /root/idurar-erp-crm/ansible
ansible all -i hosts.ini -m ping
```

### 3. Run Playbook

```bash
ansible-playbook -i hosts.ini playbook.yml
```

## 📸 Screenshots for Submission

1. **Ansible version:**
   ```bash
   ansible --version
   ```

2. **Inventory:**
   ```bash
   cat hosts.ini
   ansible-inventory -i hosts.ini --list
   ```

3. **Connection test:**
   ```bash
   ansible all -i hosts.ini -m ping
   ```

4. **Playbook execution:**
   ```bash
   ansible-playbook -i hosts.ini playbook.yml
   ```

5. **Verification:**
   ```bash
   docker --version
   node --version
   nginx -v
   ```

## ✅ Assignment Requirements Met

- ✅ **Task D1:** Inventory with 4 servers (2 roles)
- ✅ **Task D2:** Playbook automates:
  - Docker installation
  - Node.js installation
  - Nginx installation
  - Python installation
  - Service configuration
  - Directory creation

## 🎓 Notes

- Uses `localhost` with `ansible_connection=local` for easy testing
- All 4 servers configured on same machine (for demonstration)
- For production, update `hosts.ini` with actual server IPs
- Playbook is idempotent (safe to run multiple times)
