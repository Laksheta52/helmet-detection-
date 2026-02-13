# 📱 SMS Notification Setup Guide

## Overview

The Third Eye system now automatically sends SMS notifications to vehicle owners when violations are detected!

## Features

✅ **Automatic License Plate Detection** - Already working with EasyOCR  
✅ **Vehicle Database Lookup** - Maps license plates to owner phone numbers  
✅ **SMS Notifications** - Sends penalty alerts via Twilio  
✅ **Violation Details** - Includes violation type, penalty amount, and legal section  

## How It Works

1. System detects traffic violation
2. EasyOCR extracts license plate number
3. Lookup phone number in vehicle database
4. Send SMS notification automatically via Twilio
5. Driver receives penalty alert instantly!

---

## Setup Instructions

### Demo Mode (No SMS - Just Testing)

**Current Status:** ✅ Already working!

The system is in DEMO mode by default. When violations are detected:
- License plates ARE extracted
- SMS would be sent BUT...
- Instead, notification is logged to console
- No actual SMS sent

**Test it now:**
1. Upload an image with a violation
2. Check backend terminal for demo SMS output
3. See what message would be sent

---

### Production Mode (Real SMS via Twilio)

To send actual SMS messages, you need a Twilio account:

#### Step 1: Get Twilio Credentials (Free Trial Available)

1. Go to https://www.twilio.com/try-twilio
2. Sign up for free account ($15 free credit)
3. Get your credentials:
   - **Account SID** (looks like: ACxxxxxxxxxxxxxxx)
   - **Auth Token** (looks like: your-auth-token)
   - **Phone Number** (looks like: +1234567890)

#### Step 2: Set Environment Variables

**On Windows (PowerShell):**
```powershell
# Set for current session
$env:TWILIO_ACCOUNT_SID="your_account_sid_here"
$env:TWILIO_AUTH_TOKEN="your_auth_token_here"
$env:TWILIO_PHONE_NUMBER="+1234567890"

# Set permanently
[System.Environment]::SetEnvironmentVariable("TWILIO_ACCOUNT_SID", "your_sid", "User")
[System.Environment]::SetEnvironmentVariable("TWILIO_AUTH_TOKEN", "your_token", "User")
[System.Environment]::SetEnvironmentVariable("TWILIO_PHONE_NUMBER", "+1234567890", "User")
```

**On Linux/Mac:**
```bash
export TWILIO_ACCOUNT_SID="your_account_sid_here"
export TWILIO_AUTH_TOKEN="your_auth_token_here"
export TWILIO_PHONE_NUMBER="+1234567890"

# Add to ~/.bashrc or ~/.zshrc for permanent
```

#### Step 3: Install Twilio Package

```bash
cd backend
pip install twilio
```

#### Step 4: Restart Backend

```bash
cd backend
.\start.bat
```

You should see:
```
✅ SMS service initialized (Twilio)
📱 SMS notifications: ENABLED
```

---

## Vehicle Registration Database

### Default Demo Data

The system includes 3 demo vehicles:

| License Plate | Phone Number | Owner |
|---------------|--------------|-------|
| DL-01-AB-1234 | +919876543210 | Demo Driver 1 |
| DL-02-CD-5678 | +919876543211 | Demo Driver 2 |
| MH-12-EF-9012 | +919876543212 | Demo Driver 3 |

**Location:** `backend/vehicle_db.json`

### Adding Your Own Vehicles

**Option 1: Edit JSON File**
```json
{
  "YOUR-PLATE-123": {
    "phone": "+919999999999",
    "owner": "Owner Name",
    "vehicle_type": "Motorcycle"
  }
}
```

**Option 2: Use API Endpoint** (Coming soon)

---

## SMS Message Format

When a violation is detected, the driver receives:

```
🚨 TRAFFIC VIOLATION ALERT

Vehicle: DL-01-AB-1234
Date: 2026-02-02 21:35

VIOLATIONS DETECTED:
• Riding Without Helmet - ₹1,000
• Triple Riding - ₹1,000

TOTAL PENALTY: ₹2,000

Section: Motor Vehicles Act, 1988

⚠️ Please pay the fine within 30 days.

Payment: Visit nearest RTO or online portal.

- Traffic Police Department
```

---

## Testing SMS Notifications

### Test with Demo Plates

1. **Upload image** with violation (helmet, triple riding, etc.)
2. **System extracts** license plate
3. **If plate matches** demo database → SMS sent!
4. **Check console** for notification log

### Test with Your Twilio Number

During Twilio free trial, you can only send SMS to verified numbers:

1. In Twilio dashboard → Verified Caller IDs
2. Add your phone number
3. Update `vehicle_db.json` with your number
4. Test the system!

---

## API Response Format

When violations are detected, response includes:

```json
{
  "success": true,
  "violations": {
    "total_violations": 2,
    "violations": [...],
    "total_penalty_range": "₹2,000"
  },
  "sms_notifications": [
    {
      "success": true,
      "status": "sent",
      "license_plate": "DL-01-AB-1234",
      "owner": "Demo Driver 1",
      "message_sid": "SMxxxxxxxxxx"
    }
  ]
}
```

---

## Troubleshooting

### "SMS service in demo mode"
- This is normal! System works in demo mode by default
- To enable real SMS, set Twilio credentials

### "Vehicle not found in database"
- License plate extracted but not in `vehicle_db.json`
- Add vehicle to database or test with demo plates

### "SMS send failed"
- Check Twilio credentials
- Check phone number format (+country code)
- Check Twilio account balance

### License plate not detected
- Image quality might be poor
- Angle might be difficult
- Try image enhancement
- Use higher resolution images

---

## Cost Considerations

**Twilio Pricing (India):**
- Transactional SMS: ~₹0.50-₹1 per SMS
- Free trial: $15 credit
- Enough for ~500-1000 test messages

**Alternatives:**
- India-specific: MSG91, Kaleyra, Fast2SMS
- Just update `sms_service.py` with their API

---

## Production Deployment

For real deployment, consider:

1. **Real RTO Database Integration**
   - Connect to actual vehicle registration system
   - Requires official permissions

2. **SMS Provider**
   - Bulk SMS rates for government
   - Dedicated sender ID

3. **Security**
   - Store credentials securely (not in code)
   - Use environment variables or secrets manager

4. **Compliance**
   - Follow telecom regulations
   - Include opt-out mechanism
   - Privacy policy

---

## File Structure

```
backend/
├── app.py                    # Main API (SMS integrated)
├── sms_service.py            # Twilio SMS service
├── vehicle_db.py             # Vehicle registration database
├── notification_helper.py    # SMS notification logic
└── vehicle_db.json          # Demo vehicle data
```

---

## Testing Checklist

- [ ] System detects violations
- [ ] License plates extracted correctly
- [ ] Demo SMS logged to console
- [ ] Vehicle lookup works
- [ ] Real SMS sent (if Twilio configured)
- [ ] Message format looks good
- [ ] Phone number format correct

---

## Quick Start

**Test NOW (Demo Mode):**
```bash
cd backend
.\start.bat

# Upload image with demo plate: DL-01-AB-1234
# Check terminal for SMS notification log!
```

**Enable Real SMS:**
```bash
# Set Twilio credentials
$env:TWILIO_ACCOUNT_SID="ACxxxx"
$env:TWILIO_AUTH_TOKEN="your_token"
$env:TWILIO_PHONE_NUMBER="+1234567890"

# Install Twilio
pip install twilio

# Restart
.\start.bat
```

---

## Support

**Twilio Setup Issues:** https://www.twilio.com/docs/sms  
**India SMS Providers:** MSG91, Fast2SMS, Kaleyra  
**Free Testing:** Use Twilio free trial with verified numbers

---

**Your SMS notification system is READY!** 🎉

Test it in demo mode now, or configure Twilio for production use!
