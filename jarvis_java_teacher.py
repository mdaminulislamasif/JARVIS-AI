#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS JAVA TEACHER
জার্ভিস জাভা শিক্ষক

Complete Java Programming Course with Bengali Support
বাংলা সমর্থন সহ সম্পূর্ণ জাভা প্রোগ্রামিং কোর্স

Features / বৈশিষ্ট্য:
1. Step-by-step Java lessons / ধাপে ধাপে জাভা পাঠ
2. Interactive code examples / ইন্টারঅ্যাক্টিভ কোড উদাহরণ
3. Practice exercises / অনুশীলন ব্যায়াম
4. Progress tracking / অগ্রগতি ট্র্যাকিং
5. Bilingual support (English + Bengali) / দ্বিভাষিক সমর্থন
"""

import os
import sys
import sqlite3
from datetime import datetime

DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

class JavaTeacher:
    """JARVIS Java Teacher System"""
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.current_lesson = 1
        self.create_tables()
        
        # Java curriculum structure
        self.lessons = {
            1: {
                'title_en': 'Introduction to Java',
                'title_bn': 'জাভার পরিচিতি',
                'topics': ['What is Java', 'JDK Installation', 'First Program', 'Basic Syntax']
            },
            2: {
                'title_en': 'Variables and Data Types',
                'title_bn': 'ভেরিয়েবল এবং ডেটা টাইপ',
                'topics': ['Primitive Types', 'Reference Types', 'Type Casting', 'Constants']
            },
            3: {
                'title_en': 'Operators and Expressions',
                'title_bn': 'অপারেটর এবং এক্সপ্রেশন',
                'topics': ['Arithmetic', 'Relational', 'Logical', 'Bitwise']
            },
            4: {
                'title_en': 'Control Flow Statements',
                'title_bn': 'কন্ট্রোল ফ্লো স্টেটমেন্ট',
                'topics': ['if-else', 'switch', 'for loop', 'while loop']
            },
            5: {
                'title_en': 'Arrays and Strings',
                'title_bn': 'অ্যারে এবং স্ট্রিং',
                'topics': ['Array Declaration', 'Multi-dimensional Arrays', 'String Methods', 'StringBuilder']
            },
            6: {
                'title_en': 'Object-Oriented Programming Basics',
                'title_bn': 'অবজেক্ট-ওরিয়েন্টেড প্রোগ্রামিং মূল বিষয়',
                'topics': ['Classes', 'Objects', 'Methods', 'Constructors']
            },
            7: {
                'title_en': 'Inheritance and Polymorphism',
                'title_bn': 'ইনহেরিটেন্স এবং পলিমরফিজম',
                'topics': ['extends keyword', 'Method Overriding', 'super keyword', 'Abstract Classes']
            },
            8: {
                'title_en': 'Interfaces and Packages',
                'title_bn': 'ইন্টারফেস এবং প্যাকেজ',
                'topics': ['Interface Definition', 'implements keyword', 'Package Creation', 'import statements']
            },
            9: {
                'title_en': 'Exception Handling',
                'title_bn': 'এক্সেপশন হ্যান্ডলিং',
                'topics': ['try-catch', 'throw', 'throws', 'Custom Exceptions']
            },
            10: {
                'title_en': 'Collections Framework',
                'title_bn': 'কালেকশন ফ্রেমওয়ার্ক',
                'topics': ['ArrayList', 'HashMap', 'HashSet', 'Iterator']
            },
            11: {
                'title_en': 'File I/O and Streams',
                'title_bn': 'ফাইল I/O এবং স্ট্রিম',
                'topics': ['FileReader', 'FileWriter', 'BufferedReader', 'Serialization']
            },
            12: {
                'title_en': 'Multithreading',
                'title_bn': 'মাল্টিথ্রেডিং',
                'topics': ['Thread Class', 'Runnable Interface', 'Synchronization', 'Thread Pool']
            },
            13: {
                'title_en': 'Lambda Expressions and Streams',
                'title_bn': 'ল্যাম্বডা এক্সপ্রেশন এবং স্ট্রিম',
                'topics': ['Lambda Syntax', 'Functional Interfaces', 'Stream API', 'Collectors']
            },
            14: {
                'title_en': 'JDBC and Database Connectivity',
                'title_bn': 'JDBC এবং ডেটাবেস সংযোগ',
                'topics': ['JDBC Drivers', 'Connection', 'Statement', 'ResultSet']
            },
            15: {
                'title_en': 'Advanced Topics',
                'title_bn': 'উন্নত বিষয়',
                'topics': ['Generics', 'Annotations', 'Reflection', 'Design Patterns']
            }
        }
    
    def create_tables(self):
        """Create database tables for tracking progress"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS java_learning_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lesson_number INTEGER NOT NULL,
                    lesson_title TEXT NOT NULL,
                    completed BOOLEAN DEFAULT 0,
                    completion_date TIMESTAMP,
                    notes TEXT,
                    score INTEGER DEFAULT 0
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS java_code_examples (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lesson_number INTEGER NOT NULL,
                    example_title TEXT NOT NULL,
                    code TEXT NOT NULL,
                    explanation_en TEXT,
                    explanation_bn TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Error creating tables: {e}")
    
    def show_banner(self):
        """Display welcome banner"""
        print("\n" + "="*80)
        print("  ☕ JARVIS JAVA TEACHER")
        print("  ☕ জার্ভিস জাভা শিক্ষক")
        print("="*80)
        print("  Learn Java Programming from Basics to Advanced")
        print("  মৌলিক থেকে উন্নত পর্যন্ত জাভা প্রোগ্রামিং শিখুন")
        print("="*80 + "\n")
    
    def show_curriculum(self):
        """Display complete curriculum"""
        print("\n" + "="*80)
        print("  📚 JAVA LEARNING CURRICULUM")
        print("  📚 জাভা শিক্ষা পাঠ্যক্রম")
        print("="*80 + "\n")
        
        for lesson_num, lesson_data in self.lessons.items():
            status = self.get_lesson_status(lesson_num)
            status_icon = "✅" if status else "⭕"
            
            print(f"  {status_icon} Lesson {lesson_num}: {lesson_data['title_en']}")
            print(f"     পাঠ {lesson_num}: {lesson_data['title_bn']}")
            print(f"     Topics: {', '.join(lesson_data['topics'])}\n")
    
    def get_lesson_status(self, lesson_num):
        """Check if lesson is completed"""
        try:
            self.cursor.execute("""
                SELECT completed FROM java_learning_progress
                WHERE lesson_number = ?
            """, (lesson_num,))
            result = self.cursor.fetchone()
            return result[0] if result else False
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return False
    
    def teach_lesson_1(self):
        """Lesson 1: Introduction to Java"""
        print("\n" + "="*80)
        print("  📖 LESSON 1: INTRODUCTION TO JAVA")
        print("  📖 পাঠ ১: জাভার পরিচিতি")
        print("="*80 + "\n")
        
        content = """
🌟 What is Java? / জাভা কি?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Java is a high-level, object-oriented programming language developed by Sun 
Microsystems (now Oracle) in 1995.

জাভা একটি উচ্চ-স্তরের, অবজেক্ট-ওরিয়েন্টেড প্রোগ্রামিং ভাষা যা সান মাইক্রোসিস্টেমস 
(এখন ওরাকল) ১৯৯৫ সালে তৈরি করেছিল।

Key Features / মূল বৈশিষ্ট্য:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ☕ Platform Independent (Write Once, Run Anywhere)
   প্ল্যাটফর্ম স্বাধীন (একবার লিখুন, যেকোনো জায়গায় চালান)

2. 🎯 Object-Oriented (Everything is an object)
   অবজেক্ট-ওরিয়েন্টেড (সবকিছু একটি অবজেক্ট)

3. 🔒 Secure (Built-in security features)
   নিরাপদ (অন্তর্নির্মিত নিরাপত্তা বৈশিষ্ট্য)

4. 🚀 Robust (Strong memory management)
   শক্তিশালী (শক্তিশালী মেমরি ম্যানেজমেন্ট)

5. 🌐 Multithreaded (Concurrent programming support)
   মাল্টিথ্রেডেড (সমসাময়িক প্রোগ্রামিং সমর্থন)


📝 Your First Java Program / আপনার প্রথম জাভা প্রোগ্রাম:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        print(content)
        
        # Show first program
        code_example = '''
// HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        System.out.println("হ্যালো, ওয়ার্ল্ড!");
    }
}
'''
        print("```java")
        print(code_example)
        print("```\n")
        
        explanation = """
📖 Code Explanation / কোড ব্যাখ্যা:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. public class HelloWorld
   - Declares a public class named HelloWorld
   - HelloWorld নামে একটি পাবলিক ক্লাস ঘোষণা করে

2. public static void main(String[] args)
   - The main method - entry point of the program
   - মেইন মেথড - প্রোগ্রামের প্রবেশ পয়েন্ট

3. System.out.println()
   - Prints text to console
   - কনসোলে টেক্সট প্রিন্ট করে


🔧 How to Compile and Run / কিভাবে কম্পাইল এবং চালাবেন:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Save the file as HelloWorld.java
        ফাইলটি HelloWorld.java হিসাবে সংরক্ষণ করুন

Step 2: Compile the program
        প্রোগ্রামটি কম্পাইল করুন
        
        javac HelloWorld.java

Step 3: Run the program
        প্রোগ্রামটি চালান
        
        java HelloWorld


💡 Important Notes / গুরুত্বপূর্ণ নোট:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Class name must match filename (HelloWorld.java → class HelloWorld)
  ক্লাসের নাম ফাইলের নামের সাথে মিলতে হবে

• Java is case-sensitive (HelloWorld ≠ helloworld)
  জাভা কেস-সেনসিটিভ

• Every statement ends with semicolon (;)
  প্রতিটি স্টেটমেন্ট সেমিকোলন দিয়ে শেষ হয়

• main() method is required to run the program
  প্রোগ্রাম চালানোর জন্য main() মেথড প্রয়োজন
"""
        print(explanation)
        
        # Save to database
        self.save_code_example(1, "Hello World Program", code_example,
                              "First Java program that prints Hello World",
                              "প্রথম জাভা প্রোগ্রাম যা হ্যালো ওয়ার্ল্ড প্রিন্ট করে")
        
        # Practice exercise
        self.show_practice_exercise_1()
    
    def show_practice_exercise_1(self):
        """Practice exercise for Lesson 1"""
        print("\n" + "="*80)
        print("  ✏️ PRACTICE EXERCISE / অনুশীলন ব্যায়াম")
        print("="*80 + "\n")
        
        exercise = """
📝 Exercise 1: Create a program that prints your name and favorite programming language

   ব্যায়াম ১: একটি প্রোগ্রাম তৈরি করুন যা আপনার নাম এবং প্রিয় প্রোগ্রামিং ভাষা প্রিন্ট করে

   Example Output:
   My name is: [Your Name]
   My favorite language is: Java

📝 Exercise 2: Modify the Hello World program to print 5 different messages

   ব্যায়াম ২: হ্যালো ওয়ার্ল্ড প্রোগ্রামটি পরিবর্তন করুন ৫টি ভিন্ন বার্তা প্রিন্ট করতে

📝 Exercise 3: Create a program that prints a simple pattern:
   
   ব্যায়াম ৩: একটি প্রোগ্রাম তৈরি করুন যা একটি সাধারণ প্যাটার্ন প্রিন্ট করে:

   *
   **
   ***
   ****
   *****
"""
        print(exercise)
    
    def teach_lesson_2(self):
        """Lesson 2: Variables and Data Types"""
        print("\n" + "="*80)
        print("  📖 LESSON 2: VARIABLES AND DATA TYPES")
        print("  📖 পাঠ ২: ভেরিয়েবল এবং ডেটা টাইপ")
        print("="*80 + "\n")
        
        content = """
🔢 What are Variables? / ভেরিয়েবল কি?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Variables are containers that store data values.
ভেরিয়েবল হল কন্টেইনার যা ডেটা মান সংরক্ষণ করে।

Syntax: dataType variableName = value;


📊 Primitive Data Types / প্রিমিটিভ ডেটা টাইপ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. byte    - 8-bit integer  (-128 to 127)
2. short   - 16-bit integer (-32,768 to 32,767)
3. int     - 32-bit integer (-2 billion to 2 billion)
4. long    - 64-bit integer (very large numbers)
5. float   - 32-bit decimal (6-7 decimal digits)
6. double  - 64-bit decimal (15 decimal digits)
7. char    - Single character ('A', 'b', '1')
8. boolean - true or false
"""
        print(content)
        
        code_example = '''
// VariablesDemo.java
public class VariablesDemo {
    public static void main(String[] args) {
        // Integer types / পূর্ণসংখ্যা টাইপ
        byte age = 25;
        short year = 2024;
        int population = 1000000;
        long distance = 9876543210L;
        
        // Floating-point types / দশমিক সংখ্যা টাইপ
        float price = 99.99f;
        double pi = 3.14159265359;
        
        // Character and Boolean / অক্ষর এবং বুলিয়ান
        char grade = 'A';
        boolean isJavaFun = true;
        
        // String (Reference type) / স্ট্রিং (রেফারেন্স টাইপ)
        String name = "JARVIS";
        String message = "জাভা শিখছি";
        
        // Print all variables / সব ভেরিয়েবল প্রিন্ট করুন
        System.out.println("Age: " + age);
        System.out.println("Year: " + year);
        System.out.println("Population: " + population);
        System.out.println("Distance: " + distance);
        System.out.println("Price: $" + price);
        System.out.println("Pi: " + pi);
        System.out.println("Grade: " + grade);
        System.out.println("Is Java Fun? " + isJavaFun);
        System.out.println("Name: " + name);
        System.out.println("Message: " + message);
    }
}
'''
        print("```java")
        print(code_example)
        print("```\n")
        
        explanation = """
💡 Important Rules / গুরুত্বপূর্ণ নিয়ম:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Variable names must start with letter, $, or _
   ভেরিয়েবলের নাম অক্ষর, $, বা _ দিয়ে শুরু হতে হবে

2. Cannot use Java keywords (int, class, public, etc.)
   জাভা কীওয়ার্ড ব্যবহার করা যাবে না

3. Use camelCase for variable names (myAge, studentName)
   ভেরিয়েবলের নামের জন্য camelCase ব্যবহার করুন

4. long values end with 'L', float values end with 'f'
   long মান 'L' দিয়ে শেষ হয়, float মান 'f' দিয়ে শেষ হয়

5. Strings use double quotes "", chars use single quotes ''
   স্ট্রিং ডাবল কোট "" ব্যবহার করে, char সিঙ্গেল কোট '' ব্যবহার করে


🔄 Type Casting / টাইপ কাস্টিং:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Widening (Automatic):  byte → short → int → long → float → double
Narrowing (Manual):    double → float → long → int → short → byte

Example:
int myInt = 9;
double myDouble = myInt;        // Automatic casting
double myDouble2 = 9.78;
int myInt2 = (int) myDouble2;   // Manual casting
"""
        print(explanation)
        
        self.save_code_example(2, "Variables and Data Types", code_example,
                              "Demonstrates all primitive data types in Java",
                              "জাভাতে সমস্ত প্রিমিটিভ ডেটা টাইপ প্রদর্শন করে")
    
    def save_code_example(self, lesson_num, title, code, explanation_en, explanation_bn):
        """Save code example to database"""
        try:
            self.cursor.execute("""
                INSERT INTO java_code_examples 
                (lesson_number, example_title, code, explanation_en, explanation_bn)
                VALUES (?, ?, ?, ?, ?)
            """, (lesson_num, title, code, explanation_en, explanation_bn))
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Error saving example: {e}")
    
    def mark_lesson_complete(self, lesson_num):
        """Mark a lesson as completed"""
        try:
            lesson_data = self.lessons.get(lesson_num)
            if not lesson_data:
                print("❌ Invalid lesson number")
                return
            
            self.cursor.execute("""
                INSERT OR REPLACE INTO java_learning_progress
                (lesson_number, lesson_title, completed, completion_date)
                VALUES (?, ?, 1, ?)
            """, (lesson_num, lesson_data['title_en'], datetime.now()))
            
            self.conn.commit()
            print(f"\n✅ Lesson {lesson_num} marked as complete!")
            print(f"✅ পাঠ {lesson_num} সম্পূর্ণ হিসাবে চিহ্নিত!")
        except Exception as e:
            print(f"⚠️ Error: {e}")
    
    def show_progress(self):
        """Show learning progress"""
        print("\n" + "="*80)
        print("  📊 YOUR LEARNING PROGRESS")
        print("  📊 আপনার শিক্ষার অগ্রগতি")
        print("="*80 + "\n")
        
        try:
            self.cursor.execute("""
                SELECT lesson_number, lesson_title, completion_date
                FROM java_learning_progress
                WHERE completed = 1
                ORDER BY lesson_number
            """)
            
            completed = self.cursor.fetchall()
            total_lessons = len(self.lessons)
            completed_count = len(completed)
            
            progress_percent = (completed_count / total_lessons) * 100
            
            print(f"  Completed: {completed_count}/{total_lessons} lessons ({progress_percent:.1f}%)")
            print(f"  সম্পন্ন: {completed_count}/{total_lessons} পাঠ ({progress_percent:.1f}%)\n")
            
            if completed:
                print("  Completed Lessons / সম্পন্ন পাঠ:\n")
                for lesson_num, title, date in completed:
                    print(f"  ✅ Lesson {lesson_num}: {title}")
                    print(f"     Completed on: {date}\n")
            else:
                print("  No lessons completed yet. Start learning!")
                print("  এখনো কোনো পাঠ সম্পন্ন হয়নি। শেখা শুরু করুন!")
        
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    """Main function"""
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return
    
    teacher = JavaTeacher()
    teacher.show_banner()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "curriculum":
            teacher.show_curriculum()
        elif command == "progress":
            teacher.show_progress()
        elif command.startswith("lesson"):
            try:
                lesson_num = int(sys.argv[2]) if len(sys.argv) > 2 else 1
                if lesson_num == 1:
                    teacher.teach_lesson_1()
                elif lesson_num == 2:
                    teacher.teach_lesson_2()
                else:
                    print(f"📚 Lesson {lesson_num} content coming soon!")
                    print(f"📚 পাঠ {lesson_num} বিষয়বস্তু শীঘ্রই আসছে!")
            except ValueError:
                print("❌ Invalid lesson number")
        elif command == "complete":
            try:
                lesson_num = int(sys.argv[2])
                teacher.mark_lesson_complete(lesson_num)
            except (ValueError, IndexError):
                print("❌ Usage: python jarvis_java_teacher.py complete <lesson_number>")
        else:
            print("❌ Unknown command")
    else:
        # Show menu
        print("📚 Available Commands / উপলব্ধ কমান্ড:\n")
        print("  python jarvis_java_teacher.py curriculum    - Show all lessons")
        print("  python jarvis_java_teacher.py lesson 1      - Start Lesson 1")
        print("  python jarvis_java_teacher.py lesson 2      - Start Lesson 2")
        print("  python jarvis_java_teacher.py progress      - Show your progress")
        print("  python jarvis_java_teacher.py complete 1    - Mark lesson as complete\n")
        
        # Show quick start
        print("="*80)
        print("  🚀 QUICK START / দ্রুত শুরু")
        print("="*80 + "\n")
        print("  Start with Lesson 1:")
        print("  পাঠ ১ দিয়ে শুরু করুন:\n")
        print("  python jarvis_java_teacher.py lesson 1\n")
    
    teacher.close()

if __name__ == "__main__":
    main()
