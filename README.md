# Auto Water Purchase Script

Automated Python script for monthly water payment via Standard Bank online banking and SMS notification, designed to run on a Raspberry Pi via cron job.

## Features

- Automated Standard Bank login and navigation
- Beneficiary search and payment (R500 to "enbaya")
- Screenshot capture of payment confirmation
- SMS notification via Twilio
- Optional SMS forwarding capability
- Scheduled execution (1st of each month at 00:01)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:
- `STANDARD_BANK_USERNAME`: Your Standard Bank username
- `STANDARD_BANK_PASSWORD`: Your Standard Bank password
- `PHONE_NUMBER_USER`: Your phone number (with country code)
- `PHONE_NUMBER_ENBAYA`: Recipient phone number for SMS
- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number
- `FORCE_RUN`: Set to `true` to override timing check (for testing)

### 3. Set Up Cron Job

Run the setup script to automatically configure the cron job:

```bash
./setup_cron.sh
```

This will schedule the script to run at 00:01 on the 1st of every month.

## Testing

To test the script without waiting for the scheduled time:

```bash
FORCE_RUN=true python3 auto_water_purchase.py
```

## Files

- `auto_water_purchase.py`: Main script
- `requirements.txt`: Python dependencies
- `setup_cron.sh`: Cron job setup script
- `.env.example`: Environment variables template
- `auto_water_purchase.log`: Log file (created when script runs)

## Security Notes

- Never commit your `.env` file to version control
- Store your credentials securely
- Run on a secure network when possible
- Regularly monitor logs for any issues

## Troubleshooting

1. Check the log file: `auto_water_purchase.log`
2. Verify environment variables are set correctly
3. Ensure Chrome/Chromium is installed for Selenium WebDriver
4. Check Twilio account credits and phone number configuration