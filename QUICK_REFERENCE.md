# Quick Reference Guide

## Essential Commands

### On Your Cloud Server

#### Service Management
```bash
# Check if running
systemctl status golf-booker

# View live logs
tail -f /opt/golf_booker/logs/scheduler.log

# Restart service
systemctl restart golf-booker

# Stop service
systemctl stop golf-booker

# Start service
systemctl start golf-booker
```

#### View Logs
```bash
# Latest scheduler log
tail -50 /opt/golf_booker/logs/scheduler.log

# Latest booking log
ls -lt /opt/golf_booker/logs/booking_*.log | head -1 | awk '{print $9}' | xargs cat

# All logs from today
grep "$(date +%Y-%m-%d)" /opt/golf_booker/logs/scheduler.log
```

#### Check Screenshots
```bash
# List screenshots
ls -lht /opt/golf_booker/screenshots/

# Download screenshot to your computer
# (Run this from your LOCAL machine)
scp root@YOUR_IP:/opt/golf_booker/screenshots/error_*.png ~/Desktop/
```

#### Update Code
```bash
# Stop service
systemctl stop golf-booker

# Navigate to directory
cd /opt/golf_booker

# Pull latest changes (if using git)
git pull

# Or upload new files via scp from local machine:
# scp booking_bot.py root@YOUR_IP:/opt/golf_booker/

# Restart service
systemctl start golf-booker
```

#### Test Manually
```bash
cd /opt/golf_booker
source venv/bin/activate
python booking_bot.py
```

### From Your Local Computer

#### Connect to Server
```bash
ssh root@YOUR_SERVER_IP
```

#### Upload Files
```bash
# Upload single file
scp booking_bot.py root@YOUR_IP:/opt/golf_booker/

# Upload entire directory
scp -r golf_booker root@YOUR_IP:/opt/
```

#### Download Logs
```bash
# Download all logs
scp -r root@YOUR_IP:/opt/golf_booker/logs ~/Desktop/golf_logs

# Download screenshots
scp -r root@YOUR_IP:/opt/golf_booker/screenshots ~/Desktop/golf_screenshots
```

## File Locations

| File/Directory | Purpose |
|---------------|---------|
| `/opt/golf_booker/` | Main application directory |
| `/opt/golf_booker/logs/` | All log files |
| `/opt/golf_booker/screenshots/` | Debug screenshots |
| `/opt/golf_booker/.env` | Your credentials (KEEP SECURE!) |
| `/etc/systemd/system/golf-booker.service` | Service configuration |

## Troubleshooting Quick Fixes

### Service Won't Start
```bash
journalctl -u golf-booker -n 50
# Look for error messages
```

### Check Chrome
```bash
google-chrome --version
```

### Verify Timezone
```bash
timedatectl
# Should show: America/New_York
```

### Test Internet Connection
```bash
ping -c 3 golfstpete.com
```

### Check Disk Space
```bash
df -h
```

### Update Environment Variables
```bash
nano /opt/golf_booker/.env
# Make changes, save with Ctrl+X, Y, Enter
systemctl restart golf-booker
```

## Monitoring Checklist

Run this weekly:

```bash
# 1. Check service is running
systemctl status golf-booker

# 2. Check recent logs
tail -50 /opt/golf_booker/logs/scheduler.log

# 3. Verify next run time is correct
grep "Next run time" /opt/golf_booker/logs/scheduler.log | tail -1

# 4. Check disk space
df -h

# 5. Update system
apt update && apt upgrade -y
```

## Emergency Contacts

| Issue | Solution |
|-------|----------|
| Can't SSH in | Check DigitalOcean console / Reset root password |
| Service crashed | `systemctl restart golf-booker` |
| Chrome errors | `apt install --reinstall google-chrome-stable` |
| Website changed | Update selectors in `booking_bot.py` |
| Wrong time | `timedatectl set-timezone America/New_York` |

## Quick Setup Reminder

1. Create Ubuntu 22.04 server
2. SSH in: `ssh root@IP`
3. Run: `deploy/setup_server.sh`
4. Upload code
5. Create `.env` with credentials
6. Install deps: `pip install -r requirements.txt`
7. Run: `deploy/install_service.sh`
8. Verify: `systemctl status golf-booker`

## Next Run Time

To see when the bot will run next:

```bash
grep "Next run time" /opt/golf_booker/logs/scheduler.log | tail -1
```

Should show: `Next run time: YYYY-MM-DD 06:00:00-05:00`

## Cost Reminder

- DigitalOcean: $4-6/month
- AWS EC2 (free tier): $0 for first year
- Linode/Vultr: $3.50-5/month

**Don't forget to monitor your billing!**

---

*Keep this file handy for quick reference when managing your bot.*
