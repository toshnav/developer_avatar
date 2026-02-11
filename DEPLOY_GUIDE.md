# Deploying to a Linux VM

This guide explains how to deploy the Developer Avatar application to a Linux VM (e.g., Ubuntu) and access the UI from your local machine.

## Prerequisites

-   A Linux VM (Ubuntu 20.04/22.04 recommended) with SSH access.
-   Access to the internet from the VM.

## Step 1: Transfer Code to VM

You can use `scp` (Secure Copy) to transfer the project files from your local machine to the VM.

Run this command **from your local machine (Windows PowerShell/WSL)**:

```bash
# Replace <user> and <vm-ip> with your VM details
# Make sure you are in the directory containing 'developer_avatar'
scp -r developer_avatar <user>@<vm-ip>:~/developer_avatar
```

Alternatively, if you are using git, you can just `git clone` your repository on the VM.

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

## Step 3: Start the Application

We use `pm2` to keep the application running in the background.

```bash
chmod +x start_app.sh
./start_app.sh
```

This will start:
-   Backend on port `8000`
-   Frontend on port `3000`

## Step 4: Access the UI

Since your VM is headless (no monitor/GUI), you need a way to see the website running on port 3000. Here are 3 ways:

### Option A: Public IP (Easiest if Firewall allows)
If your VM has a public IP and you have opened port 3000 in the firewall (e.g., Azure NSG, AWS Security Group):
1.  Go to `http://<vm-public-ip>:3000` in your browser.

### Option B: SSH Tunneling (Secure, no external config)
You can "forward" the port from the VM to your local machine using SSH.
Run this command on **your local machine**:

```bash
ssh -L 3000:localhost:3000 <user>@<vm-ip>
```
Leave this terminal window open. Now go to `http://localhost:3000` on your local machine.

### Option C: ngrok (Public URL)
If you cannot open firewall ports, use `ngrok` to create a public URL. The setup script installed it for you.

On the VM, run:
```bash
ngrok http 3000
```
This will display a URL like `https://random-name.ngrok-free.app`. Open that URL on your local machine.
