# JARVIS Portable - পোর্টেবল JARVIS

## What is this? / এটা কি?

This is a portable version of JARVIS that can be copied to any Windows computer and run without installation.

এটি JARVIS এর একটি পোর্টেবল সংস্করণ যা যেকোনো Windows কম্পিউটারে কপি করে ইনস্টলেশন ছাড়াই চালানো যায়।

## How to Use / কিভাবে ব্যবহার করবেন

### English:
1. Copy the entire `JARVIS_Portable` folder to any Windows computer
2. Open the folder
3. Double-click `JARVIS.exe`
4. JARVIS will start automatically!

### বাংলা:
1. সম্পূর্ণ `JARVIS_Portable` ফোল্ডারটি যেকোনো Windows কম্পিউটারে কপি করুন
2. ফোল্ডারটি খুলুন
3. `JARVIS.exe` তে ডাবল ক্লিক করুন
4. JARVIS স্বয়ংক্রিয়ভাবে চালু হবে!

## Folder Structure / ফোল্ডার গঠন

```
JARVIS_Portable/
├── JARVIS.exe              (Main executable / মূল এক্সিকিউটেবল)
├── jarvis_memory.db        (Database / ডাটাবেস)
├── jarvis_config.txt       (Configuration / কনফিগারেশন)
├── core/                   (Core modules / মূল মডিউল)
│   ├── brain.py
│   ├── database.py
│   └── ...
└── engine/                 (Engine modules / ইঞ্জিন মডিউল)
    ├── voice.py
    └── ...
```

## Requirements / প্রয়োজনীয়তা

- Windows 7 or higher / Windows 7 বা তার উপরে
- No Python installation needed! / Python ইনস্টলেশন লাগবে না!
- No internet required for basic functions / মৌলিক কাজের জন্য ইন্টারনেট লাগবে না

## Features / বৈশিষ্ট্য

✅ Fully portable - no installation needed
✅ Works on any Windows computer
✅ Includes complete database with:
   - Windows 10 Pro information
   - Flipper Zero knowledge
   - Cyber attack encyclopedia
✅ All data stored locally
✅ Can be run from USB drive

✅ সম্পূর্ণ পোর্টেবল - ইনস্টলেশন লাগবে না
✅ যেকোনো Windows কম্পিউটারে কাজ করে
✅ সম্পূর্ণ ডাটাবেস অন্তর্ভুক্ত:
   - Windows 10 Pro তথ্য
   - Flipper Zero জ্ঞান
   - সাইবার আক্রমণ এনসাইক্লোপিডিয়া
✅ সব ডেটা স্থানীয়ভাবে সংরক্ষিত
✅ USB ড্রাইভ থেকে চালানো যায়

## Configuration / কনফিগারেশন

Edit `jarvis_config.txt` to add your API keys:

আপনার API কী যোগ করতে `jarvis_config.txt` সম্পাদনা করুন:

```
# Add your Google API keys here
AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## Troubleshooting / সমস্যা সমাধান

### English:
- **JARVIS won't start**: Make sure all files are in the same folder
- **Database error**: Delete `jarvis_memory.db` and restart (will create new database)
- **Missing modules**: Ensure `core` and `engine` folders are present

### বাংলা:
- **JARVIS চালু হচ্ছে না**: নিশ্চিত করুন সব ফাইল একই ফোল্ডারে আছে
- **ডাটাবেস ত্রুটি**: `jarvis_memory.db` মুছে দিন এবং পুনরায় চালু করুন (নতুন ডাটাবেস তৈরি হবে)
- **মডিউল নেই**: নিশ্চিত করুন `core` এবং `engine` ফোল্ডার আছে

## Support / সহায়তা

For help, check the documentation files:
- DATABASE_README.md
- CYBER_ATTACKS_REFERENCE.md
- FLIPPER_ZERO_REFERENCE.md

সাহায্যের জন্য, ডকুমেন্টেশন ফাইল দেখুন:
- DATABASE_README.md
- CYBER_ATTACKS_REFERENCE.md
- FLIPPER_ZERO_REFERENCE.md

## Version / সংস্করণ

JARVIS Portable v2.0
Created: May 4, 2026
