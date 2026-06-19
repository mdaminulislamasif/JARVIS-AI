# Implementation Plan

## Overview

This task list implements the fix for the Jarvis greeting response bug using the bug condition methodology. The workflow follows an exploratory approach: write tests BEFORE the fix to understand the bug, then implement the fix with confidence.

## Task Sequence

- [ ] 1. Write bug condition exploration test
  - **Property 1: Bug Condition** - Greeting Detection and Immediate Response
  - **CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
  - **DO NOT attempt to fix the test or the code when it fails**
  - **NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
  - **GOAL**: Surface counterexamples that demonstrate the bug exists
  - **Scoped PBT Approach**: Scope the property to concrete failing cases: greeting inputs ("hello", "hi", "hey") with various casing and context
  - Test that greeting inputs ("Hello", "Hi", "Hey", "hello jarvis", "HELLO", "hi there") receive immediate responses without AI brain routing
  - Assert response time < 100ms
  - Assert no API call is made to AI brain
  - Assert response contains greeting message
  - Assert response is logged to chat history
  - Run test on UNFIXED code
  - **EXPECTED OUTCOME**: Test FAILS (this is correct - it proves the bug exists)
  - Document counterexamples found (e.g., "Hello routes to AI brain instead of immediate response", "Response time exceeds 100ms due to AI brain processing")
  - Mark task complete when test is written, run, and failure is documented
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_

- [ ] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Non-Greeting Input Behavior
  - **IMPORTANT**: Follow observation-first methodology
  - Observe behavior on UNFIXED code for non-greeting inputs:
    - Direct commands: "screenshot", "workspace", "clean" execute directly
    - Complex queries: "What is the weather?" routes to AI brain
    - Agent mode: commands route through agent handler when agent_mode is active
    - Specialized commands: "learn", "translate", "search" route to specialized handlers
  - Write property-based tests capturing observed behavior patterns:
    - For all direct command inputs, verify they execute directly (not routed to AI brain)
    - For all complex query inputs (non-greetings, non-commands), verify they route to AI brain
    - For all inputs when agent_mode is active, verify they route through agent handler
    - For all specialized command inputs, verify they route to specialized handlers
  - Property-based testing generates many test cases for stronger guarantees
  - Run tests on UNFIXED code
  - **EXPECTED OUTCOME**: Tests PASS (this confirms baseline behavior to preserve)
  - Mark task complete when tests are written, run, and passing on unfixed code
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

- [ ] 3. Fix for greeting response routing

  - [ ] 3.1 Implement greeting detection logic in jarvis_panel.py
    - Open `jarvis_panel.py` and locate the `process()` method (line 1291)
    - Insert greeting detection logic AFTER direct command routing (after line 1320) and BEFORE AI brain routing
    - Define greeting keywords: `greeting_keywords = ["hello", "hi", "hey"]`
    - Implement case-insensitive detection: `query_lower = query.strip().lower()`
    - Check if any greeting keyword is in the query: `any(keyword in query_lower for keyword in greeting_keywords)`
    - _Bug_Condition: isBugCondition(input) where input contains "hello", "hi", or "hey" (case-insensitive) and is not a direct command_
    - _Expected_Behavior: Immediate response within 100ms without AI brain or API key, response logged and spoken_
    - _Preservation: All existing routing logic (direct commands, AI brain queries, agent mode, offline brain fallback) must remain unchanged_
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [ ] 3.2 Implement greeting response generation
    - Create logic to generate appropriate greeting responses
    - Check if user's name is available (from config or previous interactions)
    - If name is known: Generate personalized greeting "Hello [Name]! How can I assist you today?"
    - If name is unknown: Generate generic greeting "Hello! I'm Jarvis. How can I help you?"
    - Support Bengali responses if `self.prefer_bangla_voice` is True:
      - Bengali greeting: "হ্যালো! আমি জার্ভিস। আমি কিভাবে সাহায্য করতে পারি?"
      - Bengali personalized: "হ্যালো [Name]! আমি আপনাকে কিভাবে সাহায্য করতে পারি?"
    - _Requirements: 2.5, 2.6, 2.7_

  - [ ] 3.3 Implement early return for greeting responses
    - When greeting is detected, set `res` variable to the greeting response
    - Log the response: `self.after(0, lambda: self.log("JARVIS", res))`
    - Save to chat history: `save_chat(query, res)`
    - Speak the response: `self.voice.speak(res)`
    - Set state back to idle: `self.state = "idle"`
    - Return immediately to prevent AI brain routing
    - Ensure response completes within 100ms (no external API calls)
    - _Requirements: 2.4, 2.5, 2.6, 2.7_

  - [ ] 3.4 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - Greeting Detection and Immediate Response
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior
    - When this test passes, it confirms the expected behavior is satisfied
    - Run bug condition exploration test from step 1
    - **EXPECTED OUTCOME**: Test PASSES (confirms bug is fixed)
    - Verify greeting inputs receive immediate responses
    - Verify response time < 100ms
    - Verify no AI brain calls are made
    - Verify responses are logged and spoken
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

  - [ ] 3.5 Verify preservation tests still pass
    - **Property 2: Preservation** - Non-Greeting Input Behavior
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run preservation property tests from step 2
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions)
    - Verify direct commands still execute directly
    - Verify complex queries still route to AI brain
    - Verify agent mode routing still works
    - Verify specialized command routing still works
    - Confirm all tests still pass after fix (no regressions)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

- [ ] 4. Checkpoint - Ensure all tests pass
  - Run all tests (bug condition + preservation)
  - Verify all tests pass
  - Verify greeting responses work in both English and Bengali
  - Verify response times are under 100ms
  - Verify no regressions in existing functionality
  - Ask the user if questions arise

## Notes

- **Test-First Approach**: Tasks 1 and 2 write tests BEFORE implementing the fix
- **Exploration**: Task 1 test will FAIL on unfixed code - this is expected and confirms the bug
- **Preservation**: Task 2 tests will PASS on unfixed code - this captures baseline behavior
- **Implementation**: Task 3 implements the fix with confidence from understanding gained in tasks 1-2
- **Validation**: Tasks 3.4 and 3.5 re-run the same tests to verify the fix works and preserves existing behavior
