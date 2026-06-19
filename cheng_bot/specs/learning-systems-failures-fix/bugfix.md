# Bugfix Requirements Document

## Introduction

JARVIS has 4 learning systems (MRX) that are all failing due to multiple critical bugs. These systems are designed to learn from the internet using different approaches: Internet Learner (quick facts), Ultimate Learner (Chrome + Google deep learning), Auto Learner (word-by-word learning), and Autonomous System (advanced automation). Additionally, URLs are being misinterpreted as mathematical calculations instead of being recognized as learning targets.

The failures prevent users from learning about any topic (youtube, facebook, websites, etc.) and block the core learning functionality that JARVIS depends on.

## Bug Analysis

### Current Behavior (Defect)

**System 1: Internet Learner**
1.1 WHEN user tries to learn about 'youtube' or 'facebook' from internet THEN the system returns "❌ Could not learn about 'youtube' from internet"

1.2 WHEN user tries to learn about 'youtube.com' or 'facebook.com' from internet THEN the system returns "❌ Could not learn about 'youtube.com' from internet"

**System 2: Ultimate Learner (Chrome + Google)**
1.3 WHEN user tries to use ultimate learner for 'youtube' THEN the system returns "❌ Could not learn about 'youtube'"

1.4 WHEN user tries to use ultimate learner for any website THEN all learning attempts fail

**System 3: Auto Learner (Word by Word)**
1.5 WHEN user tries to use auto learner THEN the system crashes with "'AutonomousSystem' object has no attribute 'execute_autonomous_task'"

1.6 WHEN jarvis_offline_brain.py calls autonomous.execute_autonomous_task(user_input) THEN AttributeError is raised because the method does not exist

1.7 WHEN jarvis_offline_brain.py calls auto_learner.learn_word_by_word(topic) THEN the system fails because the method expects text but receives a topic string

**System 4: URL Learning**
1.8 WHEN user enters "https://www.youtube.com/" THEN the system misinterprets it as a calculation and returns "Could not understand the calculation. Try: '2+2' or 'calculate 10 * 5'"

1.9 WHEN user enters any URL with "/" character THEN the calculation detector triggers because "/" is treated as division operator

1.10 WHEN jarvis_offline_brain.py checks for calculation on line 178 THEN it matches URLs because they contain "/" character

### Expected Behavior (Correct)

**System 1: Internet Learner**
2.1 WHEN user tries to learn about 'youtube' or 'facebook' from internet THEN the system SHALL successfully search Wikipedia and web sources and return learned content

2.2 WHEN user tries to learn about 'youtube.com' or 'facebook.com' from internet THEN the system SHALL successfully learn about the website and save to knowledge base

**System 2: Ultimate Learner (Chrome + Google)**
2.3 WHEN user tries to use ultimate learner for 'youtube' THEN the system SHALL open Chrome, search Google, learn from Wikipedia and multiple sources, and return comprehensive knowledge

2.4 WHEN user tries to use ultimate learner for any website THEN the system SHALL successfully learn from Chrome + Google and save all knowledge

**System 3: Auto Learner (Word by Word)**
2.5 WHEN user tries to use auto learner THEN the system SHALL have a valid execute_autonomous_task method that processes the learning request

2.6 WHEN jarvis_offline_brain.py calls autonomous.execute_autonomous_task(user_input) THEN the method SHALL exist and process the autonomous learning task

2.7 WHEN jarvis_offline_brain.py calls auto_learner for a topic THEN it SHALL call auto_learn_everything(topic) instead of learn_word_by_word(topic)

**System 4: URL Learning**
2.8 WHEN user enters "https://www.youtube.com/" THEN the system SHALL recognize it as a URL and trigger learning about the website

2.9 WHEN user enters any URL with "/" character THEN the system SHALL detect it as a URL before checking for calculations

2.10 WHEN jarvis_offline_brain.py checks for calculation THEN it SHALL first exclude URLs from calculation detection

### Unchanged Behavior (Regression Prevention)

**Calculation System**
3.1 WHEN user enters "2+2" or "calculate 10 * 5" THEN the system SHALL CONTINUE TO perform mathematical calculations correctly

3.2 WHEN user enters valid mathematical expressions with +, -, *, / operators THEN the system SHALL CONTINUE TO evaluate them correctly

**Learning Systems - Valid Inputs**
3.3 WHEN user learns about valid topics like "Python", "AI", "programming" THEN all 4 learning systems SHALL CONTINUE TO work correctly

3.4 WHEN user uses "learn from internet Python" command THEN Internet Learner SHALL CONTINUE TO search and learn successfully

**Other Commands**
3.5 WHEN user uses non-learning commands like "open chrome", "search Python", "create file" THEN the system SHALL CONTINUE TO process them correctly

3.6 WHEN user asks questions or uses other JARVIS features THEN they SHALL CONTINUE TO work without interference from the bug fixes
