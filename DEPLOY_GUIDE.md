# Deploying to a Linux VM

This guide explains how to deploy the Developer Avatar application to a Linux VM (e.g., Ubuntu) and access the UI from your local machine.

## Prerequisites

-   A Linux VM (Ubuntu 20.04/22.04 recommended) with SSH access.
-   Access to the internet from the VM.

## Step 1: Update Code on VM

Since you already have the code on the VM, you just need to update it with the latest changes (including the new scripts and config).

**Option A: If you use Git (Recommended)**
On the VM:
```bash
cd developer_avatar
git pull origin main
```

**IMPORTANT:** You must update the `.env` file with your new Jira credentials!
```bash
nano backend/.env
```
(Paste the new JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN, then Ctrl+O, Enter, Ctrl+X to save)

**Option B: Re-upload using SCP**
From your local machine:
```bash
scp -i ".\THTN-VM-9_key.pem" -r developer_avatar user-vm1901@4.240.105.241:~/
```


## Step 2: Run Setup Script

SSH into your VM:

```bash
ssh <user>@<vm-ip>
```

Navigate to the project directory and run the setup script:

```bash
cd developer_avatar
chmod +x setup_vm.sh
./setup_vm.sh
```

**IMPORTANT:**
The setup script creates a `backend/.env` file from `.env.example`. You **MUST** edit this file to add your Azure OpenAI keys!

```bash
nano backend/.env
# Paste your Azure keys here, save and exit (Ctrl+O, Enter, Ctrl+X)
```

## Step 3: Restart the Application

Since the app is already running, we need to restart it to apply changes.

```bash
pm2 restart backend
pm2 restart frontend
```

Or if you want to use the start script (it handles starting/restarting):
```bash
chmod +x start_app.sh
./start_app.sh
```

## Step 4: Access the UI

Since your VM is headless (no monitor/GUI), you need a way to see the website running on port 3000. Here are 3 ways:

### Option A: Public IP (Easiest if Firewall allows)
If your VM has a public IP and you have opened port 3000 in the firewall (e.g., Azure NSG, AWS Security Group):
1.  Go to `http://<vm-public-ip>:3000` in your browser.

### Option B: SSH Tunneling (Secure, no external config)
You can "forward" the port from the VM to your local machine using SSH.
Run this command on **your local machine**:

```bash
ssh -i ".\THTN-VM-9_key.pem" -L 3000:localhost:3000 -L 8000:localhost:8000 user-vm1901@4.240.105.241
```
Leave this terminal window open. Now go to `http://localhost:3000` on your local machine.

### Option C: ngrok (Public URL)
If you cannot open firewall ports, use `ngrok` to create a public URL. The setup script installed it for you.

On the VM, run:
```bash
ngrok http 3000
```
This will display a URL like `https://random-name.ngrok-free.app`. Open that URL on your local machine.
