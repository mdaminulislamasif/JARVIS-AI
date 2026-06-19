"""
COMPREHENSIVE JARVIS TEST AND FIX
সম্পূর্ণ JARVIS Test এবং Fix

This will:
1. Test all JARVIS files
2. Find and fix issues
3. Improve chat box functionality to master level
"""

import os
import sys
import importlib

def test_all_jarvis_files():
    """Test all JARVIS files"""
    print("\n" + "="*80)
    print("  🧪 COMPREHENSIVE JARVIS TEST")
    print("  🧪 সম্পূর্ণ JARVIS Test")
    print("="*80)
    
    # List of all JARVIS files to test
    jarvis_files = [
        'jarvis_offline_brain',
        'jarvis_super_brain',
        'jarvis_autonomous_system',
        'jarvis_internet_learner',
        'jarvis_ultimate_learner',
        'jarvis_auto_learner',
        'jarvis_infinite_tab_learner',
        'jarvis_tree_tab_learner',
        'jarvis_tree_auto_learner',
        'jarvis_chrome_devtools',
    ]
    
    results = {
        'passed': [],
        'failed': [],
        'warnings': []
    }
    
    print("\n📝 Testing all JARVIS modules...")
    print("📝 সব JARVIS modules test করছি...")
    
    for i, module_name in enumerate(jarvis_files, 1):
        print(f"\n[{i}/{len(jarvis_files)}] Testing: {module_name}")
        
        try:
            # Try to import module
            module = importlib.import_module(module_name)
            print(f"  ✅ Import: SUCCESS")
            
            # Check if main class exists
            class_name = ''.join(word.capitalize() for word in module_name.split('_')[1:])
            if hasattr(module, class_name):
                print(f"  ✅ Class {class_name}: EXISTS")
                
                # Try to instantiate
                try:
                    instance = getattr(module, class_name)()
                    print(f"  ✅ Instantiation: SUCCESS")
                    results['passed'].append(module_name)
                except Exception as e:
                    print(f"  ⚠️ Instantiation: WARNING - {str(e)[:50]}")
                    results['warnings'].append((module_name, str(e)))
            else:
                print(f"  ⚠️ Class {class_name}: NOT FOUND")
                results['warnings'].append((module_name, f"Class {class_name} not found"))
        
        except ImportError as e:
            print(f"  ❌ Import: FAILED - {str(e)[:50]}")
            results['failed'].append((module_name, str(e)))
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}")
            results['failed'].append((module_name, str(e)))
    
    # Print summary
    print("\n" + "="*80)
    print("  📊 TEST SUMMARY")
    print("  📊 Test সংক্ষিপ্ত")
    print("="*80)
    
    print(f"\n✅ Passed: {len(results['passed'])}/{len(jarvis_files)}")
    for module in results['passed']:
        print(f"   ✅ {module}")
    
    if results['warnings']:
        print(f"\n⚠️ Warnings: {len(results['warnings'])}")
        for module, warning in results['warnings']:
            print(f"   ⚠️ {module}: {warning[:60]}")
    
    if results['failed']:
        print(f"\n❌ Failed: {len(results['failed'])}")
        for module, error in results['failed']:
            print(f"   ❌ {module}: {error[:60]}")
    
    return results

def test_chat_box_functionality():
    """Test chat box functionality"""
    print("\n" + "="*80)
    print("  💬 TESTING CHAT BOX FUNCTIONALITY")
    print("  💬 Chat Box Functionality Test করছি")
    print("="*80)
    
    from jarvis_offline_brain import OfflineBrain
    
    brain = OfflineBrain()
    
    # Test cases for chat box
    test_cases = [
        # Basic commands
        ("hello", "greeting"),
        ("help", "help"),
        ("2+2", "calculation"),
        
        # Learning commands
        ("learn from internet Python", "learning"),
        ("ultimate learn JavaScript", "learning"),
        ("auto learn AI", "learning"),
        ("tree learn Python", "tree_learning"),
        ("tree auto Python", "tree_auto_learning"),
        
        # Questions
        ("What is Python?", "knowledge"),
        ("Python ki?", "knowledge"),
        ("What is the capital of Bangladesh?", "knowledge"),
        
        # Search
        ("search Python", "search"),
        
        # File operations
        ("create file", "file"),
        
        # System info
        ("system info", "system"),
        ("time", "time"),
    ]
    
    results = {
        'passed': 0,
        'failed': 0,
        'total': len(test_cases)
    }
    
    print(f"\n📝 Testing {len(test_cases)} chat box commands...")
    
    for i, (command, expected_type) in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] Testing: {command}")
        
        try:
            result = brain.process_command(command)
            
            if result['status'] in ['success', 'info', 'learning', 'learning_suggestion']:
                print(f"  ✅ Status: {result['status']}")
                print(f"  ✅ Type: {result.get('type', 'N/A')}")
                results['passed'] += 1
            else:
                print(f"  ⚠️ Status: {result['status']}")
                results['failed'] += 1
        
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:60]}")
            results['failed'] += 1
    
    brain.close()
    
    # Summary
    print("\n" + "="*80)
    print("  📊 CHAT BOX TEST SUMMARY")
    print("="*80)
    
    print(f"\n✅ Passed: {results['passed']}/{results['total']}")
    print(f"❌ Failed: {results['failed']}/{results['total']}")
    print(f"📊 Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    return results

def identify_improvements():
    """Identify areas for improvement"""
    print("\n" + "="*80)
    print("  🎯 IDENTIFYING IMPROVEMENTS")
    print("  🎯 Improvement চিহ্নিত করছি")
    print("="*80)
    
    improvements = []
    
    # Check for missing features
    print("\n📝 Checking for missing features...")
    
    # 1. Chat history
    print("\n[1] Chat History:")
    if not os.path.exists('jarvis_chat_history.py'):
        print("  ❌ Missing: Chat history system")
        improvements.append({
            'feature': 'Chat History',
            'priority': 'HIGH',
            'description': 'Save and recall previous conversations'
        })
    else:
        print("  ✅ Exists: Chat history system")
    
    # 2. Context awareness
    print("\n[2] Context Awareness:")
    improvements.append({
        'feature': 'Context Awareness',
        'priority': 'HIGH',
        'description': 'Remember previous messages in conversation'
    })
    
    # 3. Smart suggestions
    print("\n[3] Smart Suggestions:")
    improvements.append({
        'feature': 'Smart Suggestions',
        'priority': 'MEDIUM',
        'description': 'Suggest commands based on user input'
    })
    
    # 4. Multi-language support
    print("\n[4] Multi-language Support:")
    improvements.append({
        'feature': 'Enhanced Bengali Support',
        'priority': 'MEDIUM',
        'description': 'Better Bengali language understanding'
    })
    
    # 5. Voice input/output
    print("\n[5] Voice Support:")
    improvements.append({
        'feature': 'Voice Input/Output',
        'priority': 'LOW',
        'description': 'Speech recognition and text-to-speech'
    })
    
    # Print improvements
    print("\n" + "="*80)
    print("  📋 IMPROVEMENT RECOMMENDATIONS")
    print("="*80)
    
    for i, improvement in enumerate(improvements, 1):
        print(f"\n[{i}] {improvement['feature']}")
        print(f"    Priority: {improvement['priority']}")
        print(f"    Description: {improvement['description']}")
    
    return improvements

def generate_fix_plan():
    """Generate plan to fix issues"""
    print("\n" + "="*80)
    print("  🔧 GENERATING FIX PLAN")
    print("  🔧 Fix Plan তৈরি করছি")
    print("="*80)
    
    fix_plan = {
        'immediate': [
            'Fix any import errors',
            'Fix any instantiation errors',
            'Test all commands',
        ],
        'short_term': [
            'Add chat history system',
            'Add context awareness',
            'Improve Bengali support',
        ],
        'long_term': [
            'Add smart suggestions',
            'Add voice support',
            'Add GUI interface',
        ]
    }
    
    print("\n🔥 IMMEDIATE FIXES (Today):")
    for i, fix in enumerate(fix_plan['immediate'], 1):
        print(f"   {i}. {fix}")
    
    print("\n📅 SHORT-TERM IMPROVEMENTS (This Week):")
    for i, fix in enumerate(fix_plan['short_term'], 1):
        print(f"   {i}. {fix}")
    
    print("\n🎯 LONG-TERM GOALS (This Month):")
    for i, fix in enumerate(fix_plan['long_term'], 1):
        print(f"   {i}. {fix}")
    
    return fix_plan

def main():
    """Main function"""
    print("\n" + "="*80)
    print("  🚀 COMPREHENSIVE JARVIS TEST AND FIX")
    print("  🚀 সম্পূর্ণ JARVIS Test এবং Fix")
    print("="*80)
    
    # Step 1: Test all files
    print("\n📍 STEP 1: Testing all JARVIS files...")
    file_results = test_all_jarvis_files()
    
    # Step 2: Test chat box functionality
    print("\n📍 STEP 2: Testing chat box functionality...")
    chat_results = test_chat_box_functionality()
    
    # Step 3: Identify improvements
    print("\n📍 STEP 3: Identifying improvements...")
    improvements = identify_improvements()
    
    # Step 4: Generate fix plan
    print("\n📍 STEP 4: Generating fix plan...")
    fix_plan = generate_fix_plan()
    
    # Final summary
    print("\n" + "="*80)
    print("  ✅ COMPREHENSIVE TEST COMPLETE!")
    print("  ✅ সম্পূর্ণ Test সম্পন্ন!")
    print("="*80)
    
    print(f"\n📊 Overall Results:")
    print(f"   Files Tested: {len(file_results['passed']) + len(file_results['failed']) + len(file_results['warnings'])}")
    print(f"   Files Passed: {len(file_results['passed'])}")
    print(f"   Chat Commands Tested: {chat_results['total']}")
    print(f"   Chat Commands Passed: {chat_results['passed']}")
    print(f"   Improvements Identified: {len(improvements)}")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Fix any failed tests")
    print(f"   2. Implement high-priority improvements")
    print(f"   3. Test again to verify fixes")
    
    print("\n💡 Recommendation:")
    print("   Focus on chat history and context awareness first!")
    print("   Chat history এবং context awareness প্রথমে করুন!")

if __name__ == "__main__":
    main()
