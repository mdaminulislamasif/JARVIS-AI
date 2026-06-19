# JARVIS Portable - Complete Guide
# পোর্টেবল JARVIS - সম্পূর্ণ গাইড

---

## 🎯 What is Portable JARVIS? / পোর্টেবল JARVIS কি?

### English:
Portable JARVIS is a standalone executable (.exe) version that:
- ✅ Can be copied to any Windows computer
- ✅ Runs without installation
- ✅ No Python required
- ✅ No dependencies needed
- ✅ Works from USB drive
- ✅ Includes complete database (100 entries)
- ✅ Ready to use immediately

### বাংলা:
পোর্টেবল JARVIS একটি স্বতন্ত্র এক্সিকিউটেবল (.exe) সংস্করণ যা:
- ✅ যেকোনো Windows কম্পিউটারে কপি করা যায়
- ✅ ইনস্টলেশন ছাড়াই চলে
- ✅ Python লাগে না
- ✅ কোনো ডিপেন্ডেন্সি লাগে না
- ✅ USB ড্রাইভ থেকে কাজ করে
- ✅ সম্পূর্ণ ডাটাবেস অন্তর্ভুক্ত (100 এন্ট্রি)
- ✅ তৎক্ষণাৎ ব্যবহারের জন্য প্রস্তুত

---

## 📦 How to Build / কিভাবে তৈরি করবেন

### Method 1: Automatic Build (Recommended) / স্বয়ংক্রিয় বিল্ড (প্রস্তাবিত)

#### English:
1. **Run the build script**:
   ```bash
   build_jarvis.bat
   ```

2. **Wait for completion** (2-5 minutes)

3. **Find your portable JARVIS**:
   - Location: `JARVIS_Portable` folder
   - Main file: `JARVIS.exe`

#### বাংলা:
1. **বিল্ড স্ক্রিপ্ট চালান**:
   ```bash
   build_jarvis.bat
   ```

2. **সম্পন্ন হওয়ার জন্য অপেক্ষা করুন** (2-5 মিনিট)

3. **আপনার পোর্টেবল JARVIS খুঁজুন**:
   - স্থান: `JARVIS_Portable` ফোল্ডার
   - মূল ফাইল: `JARVIS.exe`

---

### Method 2: Manual Build / ম্যানুয়াল বিল্ড

#### English:
```bash
# Step 1: Install PyInstaller
pip install pyinstaller

# Step 2: Build the executable
pyinstaller --clean --onefile --console jarvis_launcher.py --name JARVIS

# Step 3: Create portable folder
mkdir JARVIS_Portable
copy dist\JARVIS.exe JARVIS_Portable\
xcopy /E /I core JARVIS_Portable\core
xcopy /E /I engine JARVIS_Portable\engine
copy jarvis_memory.db.fixed-* JARVIS_Portable\jarvis_memory.db
copy jarvis_config.txt JARVIS_Portable\
```

#### বাংলা:
```bash
# ধাপ 1: PyInstaller ইনস্টল করুন
pip install pyinstaller

# ধাপ 2: এক্সিকিউটেবল তৈরি করুন
pyinstaller --clean --onefile --console jarvis_launcher.py --name JARVIS

# ধাপ 3: পোর্টেবল ফোল্ডার তৈরি করুন
mkdir JARVIS_Portable
copy dist\JARVIS.exe JARVIS_Portable\
xcopy /E /I core JARVIS_Portable\core
xcopy /E /I engine JARVIS_Portable\engine
copy jarvis_memory.db.fixed-* JARVIS_Portable\jarvis_memory.db
copy jarvis_config.txt JARVIS_Portable\
```

---

## 📁 Folder Structure / ফোল্ডার গঠন

```
JARVIS_Portable/
│
├── JARVIS.exe                  ← Main executable / মূল এক্সিকিউটেবল
├── jarvis_memory.db            ← Database (100 entries) / ডাটাবেস
├── jarvis_config.txt           ← Configuration / কনফিগারেশন
│
├── core/                       ← Core modules / মূল মডিউল
│   ├── brain.py
│   ├── database.py
│   ├── auth.py
│   ├── key_generator.py
│   └── login_window.py
│
├── engine/                     ← Engine modules / ইঞ্জিন মডিউল
│   ├── voice.py
│   ├── automation.py
│   ├── face3d.py
│   ├── generator.py
│   └── ...
│
└── Documentation/              ← Optional / ঐচ্ছিক
    ├── DATABASE_README.md
    ├── CYBER_ATTACKS_REFERENCE.md
    └── FLIPPER_ZERO_REFERENCE.md
```

---

## 🚀 How to Use / কিভাবে ব্যবহার করবেন

### On Original Computer / মূল কম্পিউটারে

#### English:
1. Build JARVIS.exe using `build_jarvis.bat`
2. Find `JARVIS_Portable` folder
3. Test by running `JARVIS.exe`

#### বাংলা:
1. `build_jarvis.bat` ব্যবহার করে JARVIS.exe তৈরি করুন
2. `JARVIS_Portable` ফোল্ডার খুঁজুন
3. `JARVIS.exe` চালিয়ে পরীক্ষা করুন

---

### On Fresh Computer / নতুন কম্পিউটারে

#### English:
1. **Copy the folder**:
   - Copy entire `JARVIS_Portable` folder to:
     - USB drive
     - External hard drive
     - Network location
     - Cloud storage (Google Drive, Dropbox, etc.)

2. **Transfer to new computer**:
   - Paste folder anywhere (Desktop, Documents, etc.)

3. **Run JARVIS**:
   - Open `JARVIS_Portable` folder
   - Double-click `JARVIS.exe`
   - JARVIS will start automatically!

4. **First run**:
   - JARVIS will check database
   - Create config if needed
   - Ready to use!

#### বাংলা:
1. **ফোল্ডার কপি করুন**:
   - সম্পূর্ণ `JARVIS_Portable` ফোল্ডার কপি করুন:
     - USB ড্রাইভে
     - এক্সটার্নাল হার্ড ড্রাইভে
     - নেটওয়ার্ক লোকেশনে
     - ক্লাউড স্টোরেজে (Google Drive, Dropbox, ইত্যাদি)

2. **নতুন কম্পিউটারে স্থানান্তর করুন**:
   - যেকোনো জায়গায় ফোল্ডার পেস্ট করুন (ডেস্কটপ, ডকুমেন্টস, ইত্যাদি)

3. **JARVIS চালান**:
   - `JARVIS_Portable` ফোল্ডার খুলুন
   - `JARVIS.exe` তে ডাবল ক্লিক করুন
   - JARVIS স্বয়ংক্রিয়ভাবে চালু হবে!

4. **প্রথম চালানো**:
   - JARVIS ডাটাবেস চেক করবে
   - প্রয়োজনে কনফিগ তৈরি করবে
   - ব্যবহারের জন্য প্রস্তুত!

---

## ⚙️ Configuration / কনফিগারেশন

### Edit jarvis_config.txt / jarvis_config.txt সম্পাদনা করুন

#### English:
```
# JARVIS Configuration
# Add your Google API keys here (one per line)

AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
AIzaSyYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
```

#### বাংলা:
```
# JARVIS কনফিগারেশন
# আপনার Google API কী এখানে যোগ করুন (প্রতি লাইনে একটি)

AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
AIzaSyYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
```

---

## 💾 Database / ডাটাবেস

### Included Data / অন্তর্ভুক্ত ডেটা

The portable version includes complete database with:

পোর্টেবল সংস্করণে সম্পূর্ণ ডাটাবেস অন্তর্ভুক্ত:

- ✅ **Windows 10 Pro** (26 entries)
  - System information
  - Commands & shortcuts
  - PowerShell basics

- ✅ **Flipper Zero** (28 entries)
  - Hardware specs
  - Radio capabilities
  - BadUSB & DuckyScript
  - Firmware options
  - Flipper Patcher

- ✅ **Cyber Attacks** (46 entries)
  - Network attacks
  - Web application attacks
  - Social engineering
  - Malware types
  - Password attacks
  - Wireless attacks
  - Defense strategies
  - Penetration testing
  - MITRE ATT&CK

**Total: 100 entries!**

---

## 🔧 Troubleshooting / সমস্যা সমাধান

### Problem: JARVIS won't start / সমস্যা: JARVIS চালু হচ্ছে না

#### English:
**Solution**:
1. Check if all files are present:
   - JARVIS.exe
   - core/ folder
   - engine/ folder
   - jarvis_memory.db
   - jarvis_config.txt

2. Run as Administrator (right-click → Run as administrator)

3. Check Windows Defender/Antivirus (may block unknown .exe)

#### বাংলা:
**সমাধান**:
1. চেক করুন সব ফাইল আছে কিনা:
   - JARVIS.exe
   - core/ ফোল্ডার
   - engine/ ফোল্ডার
   - jarvis_memory.db
   - jarvis_config.txt

2. অ্যাডমিনিস্ট্রেটর হিসেবে চালান (রাইট ক্লিক → Run as administrator)

3. Windows Defender/Antivirus চেক করুন (অজানা .exe ব্লক করতে পারে)

---

### Problem: Database error / সমস্যা: ডাটাবেস ত্রুটি

#### English:
**Solution**:
1. Delete `jarvis_memory.db`
2. Restart JARVIS.exe
3. New database will be created automatically

#### বাংলা:
**সমাধান**:
1. `jarvis_memory.db` মুছে দিন
2. JARVIS.exe পুনরায় চালু করুন
3. নতুন ডাটাবেস স্বয়ংক্রিয়ভাবে তৈরি হবে

---

### Problem: Missing modules / সমস্যা: মডিউল নেই

#### English:
**Solution**:
1. Ensure `core` and `engine` folders are in same directory as JARVIS.exe
2. Re-copy the entire JARVIS_Portable folder
3. Don't move files individually

#### বাংলা:
**সমাধান**:
1. নিশ্চিত করুন `core` এবং `engine` ফোল্ডার JARVIS.exe এর একই ডিরেক্টরিতে আছে
2. সম্পূর্ণ JARVIS_Portable ফোল্ডার পুনরায় কপি করুন
3. ফাইল আলাদাভাবে সরাবেন না

---

### Problem: Antivirus blocking / সমস্যা: অ্যান্টিভাইরাস ব্লক করছে

#### English:
**Solution**:
1. Add JARVIS.exe to antivirus exclusions
2. Or temporarily disable antivirus during first run
3. JARVIS is safe - it's your own compiled code!

#### বাংলা:
**সমাধান**:
1. JARVIS.exe কে অ্যান্টিভাইরাস এক্সক্লুশনে যোগ করুন
2. অথবা প্রথম চালানোর সময় সাময়িকভাবে অ্যান্টিভাইরাস বন্ধ করুন
3. JARVIS নিরাপদ - এটি আপনার নিজের কম্পাইল করা কোড!

---

## 📊 System Requirements / সিস্টেম প্রয়োজনীয়তা

### Minimum / ন্যূনতম:
- **OS**: Windows 7 or higher / Windows 7 বা তার উপরে
- **RAM**: 2 GB
- **Storage**: 100 MB free space / 100 MB খালি জায়গা
- **Processor**: Any modern CPU / যেকোনো আধুনিক CPU

### Recommended / প্রস্তাবিত:
- **OS**: Windows 10/11
- **RAM**: 4 GB or more / 4 GB বা তার বেশি
- **Storage**: 500 MB free space / 500 MB খালি জায়গা
- **Internet**: For AI features / AI ফিচারের জন্য

---

## 🎁 Advantages / সুবিধা

### English:
1. **No Installation**: Just copy and run
2. **Portable**: Works from USB drive
3. **Complete**: Includes all data and modules
4. **Independent**: No Python or dependencies needed
5. **Fast**: Starts in seconds
6. **Shareable**: Easy to share with others
7. **Safe**: No registry modifications
8. **Flexible**: Run from anywhere

### বাংলা:
1. **ইনস্টলেশন নেই**: শুধু কপি করে চালান
2. **পোর্টেবল**: USB ড্রাইভ থেকে কাজ করে
3. **সম্পূর্ণ**: সব ডেটা এবং মডিউল অন্তর্ভুক্ত
4. **স্বাধীন**: Python বা ডিপেন্ডেন্সি লাগে না
5. **দ্রুত**: সেকেন্ডে চালু হয়
6. **শেয়ারযোগ্য**: অন্যদের সাথে শেয়ার করা সহজ
7. **নিরাপদ**: কোনো রেজিস্ট্রি পরিবর্তন নেই
8. **নমনীয়**: যেকোনো জায়গা থেকে চালানো যায়

---

## 📝 Usage Examples / ব্যবহারের উদাহরণ

### Scenario 1: USB Drive / USB ড্রাইভ

#### English:
1. Copy JARVIS_Portable to USB drive
2. Plug USB into any computer
3. Run JARVIS.exe from USB
4. All data stays on USB

#### বাংলা:
1. JARVIS_Portable USB ড্রাইভে কপি করুন
2. যেকোনো কম্পিউটারে USB প্লাগ করুন
3. USB থেকে JARVIS.exe চালান
4. সব ডেটা USB তে থাকবে

---

### Scenario 2: Multiple Computers / একাধিক কম্পিউটার

#### English:
1. Copy JARVIS_Portable to cloud storage (Google Drive)
2. Download on any computer
3. Run JARVIS.exe
4. Sync changes back to cloud

#### বাংলা:
1. JARVIS_Portable ক্লাউড স্টোরেজে কপি করুন (Google Drive)
2. যেকোনো কম্পিউটারে ডাউনলোড করুন
3. JARVIS.exe চালান
4. পরিবর্তন ক্লাউডে সিঙ্ক করুন

---

### Scenario 3: Offline Use / অফলাইন ব্যবহার

#### English:
1. Copy JARVIS_Portable to computer
2. No internet needed for:
   - Database queries
   - Local file operations
   - System information
3. Internet only needed for AI features

#### বাংলা:
1. JARVIS_Portable কম্পিউটারে কপি করুন
2. ইন্টারনেট লাগবে না:
   - ডাটাবেস কোয়েরি
   - লোকাল ফাইল অপারেশন
   - সিস্টেম তথ্য
3. শুধু AI ফিচারের জন্য ইন্টারনেট লাগবে

---

## 🔒 Security / নিরাপত্তা

### English:
- ✅ No data sent to external servers (except AI API)
- ✅ All data stored locally
- ✅ No telemetry or tracking
- ✅ Open source code
- ✅ You control everything

### বাংলা:
- ✅ কোনো ডেটা বাহ্যিক সার্ভারে পাঠানো হয় না (AI API ছাড়া)
- ✅ সব ডেটা স্থানীয়ভাবে সংরক্ষিত
- ✅ কোনো টেলিমেট্রি বা ট্র্যাকিং নেই
- ✅ ওপেন সোর্স কোড
- ✅ আপনি সবকিছু নিয়ন্ত্রণ করেন

---

## 📦 File Size / ফাইল সাইজ

- **JARVIS.exe**: ~30-50 MB
- **Database**: ~1 MB
- **Core modules**: ~5 MB
- **Engine modules**: ~10 MB
- **Total**: ~50-70 MB

---

## 🆘 Support / সহায়তা

### English:
For help:
1. Read documentation files
2. Check troubleshooting section
3. Review error messages
4. Test on original computer first

### বাংলা:
সাহায্যের জন্য:
1. ডকুমেন্টেশন ফাইল পড়ুন
2. সমস্যা সমাধান বিভাগ দেখুন
3. ত্রুটি বার্তা পর্যালোচনা করুন
4. প্রথমে মূল কম্পিউটারে পরীক্ষা করুন

---

## ✅ Checklist / চেকলিস্ট

### Before Copying / কপি করার আগে:
- [ ] JARVIS.exe built successfully
- [ ] All files in JARVIS_Portable folder
- [ ] Database file present
- [ ] Config file present
- [ ] Tested on original computer

### After Copying / কপি করার পরে:
- [ ] All files copied
- [ ] Folder structure intact
- [ ] JARVIS.exe runs
- [ ] Database accessible
- [ ] No error messages

---

## 🎉 Success! / সফল!

### English:
You now have a fully portable JARVIS that:
- Works on any Windows computer
- Requires no installation
- Includes complete database
- Can be shared easily
- Runs from USB drive

**Enjoy your portable AI assistant!**

### বাংলা:
আপনার এখন একটি সম্পূর্ণ পোর্টেবল JARVIS আছে যা:
- যেকোনো Windows কম্পিউটারে কাজ করে
- কোনো ইনস্টলেশন লাগে না
- সম্পূর্ণ ডাটাবেস অন্তর্ভুক্ত
- সহজে শেয়ার করা যায়
- USB ড্রাইভ থেকে চলে

**আপনার পোর্টেবল AI সহায়ক উপভোগ করুন!**

---

**Version**: 2.0 Portable  
**Created**: May 4, 2026  
**Status**: ✅ Ready to Use / ব্যবহারের জন্য প্রস্তুত
