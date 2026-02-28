# Golf Tee Time Booking Bot

Automated Selenium bot that books golf tee times at Mangrove Bay Golf Course 7 days in advance, triggered daily at 6:00 AM EST.

## Features

- ✅ Runs at exactly 6:00 AM EST daily
- ✅ Books 4-some for first available tee time, 7 days in advance
- ✅ Automatic login and navigation
- ✅ Headless browser operation
- ✅ Comprehensive logging and error screenshots
- ✅ **FREE deployment on GitHub Actions** (recommended)
- ✅ Alternative cloud server deployment

## 🚀 Quick Start

**Get running in 5 minutes:** See [QUICKSTART.md](QUICKSTART.md)

**Recommended:** Deploy to GitHub Actions (FREE, no server needed)

## Deployment Options

### 1. GitHub Actions (Recommended) ⭐

**Why GitHub Actions:**
- ✅ **FREE** - No cost!
- ✅ **No Server Management** - GitHub handles everything
- ✅ **5-Minute Setup** - Easiest option
- ✅ **Built-in Logs** - Easy monitoring
- ✅ **Reliable** - Backed by GitHub SLA

**Setup:** See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)

### 2. Cloud Server (Alternative)

**Cost:** $4-6/month
**Setup:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## Prerequisites

- GitHub account (for GitHub Actions) OR Cloud server
- Python 3.8+ (for local testing)
- Golf course account credentials

## Local Setup (Testing)

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Credentials

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your credentials
nano .env
```

Add your credentials:
```
GOLF_USERNAME=your_email@example.com
GOLF_PASSWORD=your_password
NUM_PLAYERS=4
```

### 3. Test the Bot (Manual Run)

```bash
# Run the bot once to test
python booking_bot.py
```

Check the `logs/` directory for output and `screenshots/` for debugging images.

### 4. Test the Scheduler (Optional)

```bash
# Run the scheduler (will wait until 6 AM to execute)
python scheduler.py
```

## Cloud Deployment (24/7 Operation)

**Important:** Your laptop cannot reliably run this while sleeping. You need a cloud server.

### Recommended Providers:

1. **DigitalOcean** - $4-6/month droplet
2. **AWS EC2** - t2.micro (free tier eligible)
3. **Linode** - $5/month
4. **Vultr** - $3.50/month

### Deployment Steps (Ubuntu Server)

#### 1. Create a Server

Create an Ubuntu 22.04 server instance on your chosen provider.

#### 2. Connect via SSH

```bash
ssh root@your_server_ip
```

#### 3. Install Dependencies

```bash
# Update system
apt update && apt upgrade -y

# Install Python 3 and pip
apt install python3 python3-pip python3-venv -y

# Install Chrome dependencies
apt install -y wget unzip curl gnupg

# Install Google Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt update
apt install -y google-chrome-stable

# Verify Chrome installation
google-chrome --version
```

#### 4. Setup Application

```bash
# Create application directory
mkdir -p /opt/golf_booker
cd /opt/golf_booker

# Upload your code (use scp, git, or manual copy)
# Option A: Using git
git clone your_repository_url .

# Option B: Using scp from your local machine
# scp -r /Users/michaelmarsh/Desktop/golf_booker/* root@your_server_ip:/opt/golf_booker/

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 5. Configure Environment

```bash
# Create .env file
nano .env
```

Add your credentials:
```
GOLF_USERNAME=your_email@example.com
GOLF_PASSWORD=your_password
NUM_PLAYERS=4
BOOKING_TIME=06:00
TIMEZONE=America/New_York
HEADLESS=True
```

#### 6. Create Systemd Service

This keeps the scheduler running 24/7, even after reboots.

```bash
# Create service file
nano /etc/systemd/system/golf-booker.service
```

Add this content:
```ini
[Unit]
Description=Golf Tee Time Booking Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/golf_booker
Environment="PATH=/opt/golf_booker/venv/bin"
ExecStart=/opt/golf_booker/venv/bin/python scheduler.py
Restart=always
RestartSec=10
StandardOutput=append:/opt/golf_booker/logs/service.log
StandardError=append:/opt/golf_booker/logs/service_error.log

[Install]
WantedBy=multi-user.target
```

#### 7. Start the Service

```bash
# Create log directory
mkdir -p /opt/golf_booker/logs
mkdir -p /opt/golf_booker/screenshots

# Reload systemd
systemctl daemon-reload

# Enable service to start on boot
systemctl enable golf-booker

# Start the service
systemctl start golf-booker

# Check status
systemctl status golf-booker
```

## Monitoring

### View Logs

```bash
# Real-time logs
tail -f /opt/golf_booker/logs/scheduler.log

# Service logs
journalctl -u golf-booker -f

# View all recent logs
ls -lht /opt/golf_booker/logs/
```

### Check Service Status

```bash
systemctl status golf-booker
```

### Restart Service

```bash
systemctl restart golf-booker
```

## Troubleshooting

### Bot Not Running

```bash
# Check service status
systemctl status golf-booker

# Check logs for errors
tail -100 /opt/golf_booker/logs/scheduler.log

# Verify Chrome is installed
google-chrome --version

# Test bot manually
cd /opt/golf_booker
source venv/bin/activate
python booking_bot.py
```

### Login Failures

- Verify credentials in `.env`
- Check screenshots in `screenshots/` directory
- Website may have changed - inspect error screenshots

### Booking Failures

- Check if tee times are actually available 7 days out
- Review screenshots to see where the process failed
- Website structure may have changed

## Website Changes

If the golf course website changes its layout, you may need to update the XPath selectors in `booking_bot.py`. Check the screenshots to identify which step failed, then update the corresponding selectors.

## Security Notes

- ✅ Never commit `.env` to version control
- ✅ Use strong passwords for your server
- ✅ Keep the server updated: `apt update && apt upgrade`
- ✅ Consider using SSH keys instead of passwords
- ✅ Enable a firewall: `ufw allow 22 && ufw enable`

## Cost Estimate

- **Cloud Server:** $4-6/month
- **Total:** ~$50-70/year for 24/7 automated booking

## Architecture

```
┌─────────────────┐
│   Cloud Server  │
│   (Always On)   │
├─────────────────┤
│   Scheduler     │ ← Runs at 6 AM EST daily
│   (APScheduler) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Booking Bot    │
│  (Selenium)     │
├─────────────────┤
│ 1. Login        │
│ 2. Select Date  │
│ 3. Pick Time    │
│ 4. Book 4-some  │
└─────────────────┘
```

## Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Review screenshots in `screenshots/` directory
3. Verify credentials and configuration
4. Test manually with `python booking_bot.py`

## License

Private use only
