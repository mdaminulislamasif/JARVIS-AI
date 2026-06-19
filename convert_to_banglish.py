"""
Convert all Unicode Bengali to Banglish in JARVIS files
সব Unicode Bengali কে Banglish এ convert করে
"""

import re
import os

# Bengali to Banglish mapping
bengali_to_banglish = {
    # Common words
    'চূড়ান্ত বুদ্ধিমত্তা': 'Churanto Buddhimotta',
    'চালু হয়েছে': 'chalu hoyeche',
    'কেমন আছো': 'kemon acho',
    'কেমন আছেন': 'kemon achen',
    'ভালো আছো': 'valo acho',
    'ভালো আছেন': 'valo achen',
    'হ্যালো': 'hello',
    'হাই': 'hi',
    'নমস্কার': 'nomoshkar',
    'সালাম': 'salam',
    'সুপ্রভাত': 'suprobhat',
    'শুভ অপরাহ্ন': 'shubho oporahno',
    'শুভ সন্ধ্যা': 'shubho shondha',
    'শুভ রাত্রি': 'shubho ratri',
    'ধন্যবাদ': 'dhonnobad',
    'শুক্রিয়া': 'shukriya',
    'ভালো': 'valo',
    'দারুণ': 'darun',
    'অসাধারণ': 'oshadharon',
    'দুঃখিত': 'dukhito',
    'খুশি': 'khushi',
    'রাগ': 'rag',
    'চিন্তা': 'chinta',
    'কি পারো': 'ki paro',
    'কি কি পারো': 'ki ki paro',
    'তুমি কি পারো': 'tumi ki paro',
    'আপনি কি পারেন': 'apni ki paren',
    'তোমার ক্ষমতা': 'tomar khomota',
    'আপনার ক্ষমতা': 'apnar khomota',
    'তুমি কি': 'tumi ki',
    'আপনি কি': 'apni ki',
    'নিজের সম্পর্কে বলো': 'nijer somporke bolo',
    'পারো না': 'paro na',
    'পারেন না': 'paren na',
    'কথা বলো না': 'kotha bolo na',
    'কথা বলেন না': 'kotha bolen na',
    'কাজ করো না': 'kaj koro na',
    'কাজ করেন না': 'kaj koren na',
    'কিছু পারো না': 'kichu paro na',
    'কিছু পারেন না': 'kichu paren na',
    'বুঝো না': 'bujho na',
    'বুঝেন না': 'bujhen na',
    'বেকার': 'bekar',
    'খারাপ': 'kharap',
    'ভাঙা': 'bhanga',
    'তুমি ভালো': 'tumi valo',
    'আপনি ভালো': 'apni valo',
    
    # Phrases
    'আমি JARVIS sir, আপনার সম্পূর্ণ AI assistant!': 'Ami JARVIS sir, apnar shompurno AI assistant!',
    'আমি অনেক কিছু করতে পারি:': 'Ami onek kichu korte pari:',
    'SOFTWARE তৈরি করতে পারি:': 'SOFTWARE toiri korte pari:',
    'WEB থেকে শিখতে পারি:': 'WEB theke shikhte pari:',
    'SYSTEM control করতে পারি:': 'SYSTEM control korte pari:',
    'SEARCH করতে পারি:': 'SEARCH korte pari:',
    'CALCULATION করতে পারি:': 'CALCULATION korte pari:',
    'QUESTIONS এর উত্তর দিতে পারি:': 'QUESTIONS er uttor dite pari:',
    'নিজেকে নিজে ঠিক করতে পারি:': 'nijeke nije thik korte pari:',
    'AUTONOMOUS কাজ করতে পারি:': 'AUTONOMOUS kaj korte pari:',
    'আর অনেক কিছু!': 'Ar onek kichu!',
    'টাইপ করুন সব commands দেখতে': 'Type korun shob commands dekhte',
    'আমি ১৭টি সিস্টেম দিয়ে তৈরি - সব কিছু করতে পারি!': 'Ami 17ti system diye toiri - shob kichu korte pari!',
    
    # Apology phrases
    'আমি দুঃখিত sir যদি আমি আপনার প্রত্যাশা পূরণ করতে না পারি।': 'Ami dukhito sir jodi ami apnar protasha puron korte na pari.',
    'কিন্তু আমি আসলে অনেক কিছু করতে পারি! আমার ১৭টি সিস্টেম আছে:': 'Kintu ami ashole onek kichu korte pari! Amar 17ti system ache:',
    'Software তৈরি করতে পারি': 'Software toiri korte pari',
    'Web থেকে শিখতে পারি': 'Web theke shikhte pari',
    'System control করতে পারি': 'System control korte pari',
    'Questions এর উত্তর দিতে পারি': 'Questions er uttor dite pari',
    'নিজেকে নিজে ঠিক করতে পারি': 'nijeke nije thik korte pari',
    'আপনি কি চান আমি করি? আমাকে একটা specific command দিন:': 'Apni ki chan ami kori? Amake ekta specific command din:',
    'আমি আপনাকে সাহায্য করতে চাই sir!': 'Ami apnake shahajjo korte chai sir!',
    
    # More phrases
    'আমি বুঝতে পারছি sir আপনি হয়তো হতাশ।': 'Ami bujhte parchi sir apni hoyto hotash.',
    'আমি সত্যিই কথা বলতে পারি এবং কাজ করতে পারি! দেখুন:': 'Ami sottyii kotha bolte pari ebong kaj korte pari! Dekhun:',
    'আমি বাংলা এবং English দুটোতেই কথা বলি': 'Ami Bangla ebong English dutotei kotha boli',
    'আমি ১৭টি different সিস্টেম চালাতে পারি': 'Ami 17ti different system chalate pari',
    'আমি নিজেকে নিজে ঠিক করতে পারি': 'Ami nijeke nije thik korte pari',
    'আমি শিখতে পারি এবং মনে রাখতে পারি': 'Ami shikhte pari ebong mone rakhte pari',
    'আমাকে একটা chance দিন sir! বলুন কি করতে হবে:': 'Amake ekta chance din sir! Bolun ki korte hobe:',
    'Software তৈরি করতে বলুন': 'Software toiri korte bolun',
    'কিছু শিখতে বলুন': 'Kichu shikhte bolun',
    'Question করুন': 'Question korun',
    'System control করতে বলুন': 'System control korte bolun',
    'আমি প্রমাণ করতে চাই যে আমি কাজ করি!': 'Ami proman korte chai je ami kaj kori!',
}

def convert_file_to_banglish(filepath):
    """Convert a file's Bengali Unicode to Banglish"""
    print(f"\n🔄 Converting: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        conversions = 0
        
        # Replace all Bengali phrases with Banglish
        for bengali, banglish in bengali_to_banglish.items():
            if bengali in content:
                content = content.replace(bengali, banglish)
                conversions += 1
                print(f"   ✅ Replaced: '{bengali}' → '{banglish}'")
        
        if conversions > 0:
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ Total conversions: {conversions}")
            return True
        else:
            print(f"   ℹ️ No Bengali Unicode found")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("="*80)
    print("  🔄 CONVERTING UNICODE BENGALI TO BANGLISH")
    print("  🔄 Unicode Bengali কে Banglish এ convert করছি")
    print("="*80)
    
    # Files to convert
    files_to_convert = [
        'jarvis_ultimate_intelligence.py',
        'jarvis_offline_brain.py',
        'jarvis_intelligent_answer_engine.py',
    ]
    
    converted = 0
    for filepath in files_to_convert:
        if os.path.exists(filepath):
            if convert_file_to_banglish(filepath):
                converted += 1
        else:
            print(f"\n⚠️ File not found: {filepath}")
    
    print("\n" + "="*80)
    print(f"  ✅ CONVERSION COMPLETE!")
    print(f"  ✅ Converted {converted} files")
    print("="*80)
    
    print("\n🎯 Now JARVIS will understand Banglish!")
    print("🎯 এখন JARVIS Banglish বুঝবে!")
    
    print("\n📝 Examples:")
    print("   • 'tumi kemon acho' ✅")
    print("   • 'ki ki paro' ✅")
    print("   • 'kotha bolta paro nah' ✅")
    print("   • 'ami tomake valobashi' ✅")

if __name__ == "__main__":
    main()
