# GitHub Actions Setup Guide

Complete guide to deploying the Golf Booking Bot using GitHub Actions (FREE!)

## Why GitHub Actions?

- ✅ **FREE** - 2,000 minutes/month for private repos, unlimited for public
- ✅ **No Server Management** - GitHub handles everything
- ✅ **Built-in Secrets** - Secure credential storage
- ✅ **Easy Scheduling** - Simple cron syntax
- ✅ **Logs & Artifacts** - Automatic log storage and screenshots
- ✅ **Manual Triggers** - Test runs on demand

## Setup Steps

### 1. Create a GitHub Repository

```bash
# Initialize git repository (if not already done)
cd /Users/michaelmarsh/Desktop/golf_booker
git init

# Create .gitignore (already exists)
# Make sure .env is in .gitignore (already done)

# Add all files
git add .

# Commit
git commit -m "Initial commit - Golf booking bot"

# Create repository on GitHub.com
# Go to https://github.com/new
# Repository name: golf-tee-time-booker
# Privacy: Private (recommended) or Public

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/golf-tee-time-booker.git
git branch -M main
git push -u origin main
```

### 2. Add Secrets to GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these two secrets:

**Secret 1:**
- Name: `GOLF_USERNAME`
- Value: Your golf course login email/username

**Secret 2:**
- Name: `GOLF_PASSWORD`
- Value: Your golf course password

### 3. Enable GitHub Actions

The workflow file is already in `.github/workflows/book-tee-time.yml`

GitHub Actions will automatically:
- Run at **6:00 AM EST** every day (11:00 AM UTC)
- Install Chrome and dependencies
- Run the booking bot
- Upload logs and screenshots

### 4. Test the Workflow

**Manual Test Run:**

1. Go to **Actions** tab in your GitHub repository
2. Click **Book Golf Tee Time** workflow
3. Click **Run workflow** dropdown
4. Click **Run workflow** button

This triggers an immediate test run so you can verify everything works.

### 5. Monitor Runs

**View Workflow Runs:**
- Go to **Actions** tab
- Click on any run to see details
- Check each step for success/failure

**Download Logs/Screenshots:**
- Click on a workflow run
- Scroll to **Artifacts** section at bottom
- Download logs and screenshots

## Scheduling Details

### Default Schedule
```yaml
cron: '0 11 * * *'  # 11 AM UTC = 6 AM EST
```

This runs at:
- **6:00 AM EST** (Eastern Standard Time, Nov-Mar)
- **7:00 AM EDT** (Eastern Daylight Time, Mar-Nov)

### Adjust Schedule for DST (Optional)

If you want it to run at 6 AM year-round:

**During EDT (March-November):**
```yaml
cron: '0 10 * * *'  # 10 AM UTC = 6 AM EDT
```

**During EST (November-March):**
```yaml
cron: '0 11 * * *'  # 11 AM UTC = 6 AM EST
```

You'll need to manually update the workflow file twice a year, or just accept the 1-hour shift.

### Change Booking Time

Edit `.github/workflows/book-tee-time.yml`:

```yaml
schedule:
  - cron: '0 10 * * *'  # Change hour (0-23 in UTC)
```

Cron format: `minute hour day month weekday`
- `0 10 * * *` = 10:00 AM UTC daily
- `30 9 * * 1-5` = 9:30 AM UTC, Monday-Friday only
- `0 11 * * 0,6` = 11:00 AM UTC, weekends only

Use [crontab.guru](https://crontab.guru/) to build cron expressions.

## Troubleshooting

### Workflow Not Running

**Check:**
1. Is the repository public or do you have Actions minutes remaining?
2. Go to **Settings** → **Actions** → **General** → Ensure "Allow all actions" is selected
3. Check **Actions** tab for any error messages

### Booking Failed

1. Go to **Actions** tab
2. Click the failed run
3. Download artifacts (logs and screenshots)
4. Review screenshots to see where it failed
5. Check if website structure changed

### Update Bot Code

```bash
# Make changes locally
git add .
git commit -m "Update selectors"
git push

# GitHub will use the updated code in next run
```

### Test Changes Immediately

1. Go to **Actions** tab
2. Click **Book Golf Tee Time**
3. **Run workflow** → **Run workflow**

## Cost

### Free Tier
- **Public repos**: Unlimited minutes
- **Private repos**: 2,000 minutes/month

### Usage Estimate
- Each booking run: ~5 minutes
- Daily runs: 5 min × 30 days = 150 minutes/month
- **Well within free tier!**

## Security

### Secrets Are Secure
- Secrets are encrypted and never exposed in logs
- Only accessible to workflow runs
- Can't be viewed after creation (only updated)

### Keep Repository Private
- If using private repo, your credentials are fully private
- If public, secrets are still secure but code is visible

## Monitoring & Notifications

### Email Notifications (Built-in)

GitHub automatically emails you when:
- Workflow fails
- First failure after success
- Success after failure

Configure in **Settings** → **Notifications** → **Actions**

### Slack/Discord Notifications (Optional)

Add to workflow file:

```yaml
- name: Notify on success
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "✅ Golf tee time booked successfully!"
      }
```

## Advanced: Multiple Courses or Times

Create multiple workflow files:

`.github/workflows/morning-booking.yml`:
```yaml
name: Morning Booking
on:
  schedule:
    - cron: '0 10 * * *'
```

`.github/workflows/evening-booking.yml`:
```yaml
name: Evening Booking
on:
  schedule:
    - cron: '0 18 * * *'
```

## FAQ

**Q: Can I test without waiting until 6 AM?**
A: Yes! Use **Run workflow** button in Actions tab.

**Q: What if the booking fails one day?**
A: You'll receive an email. Check logs/screenshots to diagnose. Fix code and it will try again next day.

**Q: How do I stop the daily bookings?**
A: Delete the workflow file or disable it in **Actions** settings.

**Q: Can I change which day it books?**
A: Yes, edit `booking_bot.py`, change `timedelta(days=7)` to desired days ahead.

**Q: What about holidays when course is closed?**
A: Bot will fail gracefully (no harm done). You can disable workflow temporarily.

## Comparison: GitHub Actions vs Cloud Server

| Feature | GitHub Actions | Cloud Server |
|---------|---------------|--------------|
| **Cost** | FREE | $4-6/month |
| **Setup** | 5 minutes | 30-60 minutes |
| **Maintenance** | None | Updates, monitoring |
| **Logs** | Built-in UI | SSH required |
| **Reliability** | GitHub SLA | Your responsibility |
| **Secrets** | Encrypted | Manual .env |

**Recommendation:** Use GitHub Actions! It's easier, free, and more reliable.

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Add secrets (username, password)
3. ✅ Push code to GitHub
4. ✅ Test with manual workflow run
5. ✅ Wait for first scheduled run at 6 AM EST

**You're done!** The bot will now run automatically every morning.

---

Need help? Check the logs in the **Actions** tab and review screenshots to debug issues.
