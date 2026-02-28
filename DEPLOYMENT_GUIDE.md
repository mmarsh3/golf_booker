# Cloud Deployment Guide

Step-by-step guide to deploy the Golf Booking Bot on a cloud server.

## Quick Start (DigitalOcean Example)

### 1. Create Droplet

1. Log into DigitalOcean
2. Create Droplet:
   - **Image:** Ubuntu 22.04 LTS
   - **Plan:** Basic ($4-6/month)
   - **CPU:** 1 vCPU, 512MB-1GB RAM
   - **Region:** Choose closest to EST (New York/Toronto)
3. Add SSH key or create root password
4. Click "Create Droplet"

### 2. Connect to Server

```bash
ssh root@YOUR_DROPLET_IP
```

### 3. Run Automated Setup

```bash
# Create installation directory
mkdir -p /opt/golf_booker
cd /opt/golf_booker

# Download setup script (if you have the repo)
curl -O https://your-repo.com/deploy/setup_server.sh

# Or create it manually
nano setup_server.sh
# Paste the contents from deploy/setup_server.sh

# Make executable and run
chmod +x setup_server.sh
./setup_server.sh
```

### 4. Upload Your Code

**Option A: Using SCP (from your local machine)**

```bash
# From your local machine
cd /Users/michaelmarsh/Desktop
scp -r golf_booker root@YOUR_DROPLET_IP:/opt/
```

**Option B: Using Git**

```bash
# On the server
cd /opt/golf_booker
git clone YOUR_REPO_URL .
```

**Option C: Manual Upload (if no git)**

Use SFTP client (FileZilla, Cyberduck, etc.) to upload files to `/opt/golf_booker`

### 5. Configure Environment

```bash
cd /opt/golf_booker

# Create .env file
nano .env
```

Paste your credentials:
```env
GOLF_USERNAME=your_email@example.com
GOLF_PASSWORD=your_password_here
NUM_PLAYERS=4
BOOKING_TIME=06:00
TIMEZONE=America/New_York
HEADLESS=True
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

### 6. Install Python Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 7. Test the Bot

```bash
# Run a test (will attempt booking immediately)
python booking_bot.py
```

Check the output. If errors occur:
- View logs: `cat logs/booking_*.log`
- View screenshots: `ls -lh screenshots/`

### 8. Install as Service

```bash
chmod +x deploy/install_service.sh
./deploy/install_service.sh
```

### 9. Verify Service is Running

```bash
# Check status
systemctl status golf-booker

# View live logs
tail -f logs/scheduler.log
```

You should see something like:
```
Golf Booking Bot Scheduler Starting
Timezone: America/New_York
Scheduled run time: 06:00 America/New_York
Next run time: 2024-XX-XX 06:00:00-05:00
Scheduler is now running.
```

## Post-Deployment Checklist

- [ ] Service is running: `systemctl status golf-booker`
- [ ] Logs are being written: `ls -lh logs/`
- [ ] Next run time is correct: Check scheduler.log
- [ ] Server timezone is correct: `timedatectl`
- [ ] Credentials are working: Test manually first

## Monitoring from Your Phone

### Setup Email Alerts (Optional Enhancement)

You can enhance the bot to send email notifications. Add to `booking_bot.py`:

```python
import smtplib
from email.mime.text import MIMEText

def send_notification(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = 'your-email@gmail.com'

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your-email@gmail.com', 'app-password')
        smtp.send_message(msg)

# Call after booking succeeds or fails
send_notification("Golf Booking", "Booking completed!")
```

### Check Status via SSH from Phone

Use SSH apps like:
- **iOS:** Termius, Prompt
- **Android:** JuiceSSH, Termux

Connect and run:
```bash
tail -20 /opt/golf_booker/logs/scheduler.log
```

## Cost Breakdown

### Cloud Providers Comparison

| Provider | Plan | RAM | Monthly | Annual |
|----------|------|-----|---------|--------|
| DigitalOcean | Basic Droplet | 512MB | $4 | $48 |
| DigitalOcean | Basic Droplet | 1GB | $6 | $72 |
| Linode | Nanode | 1GB | $5 | $60 |
| Vultr | Cloud Compute | 512MB | $3.50 | $42 |
| AWS EC2 | t2.micro | 1GB | Free* | Free* |

*AWS Free Tier: 750 hours/month for 12 months

**Recommendation:** DigitalOcean $6/month (1GB) for reliability

## Updating the Bot

```bash
# SSH into server
ssh root@YOUR_DROPLET_IP

# Stop service
systemctl stop golf-booker

# Update code (if using git)
cd /opt/golf_booker
git pull

# Or re-upload changed files via SCP

# Restart service
systemctl start golf-booker

# Verify
systemctl status golf-booker
```

## Troubleshooting

### Service Won't Start

```bash
# Check detailed logs
journalctl -u golf-booker -n 50

# Check for Python errors
cd /opt/golf_booker
source venv/bin/activate
python scheduler.py
```

### Chrome Not Found

```bash
# Verify Chrome installation
google-chrome --version

# If missing, reinstall
apt install -y google-chrome-stable
```

### Wrong Timezone

```bash
# Check current timezone
timedatectl

# Set to EST
timedatectl set-timezone America/New_York
systemctl restart golf-booker
```

### Booking Failed

1. Check screenshots: `ls -lh screenshots/`
2. Download screenshot: `scp root@YOUR_IP:/opt/golf_booker/screenshots/error_*.png ~/Desktop/`
3. Review to see where it failed
4. Website may have changed - update selectors in `booking_bot.py`

## Security Hardening

### Create Non-Root User

```bash
# Create user
adduser golfbot
usermod -aG sudo golfbot

# Copy files
cp -r /opt/golf_booker /home/golfbot/
chown -R golfbot:golfbot /home/golfbot/golf_booker

# Update service to run as golfbot
nano /etc/systemd/system/golf-booker.service
# Change: User=root to User=golfbot
# Change: WorkingDirectory=/opt/golf_booker to WorkingDirectory=/home/golfbot/golf_booker
```

### Enable Firewall

```bash
ufw allow 22
ufw enable
```

### Auto-Updates

```bash
apt install unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
```

## Backup Strategy

### Backup Logs Weekly

```bash
# Create backup script
nano /usr/local/bin/backup-golf-logs.sh
```

```bash
#!/bin/bash
tar -czf /root/golf-logs-$(date +%Y%m%d).tar.gz /opt/golf_booker/logs/
find /root/golf-logs-*.tar.gz -mtime +30 -delete
```

```bash
chmod +x /usr/local/bin/backup-golf-logs.sh

# Add to crontab (runs Sundays at 3 AM)
crontab -e
# Add: 0 3 * * 0 /usr/local/bin/backup-golf-logs.sh
```

## Maintenance

### Weekly Check (5 minutes)

```bash
# SSH in
ssh root@YOUR_IP

# Check service status
systemctl status golf-booker

# Review recent logs
tail -50 /opt/golf_booker/logs/scheduler.log

# Check disk space
df -h

# Update system
apt update && apt upgrade -y
```

## Support Resources

- DigitalOcean Docs: https://docs.digitalocean.com/
- Ubuntu Server Guide: https://ubuntu.com/server/docs
- Selenium Python Docs: https://selenium-python.readthedocs.io/

Good luck with your automated bookings! 🏌️
