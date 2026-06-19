# Implementation Plan

## Overview
This implementation plan fixes 4 critical learning system failures in JARVIS using the bug condition methodology. The plan follows the exploratory bugfix workflow: explore bugs first, write preservation tests, then implement fixes with validation.

---

## Phase 1: Bug Condition Exploration (BEFORE Fix)

- [x] 1. Write bug condition exploration tests for all 4 learning system failures
  - **Property 1: Bug Condition** - Learning Systems Failures
  - **CRITICAL**: These tests MUST FAIL on unfixed code - failures confirm the bugs exist
  - **DO NOT attempt to fix the tests or the code when they fail**
  - **NOTE**: These tests encode the expected behavior - they will validate the fixes when they pass after implementation
  - **GOAL**: Surface counterexamples that demonstrate all 4 bugs exist
  - **Scoped PBT Approach**: For deterministic bugs, scope properties to concrete failing cases to ensure reproducibility
  
  - **Test 1.1: Internet Learner - Website Names**
    - Test that `internet_learner.search_and_learn('youtube')` fails on unfixed code
    - Test that `internet_learner.search_and_learn('facebook.com')` fails on unfixed code
    - Assert returns error status with "Could not learn" message
    - Document counterexamples: specific error messages and failure points
  
  - **Test 1.2: Ultimate Learner - API Failures**
    - Test that `ultimate_learner.learn_everything('youtube')` fails on unfixed code
    - Mock Wikipedia API to return 404, verify error propagation
    - Assert returns error status instead of partial results
    - Document counterexamples: which APIs fail and how errors propagate
  
  - **Test 1.3: Auto Learner - Wrong Method Call**
    - Test that `offline_brain.process_command('auto learn Python')` crashes on unfixed code
    - Assert TypeError or AttributeError due to wrong method signature
    - Document counterexamples: exact error message and stack trace
  
  - **Test 1.4: Autonomous System - Missing Method**
    - Test that `offline_brain.process_command('autonomous learn Python')` crashes on unfixed code
    - Assert AttributeError: 'AutonomousSystem' object has no attribute 'execute_autonomous_task'
    - Document counterexamples: exact error and missing method name
  
  - **Test 1.5: URL Calculation - Misinterpretation**
    - Test that `offline_brain.process_command('https://www.youtube.com/')` fails on unfixed code
    - Assert returns "Could not understand the calculation" error
    - Document counterexamples: URLs that are misinterpreted as calculations
  
  - Run tests on UNFIXED code
  - **EXPECTED OUTCOME**: All tests FAIL (this is correct - it proves the bugs exist)
  - Document all counterexamples found to understand root causes
  - Mark task complete when tests are written, run, and failures are documented
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10_

---

## Phase 2: Preservation Property Tests (BEFORE Fix)

- [x] 2. Write preservation property tests for non-buggy behavior
  - **Property 2: Preservation** - Calculation and Learning Systems Preservation
  - **IMPORTANT**: Follow observation-first methodology
  - Observe behavior on UNFIXED code for non-buggy inputs
  - Write property-based tests capturing observed behavior patterns from Preservation Requirements
  - Property-based testing generates many test cases for stronger guarantees
  
  - **Test 2.1: Calculation System Preservation**
    - Observe: "2+2" returns 4 on unfixed code
    - Observe: "calculate 10 * 5" returns 50 on unfixed code
    - Observe: "25 - 17" returns 8 on unfixed code
    - Observe: "100 / 4" returns 25 on unfixed code
    - Write property-based test: for all valid mathematical expressions (contains +, -, *, / but NOT URL patterns), result equals correct calculation
    - Verify test passes on UNFIXED code
  
  - **Test 2.2: Valid Learning Topics Preservation**
    - Observe: "learn from internet Python" works on unfixed code
    - Observe: "ultimate learn AI" works on unfixed code
    - Observe: "auto learn programming" behavior on unfixed code (may fail due to bug, but observe what happens)
    - Write property-based test: for all valid non-website topics, learning systems return success or expected behavior
    - Verify test passes on UNFIXED code (for working systems)
  
  - **Test 2.3: Other Commands Preservation**
    - Observe: "open chrome" works on unfixed code
    - Observe: "search Python" works on unfixed code
    - Observe: "create file test.txt" works on unfixed code
    - Observe: "system info" works on unfixed code
    - Write property-based test: for all non-learning commands, behavior is unchanged
    - Verify test passes on UNFIXED code
  
  - **Test 2.4: Question Preservation**
    - Observe: "What is Python?" behavior on unfixed code
    - Observe: "How many planets?" behavior on unfixed code
    - Write property-based test: for all question inputs, behavior is unchanged
    - Verify test passes on UNFIXED code
  
  - Run tests on UNFIXED code
  - **EXPECTED OUTCOME**: Tests PASS (this confirms baseline behavior to preserve)
  - Mark task complete when tests are written, run, and passing on unfixed code
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

---

## Phase 3: Implementation

- [-] 3. Fix all 4 learning system failures

  - [x] 3.1 Fix Internet Learner - Add fallback mechanisms for website names
    - Add `_get_builtin_knowledge(topic)` method with pre-defined information for common websites (youtube, facebook, google, twitter, etc.)
    - Improve `_learn_from_web()` with retry logic and different user agents
    - Add alternative search engines (DuckDuckGo, Bing) if Google fails
    - Add DuckDuckGo Instant Answer API as fallback
    - Modify `search_and_learn()` to try all fallbacks: Wikipedia → Web Search → Alternative APIs → Built-in Knowledge
    - Return success if ANY source provides content
    - _Bug_Condition: isBugCondition_InternetLearner(input) where input IN ['youtube', 'facebook', 'youtube.com', 'facebook.com'] AND Wikipedia returns 404 AND web scraping fails_
    - _Expected_Behavior: search_and_learn(input) returns success status with learned content from fallback sources_
    - _Preservation: Valid learning topics (Python, AI, programming) continue to work exactly as before_
    - _Requirements: 1.1, 1.2, 2.1, 2.2, 3.3, 3.4_

  - [ ] 3.2 Fix Ultimate Learner - Add graceful degradation and partial results
    - Modify `learn_everything()` to accept partial results instead of requiring all sources to succeed
    - Change logic from "if learned_content: return success else: return error" to "if ANY content learned: return success with partial results"
    - Add `_get_builtin_knowledge(topic)` method as last resort fallback
    - Wrap each learning source in try-except to continue to next source if one fails
    - Add minimum content check: provide basic information from topic name analysis if all sources fail
    - Add warning messages for failed sources but still return success
    - _Bug_Condition: isBugCondition_UltimateLearner(input) where Wikipedia OR Google fails AND learned_content is empty_
    - _Expected_Behavior: learn_everything(input) returns success with partial results even if some sources fail_
    - _Preservation: Valid learning topics continue to work exactly as before_
    - _Requirements: 1.3, 1.4, 2.3, 2.4, 3.3, 3.4_

  - [ ] 3.3 Fix Auto Learner - Correct method call in jarvis_offline_brain.py
    - Change line 336 from `self.auto_learner.learn_word_by_word(topic)` to `self.auto_learner.auto_learn_everything(topic)`
    - Update comments that reference the old method name
    - Verify auto_learn_everything method exists in jarvis_auto_learner.py
    - _Bug_Condition: isBugCondition_AutoLearner(input) where 'auto learn' IN input AND jarvis_offline_brain calls learn_word_by_word(topic) instead of auto_learn_everything(topic)_
    - _Expected_Behavior: Auto learner processes topic-based learning without TypeError_
    - _Preservation: All other learning commands and auto learner functionality remain unchanged_
    - _Requirements: 1.7, 2.7, 3.3, 3.4_

  - [ ] 3.4 Fix Autonomous System - Add missing execute_autonomous_task method
    - Add `execute_autonomous_task(user_input)` method to AutonomousSystem class in jarvis_autonomous_system.py
    - Parse user_input to determine which autonomous capability to use
    - Dispatch to appropriate methods: start_chrome_autonomous, auto_navigate_website, collect_data_from_page, etc.
    - Return structured response similar to other learning systems
    - Add `_show_autonomous_help()` method for default case
    - _Bug_Condition: isBugCondition_AutonomousSystem(input) where autonomous keywords IN input AND AutonomousSystem class does NOT have execute_autonomous_task method_
    - _Expected_Behavior: execute_autonomous_task method exists and processes autonomous learning tasks without AttributeError_
    - _Preservation: All other autonomous system methods and functionality remain unchanged_
    - _Requirements: 1.5, 1.6, 2.5, 2.6, 3.5, 3.6_

  - [ ] 3.5 Fix URL Detection - Add URL detection before calculation check
    - Add `_is_url(text)` helper method to jarvis_offline_brain.py that checks for URL patterns (http://, https://, www., .com/.org/.net/.edu/.gov/.io/.co)
    - Add `learn_from_url(url)` method that extracts domain name and uses Internet Learner
    - Move URL detection to happen BEFORE line 178 (calculation check)
    - Insert URL detection logic before calculation check: if _is_url(user_input): return learn_from_url(user_input)
    - Update calculation check to be more specific: ensure "/" is used in mathematical context, not URL context
    - _Bug_Condition: isBugCondition_URLCalculation(input) where input matches URL pattern AND contains "/" AND calculation check triggers before URL detection_
    - _Expected_Behavior: URLs are detected and trigger learning functionality BEFORE calculation check_
    - _Preservation: Valid mathematical expressions with +, -, *, / continue to work exactly as before_
    - _Requirements: 1.8, 1.9, 1.10, 2.8, 2.9, 2.10, 3.1, 3.2_

  - [ ] 3.6 Verify bug condition exploration tests now pass
    - **Property 1: Expected Behavior** - Learning Systems Fixed
    - **IMPORTANT**: Re-run the SAME tests from task 1 - do NOT write new tests
    - The tests from task 1 encode the expected behavior
    - When these tests pass, it confirms the expected behavior is satisfied
    - Run all 5 bug condition exploration tests from step 1
    - **EXPECTED OUTCOME**: All tests PASS (confirms all bugs are fixed)
    - Verify Internet Learner handles website names successfully
    - Verify Ultimate Learner returns partial results when some sources fail
    - Verify Auto Learner uses correct method call
    - Verify Autonomous System has execute_autonomous_task method
    - Verify URLs are detected before calculation check
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10_

  - [ ] 3.7 Verify preservation tests still pass
    - **Property 2: Preservation** - No Regressions
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run all preservation property tests from step 2
    - **EXPECTED OUTCOME**: All tests PASS (confirms no regressions)
    - Verify calculation system works for valid mathematical expressions
    - Verify valid learning topics continue to work
    - Verify other commands (open chrome, search, create file, etc.) work
    - Verify questions and general conversation work
    - Confirm all tests still pass after fix (no regressions)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

---

## Phase 4: Final Validation

- [ ] 4. Checkpoint - Ensure all tests pass and all learning systems work
  - Run complete test suite (bug condition tests + preservation tests)
  - Verify all 4 learning systems work correctly:
    - Internet Learner handles website names (youtube, facebook, etc.)
    - Ultimate Learner returns partial results and doesn't fail completely
    - Auto Learner uses correct method call (auto_learn_everything)
    - Autonomous System has execute_autonomous_task method
    - URLs are detected before calculation check
  - Verify preservation:
    - Calculations work correctly (2+2, 10*5, etc.)
    - Valid learning topics work (Python, AI, programming)
    - Other commands work (open chrome, search, create file)
    - Questions work correctly
  - Test edge cases:
    - URLs with calculations in query params
    - Domains with numbers
    - Mixed learning commands
  - Ask user if questions arise or if additional testing is needed
  - _Requirements: All (1.1-1.10, 2.1-2.10, 3.1-3.6)_

---

## Notes

- **Bug Condition Methodology**: This plan uses C(X) for bug conditions, P(result) for expected properties, ¬C(X) for preservation
- **Test-First Approach**: Write tests BEFORE implementing fixes to understand the bugs
- **Property-Based Testing**: Use PBT for stronger preservation guarantees across input domains
- **Observation-First**: Observe unfixed code behavior before writing preservation tests
- **Scoped PBT**: For deterministic bugs, scope properties to concrete failing cases for reproducibility
- **Files Modified**: jarvis_internet_learner.py, jarvis_ultimate_learner.py, jarvis_offline_brain.py, jarvis_autonomous_system.py, jarvis_auto_learner.py (verification only)
