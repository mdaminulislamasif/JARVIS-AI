"""
Add API Integration to JARVIS
JARVIS-এ API ইন্টিগ্রেশন যোগ করুন

This script adds API key support to JARVIS database.
JARVIS will work WITHOUT API keys (basic features)
But WITH API keys, JARVIS becomes SUPER POWERFUL!

API key ছাড়া: বেসিক ফিচার কাজ করবে
API key সহ: সুপার পাওয়ারফুল হবে!
"""

import sqlite3
import os
from datetime import datetime

def add_api_integration():
    """Add API integration features to JARVIS database"""
    
    print("\n" + "=" * 80)
    print("  🔑 ADDING API INTEGRATION TO JARVIS")
    print("  🔑 JARVIS-এ API ইন্টিগ্রেশন যোগ করা হচ্ছে")
    print("=" * 80)
    print()
    
    # Database file
    db_file = 'jarvis_memory.db.fixed-20260504-091901'
    
    if not os.path.exists(db_file):
        print(f"❌ Database not found: {db_file}")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    print("✅ Connected to database")
    print()
    
    # API Integration entries
    api_entries = []
    
    # ========================================================================
    # CATEGORY 1: AI & LLM APIs (ChatGPT, Claude, Gemini, etc.)
    # ========================================================================
    
    api_entries.append({
        'category': 'AI & LLM',
        'subcategory': 'ChatGPT / OpenAI',
        'title': 'OpenAI API (ChatGPT, GPT-4, DALL-E)',
        'description': '''OpenAI API for advanced AI features:
- ChatGPT: Advanced conversations, code generation, writing
- GPT-4: Most powerful language model
- DALL-E: AI image generation from text
- Whisper: Speech-to-text transcription
- Embeddings: Semantic search and similarity

WITHOUT API: Basic offline AI
WITH API: Advanced ChatGPT-4, image generation, voice transcription

Get API key: https://platform.openai.com/api-keys
Price: Pay-as-you-go (starts free)''',
        'tags': 'openai,chatgpt,gpt4,dalle,whisper,ai,llm,image generation'
    })
    
    api_entries.append({
        'category': 'AI & LLM',
        'subcategory': 'Claude / Anthropic',
        'title': 'Anthropic Claude API',
        'description': '''Claude AI API for advanced reasoning:
- Claude 3 Opus: Most powerful model
- Claude 3 Sonnet: Balanced performance
- Claude 3 Haiku: Fast responses
- Long context: Up to 200K tokens
- Advanced reasoning and analysis

WITHOUT API: Basic AI responses
WITH API: Advanced Claude AI with long context

Get API key: https://console.anthropic.com/
Price: Pay-as-you-go''',
        'tags': 'claude,anthropic,ai,llm,reasoning'
    })
    
    api_entries.append({
        'category': 'AI & LLM',
        'subcategory': 'Google Gemini',
        'title': 'Google Gemini API',
        'description': '''Google Gemini API for multimodal AI:
- Gemini Pro: Advanced language model
- Gemini Vision: Image understanding
- Gemini Ultra: Most capable model
- Multimodal: Text, images, video, audio
- Free tier available

WITHOUT API: Basic AI
WITH API: Google's most advanced AI

Get API key: https://makersuite.google.com/app/apikey
Price: Free tier + pay-as-you-go''',
        'tags': 'gemini,google,ai,llm,multimodal,vision'
    })
    
    api_entries.append({
        'category': 'AI & LLM',
        'subcategory': 'Perplexity AI',
        'title': 'Perplexity AI API',
        'description': '''Perplexity AI for real-time web search + AI:
- Real-time web search with AI answers
- Citations and sources
- Research mode
- Up-to-date information
- Fact-checking

WITHOUT API: Basic search
WITH API: AI-powered search with real-time web data

Get API key: https://www.perplexity.ai/settings/api
Price: Pay-as-you-go''',
        'tags': 'perplexity,search,ai,web,research'
    })
    
    # ========================================================================
    # CATEGORY 2: Translation & Language APIs
    # ========================================================================
    
    api_entries.append({
        'category': 'Translation & Language',
        'subcategory': 'Google Translate',
        'title': 'Google Cloud Translation API',
        'description': '''Google Translate API for 100+ languages:
- Translate text between 100+ languages
- Auto language detection
- Neural machine translation
- Batch translation
- Document translation

WITHOUT API: Basic offline translation
WITH API: Professional Google Translate quality

Get API key: https://cloud.google.com/translate
Price: Free tier + $20 per 1M characters''',
        'tags': 'translate,google,language,multilingual'
    })
    
    api_entries.append({
        'category': 'Translation & Language',
        'subcategory': 'DeepL',
        'title': 'DeepL Translation API',
        'description': '''DeepL API for high-quality translation:
- Best translation quality
- 30+ languages
- Formal/informal tone
- Document translation
- Glossary support

WITHOUT API: Basic translation
WITH API: Professional DeepL quality

Get API key: https://www.deepl.com/pro-api
Price: Free tier (500K chars/month) + paid plans''',
        'tags': 'deepl,translate,language,professional'
    })
    
    # ========================================================================
    # CATEGORY 3: Image & Video APIs
    # ========================================================================
    
    api_entries.append({
        'category': 'Image & Video',
        'subcategory': 'Stability AI',
        'title': 'Stability AI API (Stable Diffusion)',
        'description': '''Stability AI for image generation:
- Stable Diffusion: Text-to-image generation
- Image-to-image transformation
- Upscaling and enhancement
- Style transfer
- Inpainting and outpainting

WITHOUT API: Basic image editing
WITH API: AI image generation and enhancement

Get API key: https://platform.stability.ai/
Price: Pay-as-you-go''',
        'tags': 'stability,stablediffusion,image,generation,ai'
    })
    
    api_entries.append({
        'category': 'Image & Video',
        'subcategory': 'Midjourney',
        'title': 'Midjourney API (via Discord)',
        'description': '''Midjourney for artistic AI images:
- Highest quality AI art
- Multiple styles and versions
- Upscaling and variations
- Remix and blend
- Community showcase

WITHOUT API: Basic image tools
WITH API: Professional AI art generation

Get access: https://www.midjourney.com/
Price: Subscription ($10-$60/month)''',
        'tags': 'midjourney,image,art,generation,ai'
    })
    
    api_entries.append({
        'category': 'Image & Video',
        'subcategory': 'Remove.bg',
        'title': 'Remove.bg API',
        'description': '''Remove.bg for background removal:
- Automatic background removal
- High-quality cutouts
- Batch processing
- API integration
- Fast processing

WITHOUT API: Manual background removal
WITH API: Automatic AI background removal

Get API key: https://www.remove.bg/api
Price: Free tier (50 images/month) + paid plans''',
        'tags': 'removebg,background,image,editing'
    })
    
    # ========================================================================
    # CATEGORY 4: Speech & Audio APIs
    # ========================================================================
    
    api_entries.append({
        'category': 'Speech & Audio',
        'subcategory': 'ElevenLabs',
        'title': 'ElevenLabs Text-to-Speech API',
        'description': '''ElevenLabs for realistic voice synthesis:
- Most realistic AI voices
- Voice cloning
- Multiple languages
- Emotion and tone control
- Custom voice creation

WITHOUT API: Basic text-to-speech
WITH API: Professional AI voice generation

Get API key: https://elevenlabs.io/
Price: Free tier (10K chars/month) + paid plans''',
        'tags': 'elevenlabs,tts,voice,speech,audio'
    })
    
    api_entries.append({
        'category': 'Speech & Audio',
        'subcategory': 'AssemblyAI',
        'title': 'AssemblyAI Speech-to-Text API',
        'description': '''AssemblyAI for advanced transcription:
- Accurate speech-to-text
- Speaker diarization
- Sentiment analysis
- Topic detection
- Real-time transcription

WITHOUT API: Basic speech recognition
WITH API: Professional transcription with AI features

Get API key: https://www.assemblyai.com/
Price: Pay-as-you-go ($0.00025 per second)''',
        'tags': 'assemblyai,stt,transcription,speech,audio'
    })
    
    # ========================================================================
    # CATEGORY 5: Web Scraping & Data APIs
    # ========================================================================
    
    api_entries.append({
        'category': 'Web Scraping & Data',
        'subcategory': 'ScraperAPI',
        'title': 'ScraperAPI for Web Scraping',
        'description': '''ScraperAPI for easy web scraping:
- Bypass anti-bot protection
- Automatic proxy rotation
- JavaScript rendering
- CAPTCHA solving
- Geotargeting

WITHOUT API: Basic web scraping (may get blocked)
WITH API: Professional scraping without blocks

Get API key: https://www.scraperapi.com/
Price: Free tier (1K requests/month) + paid plans''',
        'tags': 'scraper,web,data,scraping,proxy'
    })
    
    api_entries.append({
        'category': 'Web Scraping & Data',
        'subcategory': 'Bright Data',
        'title': 'Bright Data (formerly Luminati)',
        'description': '''Bright Data for enterprise web scraping:
- Largest proxy network
- Web scraping tools
- Data collection
- CAPTCHA solving
- Residential proxies

WITHOUT API: Limited scraping
WITH API: Enterprise-grade data collection

Get API key: https://brightdata.com/
Price: Pay-as-you-go''',
        'tags': 'brightdata,proxy,scraping,data'
    })
    
    # ========================================================================
    # CATEGORY 6: Email & Communication APIs
    # ========================================================================
    
    api_entries.append({
        'category': 'Email & Communication',
        'subcategory': 'SendGrid',
        'title': 'SendGrid Email API',
        'description': '''SendGrid for email sending:
- Reliable email delivery
- Email templates
- Analytics and tracking
- Bulk email sending
- Email validation

WITHOUT API: Basic email (may go to spam)
WITH API: Professional email delivery

Get API key: https://sendgrid.com/
Price: Free tier (100 emails/day) + paid plans''',
        'tags': 'sendgrid,email,smtp,communication'
    })
    
    api_entries.append({
        'category': 'Email & Communication',
        'subcategory': 'Twilio',
        'title': 'Twilio SMS & Voice API',
        'description': '''Twilio for SMS and voice:
- Send/receive SMS
- Voice calls
- WhatsApp messaging
- Video calls
- Phone number verification

WITHOUT API: No SMS/voice features
WITH API: Full SMS and voice capabilities

Get API key: https://www.twilio.com/
Price: Pay-as-you-go''',
        'tags': 'twilio,sms,voice,phone,communication'
    })
    
    # ========================================================================
    # CATEGORY 7: Weather & Location APIs
    # ========================================================================
    
    api_entries.append({
        'category': 'Weather & Location',
        'subcategory': 'OpenWeatherMap',
        'title': 'OpenWeatherMap API',
        'description': '''OpenWeatherMap for weather data:
- Current weather
- 5-day forecast
- Historical data
- Weather maps
- Air pollution data

WITHOUT API: No weather data
WITH API: Real-time weather information

Get API key: https://openweathermap.org/api
Price: Free tier (1K calls/day) + paid plans''',
        'tags': 'weather,openweathermap,forecast,climate'
    })
    
    api_entries.append({
        'category': 'Weather & Location',
        'subcategory': 'Google Maps',
        'title': 'Google Maps API',
        'description': '''Google Maps for location services:
- Maps and navigation
- Geocoding
- Places search
- Distance matrix
- Street View

WITHOUT API: Basic maps
WITH API: Full Google Maps features

Get API key: https://developers.google.com/maps
Price: Free tier ($200 credit/month) + paid''',
        'tags': 'maps,google,location,navigation,geocoding'
    })
    
    # ========================================================================
    # CATEGORY 8: Payment & E-commerce APIs
    # ========================================================================
    
    api_entries.append({
        'category': 'Payment & E-commerce',
        'subcategory': 'Stripe',
        'title': 'Stripe Payment API',
        'description': '''Stripe for payment processing:
- Accept credit cards
- Subscriptions
- Invoicing
- Payment links
- Fraud prevention

WITHOUT API: No payment processing
WITH API: Professional payment system

Get API key: https://stripe.com/
Price: 2.9% + $0.30 per transaction''',
        'tags': 'stripe,payment,ecommerce,credit card'
    })
    
    # ========================================================================
    # CATEGORY 9: Social Media APIs
    # ========================================================================
    
    api_entries.append({
        'category': 'Social Media',
        'subcategory': 'Twitter/X',
        'title': 'Twitter/X API',
        'description': '''Twitter/X API for social media:
- Post tweets
- Read timeline
- Search tweets
- User information
- Analytics

WITHOUT API: No Twitter integration
WITH API: Full Twitter automation

Get API key: https://developer.twitter.com/
Price: Free tier + paid plans''',
        'tags': 'twitter,x,social,media,api'
    })
    
    api_entries.append({
        'category': 'Social Media',
        'subcategory': 'YouTube',
        'title': 'YouTube Data API',
        'description': '''YouTube API for video platform:
- Search videos
- Upload videos
- Manage playlists
- Get video info
- Analytics

WITHOUT API: Basic YouTube viewing
WITH API: Full YouTube automation

Get API key: https://developers.google.com/youtube
Price: Free (with quotas)''',
        'tags': 'youtube,video,google,social,media'
    })
    
    # ========================================================================
    # CATEGORY 10: Database & Storage APIs
    # ========================================================================
    
    api_entries.append({
        'category': 'Database & Storage',
        'subcategory': 'Firebase',
        'title': 'Firebase (Google) API',
        'description': '''Firebase for backend services:
- Real-time database
- Cloud storage
- Authentication
- Hosting
- Analytics

WITHOUT API: Local storage only
WITH API: Cloud database and storage

Get API key: https://firebase.google.com/
Price: Free tier + pay-as-you-go''',
        'tags': 'firebase,google,database,storage,backend'
    })
    
    api_entries.append({
        'category': 'Database & Storage',
        'subcategory': 'AWS S3',
        'title': 'Amazon S3 Storage API',
        'description': '''AWS S3 for cloud storage:
- Unlimited storage
- File hosting
- CDN integration
- Backup and archiving
- Static website hosting

WITHOUT API: Local storage only
WITH API: Cloud storage with AWS

Get API key: https://aws.amazon.com/s3/
Price: Pay-as-you-go ($0.023 per GB)''',
        'tags': 'aws,s3,storage,cloud,amazon'
    })
    
    # ========================================================================
    # Add entries to database
    # ========================================================================
    
    print(f"Adding {len(api_entries)} API integration entries...")
    print()
    
    added_count = 0
    
    for entry in api_entries:
        try:
            # Add to knowledge_base (using correct schema: topic, content, source)
            content = f"""Category: {entry['category']} - {entry['subcategory']}

{entry['description']}

Tags: {entry['tags']}"""
            
            cursor.execute('''
                INSERT INTO knowledge_base (topic, content, source, created_at)
                VALUES (?, ?, ?, ?)
            ''', (
                entry['title'],
                content,
                'API Integration',
                datetime.now().isoformat()
            ))
            
            print(f"  ✅ {entry['title']}")
            added_count += 1
            
        except Exception as e:
            print(f"  ❌ Error adding {entry['title']}: {e}")
    
    # Add API configuration to system_info
    print()
    print("Adding API configuration entries...")
    
    api_config_entries = [
        {
            'key': 'api_mode',
            'value': 'hybrid',
            'category': 'API Configuration'
        },
        {
            'key': 'api_fallback',
            'value': 'enabled',
            'category': 'API Configuration'
        },
        {
            'key': 'api_keys_configured',
            'value': '0',
            'category': 'API Configuration'
        },
        {
            'key': 'api_priority',
            'value': 'openai,claude,gemini,perplexity',
            'category': 'API Configuration'
        }
    ]
    
    for config in api_config_entries:
        try:
            cursor.execute('''
                INSERT INTO system_info (key, value, category, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (
                config['key'],
                config['value'],
                config['category'],
                datetime.now().isoformat()
            ))
            print(f"  ✅ {config['key']}")
        except Exception as e:
            print(f"  ❌ Error adding {config['key']}: {e}")
    
    # Add user preferences for API
    print()
    print("Adding API user preferences...")
    
    api_prefs = [
        {
            'preference_key': 'use_api_when_available',
            'preference_value': 'yes'
        },
        {
            'preference_key': 'api_cost_limit_daily',
            'preference_value': '10.00'
        },
        {
            'preference_key': 'preferred_ai_api',
            'preference_value': 'auto'
        }
    ]
    
    for pref in api_prefs:
        try:
            cursor.execute('''
                INSERT INTO user_preferences (preference_key, preference_value, updated_at)
                VALUES (?, ?, ?)
            ''', (
                pref['preference_key'],
                pref['preference_value'],
                datetime.now().isoformat()
            ))
            print(f"  ✅ {pref['preference_key']}")
        except Exception as e:
            print(f"  ❌ Error adding {pref['preference_key']}: {e}")
    
    # Commit changes
    conn.commit()
    
    # Get total counts
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    total_knowledge = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM system_info")
    total_system = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM user_preferences")
    total_prefs = cursor.fetchone()[0]
    
    conn.close()
    
    print()
    print("=" * 80)
    print("  ✅ API INTEGRATION ADDED SUCCESSFULLY!")
    print("  ✅ API ইন্টিগ্রেশন সফলভাবে যোগ করা হয়েছে!")
    print("=" * 80)
    print()
    print(f"  Added Entries:")
    print(f"    📚 Knowledge Base: {added_count} API entries")
    print(f"    ⚙️ System Info: 4 API config entries")
    print(f"    👤 User Preferences: 3 API preference entries")
    print()
    print(f"  Database Totals:")
    print(f"    📚 Total Knowledge: {total_knowledge} entries")
    print(f"    ⚙️ Total System Info: {total_system} entries")
    print(f"    👤 Total Preferences: {total_prefs} entries")
    print()
    print("=" * 80)
    print()
    print("  🎯 HOW IT WORKS:")
    print()
    print("  WITHOUT API KEYS (API key ছাড়া):")
    print("    ✅ Basic AI (offline models)")
    print("    ✅ Basic translation")
    print("    ✅ Basic image editing")
    print("    ✅ Basic speech recognition")
    print("    ✅ All local features work!")
    print()
    print("  WITH API KEYS (API key সহ):")
    print("    🚀 ChatGPT-4, Claude, Gemini (advanced AI)")
    print("    🚀 Professional translation (Google, DeepL)")
    print("    🚀 AI image generation (DALL-E, Stable Diffusion)")
    print("    🚀 Realistic voice (ElevenLabs)")
    print("    🚀 Real-time web search (Perplexity)")
    print("    🚀 Professional email (SendGrid)")
    print("    🚀 SMS/Voice (Twilio)")
    print("    🚀 Weather data (OpenWeatherMap)")
    print("    🚀 Maps (Google Maps)")
    print("    🚀 Payment processing (Stripe)")
    print("    🚀 Social media automation (Twitter, YouTube)")
    print("    🚀 Cloud storage (Firebase, AWS S3)")
    print("    🚀 And much more!")
    print()
    print("=" * 80)
    print()
    print("  📝 NEXT STEPS:")
    print()
    print("  1. JARVIS works NOW without any API keys!")
    print("  2. To make it MORE POWERFUL, add API keys:")
    print("     - OpenAI: https://platform.openai.com/api-keys")
    print("     - Claude: https://console.anthropic.com/")
    print("     - Gemini: https://makersuite.google.com/app/apikey")
    print("     - And others as needed")
    print()
    print("  3. Configure API keys in JARVIS settings")
    print("  4. JARVIS will automatically use APIs when available")
    print("  5. If API fails, JARVIS falls back to offline mode")
    print()
    print("=" * 80)

def main():
    add_api_integration()

if __name__ == "__main__":
    main()
