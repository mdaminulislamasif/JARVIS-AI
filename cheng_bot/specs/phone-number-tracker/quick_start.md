# Phone Number Tracker - Quick Start Guide

## ⚠️ Legal Notice

**USE RESPONSIBLY AND LEGALLY**
- Only track your own phone or with explicit permission
- Respect privacy laws
- Do not use for illegal purposes

## Quick Implementation

### Option 1: Simple Python Script (5 minutes)

```python
# phone_tracker.py
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests

class PhoneTracker:
    def __init__(self):
        self.truecaller_api = "YOUR_API_KEY"  # Get from truecaller.com
        self.numverify_api = "YOUR_API_KEY"   # Get from numverify.com
    
    def track_number(self, phone_number):
        """Track a phone number"""
        try:
            # Parse phone number
            parsed = phonenumbers.parse(phone_number)
            
            # Get basic info
            info = {
                'number': phone_number,
                'valid': phonenumbers.is_valid_number(parsed),
                'country': geocoder.description_for_number(parsed, 'en'),
                'carrier': carrier.name_for_number(parsed, 'en'),
                'timezone': timezone.time_zones_for_number(parsed),
                'number_type': self.get_number_type(parsed),
                'location': self.get_location(parsed),
                'additional_info': self.get_osint_info(phone_number)
            }
            
            return info
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_number_type(self, parsed):
        """Get number type"""
        number_type = phonenumbers.number_type(parsed)
        types = {
            0: 'Fixed Line',
            1: 'Mobile',
            2: 'Fixed Line or Mobile',
            3: 'Toll Free',
            4: 'Premium Rate',
            5: 'Shared Cost',
            6: 'VoIP',
            7: 'Personal Number',
            8: 'Pager',
            9: 'UAN',
            10: 'Voicemail',
            99: 'Unknown'
        }
        return types.get(number_type, 'Unknown')
    
    def get_location(self, parsed):
        """Get approximate location"""
        country = geocoder.description_for_number(parsed, 'en')
        region = geocoder.description_for_number(parsed, 'en')
        
        return {
            'country': country,
            'region': region,
            'coordinates': self.get_coordinates(country)
        }
    
    def get_coordinates(self, location):
        """Get coordinates for location"""
        # Use geocoding API
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
            response = requests.get(url, headers={'User-Agent': 'PhoneTracker/1.0'})
            data = response.json()
            if data:
                return {
                    'lat': data[0]['lat'],
                    'lon': data[0]['lon']
                }
        except:
            pass
        return None
    
    def get_osint_info(self, phone_number):
        """Get OSINT information"""
        info = {}
        
        # Try Numverify API
        try:
            url = f"http://apilayer.net/api/validate?access_key={self.numverify_api}&number={phone_number}"
            response = requests.get(url)
            data = response.json()
            if data.get('valid'):
                info['numverify'] = {
                    'carrier': data.get('carrier'),
                    'line_type': data.get('line_type'),
                    'location': data.get('location')
                }
        except:
            pass
        
        return info
    
    def track_realtime(self, phone_number, duration=60):
        """Track phone in real-time"""
        import time
        
        print(f"🔍 Tracking {phone_number} for {duration} seconds...")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            info = self.track_number(phone_number)
            print(f"\n📍 Location Update:")
            print(f"   Country: {info.get('country')}")
            print(f"   Carrier: {info.get('carrier')}")
            print(f"   Type: {info.get('number_type')}")
            
            time.sleep(10)  # Update every 10 seconds

# Usage
if __name__ == "__main__":
    tracker = PhoneTracker()
    
    # Example: Track Bangladesh number
    phone = "+8801712345678"  # Replace with actual number
    
    print("🔍 Phone Number Tracker")
    print("=" * 50)
    
    result = tracker.track_number(phone)
    
    print(f"\n📱 Number: {result['number']}")
    print(f"✅ Valid: {result['valid']}")
    print(f"🌍 Country: {result['country']}")
    print(f"📡 Carrier: {result['carrier']}")
    print(f"📞 Type: {result['number_type']}")
    print(f"🕐 Timezone: {result['timezone']}")
    
    if result.get('location'):
        loc = result['location']
        print(f"\n📍 Location:")
        print(f"   Country: {loc['country']}")
        print(f"   Region: {loc['region']}")
        if loc.get('coordinates'):
            print(f"   Coordinates: {loc['coordinates']['lat']}, {loc['coordinates']['lon']}")
```

### Installation

```bash
# Install required packages
pip install phonenumbers
pip install requests
pip install geopy

# Run tracker
python phone_tracker.py
```

## Option 2: JARVIS Integration

Add to your JARVIS:

```python
# In your JARVIS code
from phone_tracker import PhoneTracker

class JARVIS:
    def __init__(self):
        self.phone_tracker = PhoneTracker()
    
    def process_command(self, command):
        # Track phone number
        if "track phone" in command.lower() or "phone track" in command.lower():
            # Extract phone number from command
            phone = self.extract_phone_number(command)
            if phone:
                result = self.phone_tracker.track_number(phone)
                return self.format_tracking_result(result)
            else:
                return "Please provide a phone number to track"
    
    def extract_phone_number(self, text):
        """Extract phone number from text"""
        import re
        # Bangladesh format
        pattern = r'\+?880\d{10}|\d{11}'
        match = re.search(pattern, text)
        if match:
            number = match.group()
            if not number.startswith('+'):
                number = '+880' + number[-10:]
            return number
        return None
    
    def format_tracking_result(self, result):
        """Format result for display"""
        if result.get('error'):
            return f"Error: {result['error']}"
        
        response = f"""
📱 Phone Tracking Result:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Number:    {result['number']}
Valid:     {'✅ Yes' if result['valid'] else '❌ No'}
Country:   {result['country']}
Carrier:   {result['carrier']}
Type:      {result['number_type']}
Timezone:  {', '.join(result['timezone'])}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return response
```

## Option 3: Web Interface

Create a simple web interface:

```html
<!-- phone_tracker.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Phone Number Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f0f0f0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        input {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 5px;
            margin: 10px 0;
        }
        button {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
        #result {
            margin-top: 20px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 5px;
            display: none;
        }
        .info-row {
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .label {
            font-weight: bold;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 Phone Number Tracker</h1>
        <p style="text-align: center; color: #666;">Track phone numbers worldwide</p>
        
        <input type="text" id="phoneInput" placeholder="Enter phone number (e.g., +8801712345678)">
        <button onclick="trackPhone()">🔍 Track Number</button>
        
        <div id="result"></div>
    </div>

    <script>
        async function trackPhone() {
            const phone = document.getElementById('phoneInput').value;
            const resultDiv = document.getElementById('result');
            
            if (!phone) {
                alert('Please enter a phone number');
                return;
            }
            
            resultDiv.innerHTML = '<p>🔍 Tracking...</p>';
            resultDiv.style.display = 'block';
            
            try {
                // Call your backend API
                const response = await fetch('/api/track', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({phone: phone})
                });
                
                const data = await response.json();
                
                resultDiv.innerHTML = `
                    <h3>📍 Tracking Result</h3>
                    <div class="info-row">
                        <span class="label">Number:</span> ${data.number}
                    </div>
                    <div class="info-row">
                        <span class="label">Valid:</span> ${data.valid ? '✅ Yes' : '❌ No'}
                    </div>
                    <div class="info-row">
                        <span class="label">Country:</span> ${data.country}
                    </div>
                    <div class="info-row">
                        <span class="label">Carrier:</span> ${data.carrier}
                    </div>
                    <div class="info-row">
                        <span class="label">Type:</span> ${data.number_type}
                    </div>
                    <div class="info-row">
                        <span class="label">Timezone:</span> ${data.timezone.join(', ')}
                    </div>
                `;
            } catch (error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
```

## Bangladesh Carriers

```python
BANGLADESH_CARRIERS = {
    '017': 'Grameenphone',
    '013': 'Grameenphone',
    '018': 'Robi',
    '019': 'Banglalink',
    '014': 'Banglalink',
    '015': 'Teletalk',
    '016': 'Airtel'
}

def get_bangladesh_carrier(phone):
    """Get Bangladesh carrier from phone number"""
    # Remove country code
    number = phone.replace('+880', '').replace('880', '')
    prefix = number[:3]
    return BANGLADESH_CARRIERS.get(prefix, 'Unknown')
```

## API Keys Needed

1. **Truecaller API** - https://www.truecaller.com/
2. **Numverify API** - https://numverify.com/
3. **OpenCellID** - https://opencellid.org/
4. **Google Maps API** - https://developers.google.com/maps

## Usage Examples

```python
# Track single number
tracker.track_number("+8801712345678")

# Track multiple numbers
numbers = ["+8801712345678", "+8801812345678", "+8801912345678"]
for number in numbers:
    result = tracker.track_number(number)
    print(result)

# Real-time tracking
tracker.track_realtime("+8801712345678", duration=300)  # Track for 5 minutes

# Get carrier only
carrier = tracker.get_bangladesh_carrier("01712345678")
print(f"Carrier: {carrier}")
```

## Next Steps

1. **Get API Keys** - Sign up for tracking APIs
2. **Test Script** - Run the Python script
3. **Integrate with JARVIS** - Add to your JARVIS system
4. **Create Web Interface** - Deploy web version
5. **Add to Master Plan** - Include in master implementation

## Legal Compliance

Always:
- ✅ Get consent before tracking
- ✅ Use for legal purposes only
- ✅ Respect privacy laws
- ✅ Log all tracking activities
- ✅ Provide opt-out options

Never:
- ❌ Track without permission
- ❌ Use for stalking/harassment
- ❌ Violate privacy laws
- ❌ Share tracking data unauthorized

**🔍 Phone Number Tracker এখন ready! 🔍**
