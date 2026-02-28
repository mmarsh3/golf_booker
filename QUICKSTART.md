# Quick Start - 5 Minutes to Automated Bookings!

Get your golf tee time bot running on GitHub Actions in 5 minutes.

## Prerequisites

- GitHub account (free)
- Golf course login credentials
- Git installed on your computer

## Step 1: Test Locally (2 minutes)

```bash
cd golf_booker

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
nano .env  # Add your credentials

# Test the bot
python test_booking.py
```

Watch it book! If it works, proceed to deployment.

## Step 2: Deploy to GitHub Actions (3 minutes)

### A. Create Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Golf booking bot"

# Create repository on GitHub.com
# Go to: https://github.com/new
# Name: golf-tee-time-booker
# Privacy: Private (recommended)

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/golf-tee-time-booker.git
git branch -M main
git push -u origin main
```

### B. Add Secrets

1. Go to your repo on GitHub.com
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret**:
   - Name: `GOLF_USERNAME`
   - Value: your_email@example.com
4. **New repository secret**:
   - Name: `GOLF_PASSWORD`
   - Value: your_password

### C. Test It

1. Go to **Actions** tab
2. Click **Book Golf Tee Time**
3. **Run workflow** → **Run workflow**
4. Watch it run!
5. Check **Artifacts** for logs/screenshots

## Done! 🎉

Your bot will now run automatically at **6:00 AM EST** every day!

## What Happens Next?

- **Daily at 6 AM EST**: Bot runs automatically
- **Emails**: You get notified if it fails
- **Logs**: Available in Actions tab for 7 days
- **Cost**: FREE (GitHub Actions)

## Monitoring

**Check if it ran:**
- Go to **Actions** tab in your repository
- See all runs with timestamps and status

**View logs:**
- Click on any run
- Download artifacts (logs and screenshots)

**Test changes:**
- Push code to GitHub
- Use **Run workflow** button to test immediately

## Common Commands

```bash
# Update code
git add .
git commit -m "Update bot"
git push

# View local logs
ls -lh logs/
ls -lh screenshots/

# Test locally
python test_booking.py
```

## Troubleshooting

**Bot fails?**
1. Check **Actions** tab for error
2. Download artifacts
3. Review screenshots to see where it failed
4. Website may have changed - update selectors

**Change booking time?**
- Edit `.github/workflows/book-tee-time.yml`
- Update cron schedule
- Push changes

**Stop daily bookings?**
- Delete workflow file or disable in Actions settings

## Support

- Full setup guide: `GITHUB_ACTIONS_SETUP.md`
- Cloud deployment: `DEPLOYMENT_GUIDE.md`
- Command reference: `QUICK_REFERENCE.md`

## Cost Breakdown

| Method | Cost/month | Setup Time | Reliability |
|--------|-----------|------------|-------------|
| **GitHub Actions** | FREE | 5 min | ★★★★★ |
| Cloud Server | $4-6 | 30 min | ★★★★☆ |
| Laptop | $0 | 10 min | ★★☆☆☆ (sleeps) |

**Recommended:** GitHub Actions (free, reliable, easy)

---

**You're all set!** Enjoy your automated golf bookings! ⛳
