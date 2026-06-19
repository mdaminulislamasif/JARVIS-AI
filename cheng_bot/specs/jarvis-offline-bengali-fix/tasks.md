# Implementation Plan

## Overview
This task list implements the bugfix for JARVIS offline Bengali command understanding using the bug condition methodology. The implementation follows a test-first approach: write exploration tests to understand the bug, write preservation tests to protect existing behavior, then implement the fix.

---

## Tasks

- [ ] 1. Write bug condition exploration test
  - **Property 1: Bug Condition** - Bengali Software Creation Commands Not Recognized
  - **CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
  - **DO NOT attempt to fix the test or the code when it fails**
  - **NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
  - **GOAL**: Surface counterexamples that demonstrate the bug exists
  - **Scoped PBT Approach**: For deterministic bugs, scope the property to the concrete failing case(s) to ensure reproducibility
  - Test implementation details from Bug Condition in design:
    - Test case 1: Input "jarvis amr jonno akta phone call aplition toiri koro" should invoke SuperBrain (currently shows generic help)
    - Test case 2: Input "jarvis amr free fire pac panql hack lqgba" should invoke SuperBrain (currently shows generic help)
    - Test case 3: Input "create game panal software" should recognize "panal" as "panel" (currently fails)
    - Test case 4: Input "jarvis calculator toiri koro" should detect Bengali creation intent (currently fails)
    - Test case 5: Input "make phone call aplition" should fuzzy match "aplition" to "application" (currently fails)
  - The test assertions should match the Expected Behavior Properties from design:
    - Assert software creation intent is detected
    - Assert SuperBrain is invoked with correct software description
    - Assert NOT generic help response
    - Assert fuzzy matching corrects misspellings
    - Assert Bengali language detection works
  - Run test on UNFIXED code (jarvis_offline_brain.py)
  - **EXPECTED OUTCOME**: Test FAILS (this is correct - it proves the bug exists)
  - Document counterexamples found to understand root cause:
    - Which Bengali words are not recognized?
    - Which misspellings are not handled?
    - What is the actual response vs expected response?
  - Mark task complete when test is written, run, and failure is documented
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8_

- [ ] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Non-Bengali Command Behavior Unchanged
  - **IMPORTANT**: Follow observation-first methodology
  - Observe behavior on UNFIXED code for non-buggy inputs (existing English commands)
  - Write property-based tests capturing observed behavior patterns from Preservation Requirements:
    - Test English software creation: "create calculator software" routes to software creation handler
    - Test calculation commands: "2+2", "calculate 10 * 5" route to calculation handler
    - Test search commands: "search Python", "search youtube tutorial" route to search handler
    - Test application opening: "open chrome", "open notepad" route to application opener
    - Test file operations: "create file test.txt", "list files" route to file operation handlers
    - Test learning commands: "learn from internet Python" routes to learning system
    - Test website builder: "build website" routes to website builder
    - Test autonomous system: commands with "autonomous", "admin", "privilege" route to autonomous system
    - Test help command: "help" displays comprehensive help menu
    - Test greetings: "hello jarvis", "hi jarvis" respond with smart greetings
    - Test questions: "what is Python?" attempts to answer using knowledge base
    - Test SuperBrain unavailability: graceful handling when SuperBrain is not available
  - Property-based testing generates many test cases for stronger guarantees
  - Run tests on UNFIXED code
  - **EXPECTED OUTCOME**: Tests PASS (this confirms baseline behavior to preserve)
  - Mark task complete when tests are written, run, and passing on unfixed code
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12_

- [ ] 3. Fix for JARVIS Offline Bengali Command Understanding

  - [ ] 3.1 Add Enhanced Bengali Language Detection Module
    - Create comprehensive Bengali word dictionary with all variations
    - Include Bengali script words: 'বানাও', 'তৈরি', 'বানা', 'বানিয়ে', 'আমার', 'জন্য', 'চাই', 'একটা'
    - Include romanized Bengali words: 'toiri', 'tiri', 'banao', 'tairi', 'korta', 'korbo', 'koro', 'bana', 'baniye'
    - Include Bengali intent modifiers: 'amr', 'amar', 'jonno', 'lqgba', 'lagba', 'chai', 'akta'
    - Implement `detect_bengali_language(command: str) -> bool` function
    - Function should check if any Bengali word exists in command (case-insensitive)
    - _Bug_Condition: isBugCondition(input) where containsBengaliWords(input) returns True_
    - _Expected_Behavior: System SHALL detect Bengali language and recognize comprehensive word variations (Req 2.4, 2.5, 2.10)_
    - _Preservation: No impact on English-only commands_
    - _Requirements: 2.4, 2.5, 2.10_

  - [ ] 3.2 Add Fuzzy Matching System
    - Implement fuzzy string matching for common misspellings
    - Create misspelling mapping dictionary:
      - 'aplition' → 'application'
      - 'panal' → 'panel'
      - 'panql' → 'panel'
      - 'pac' → 'pack'
      - 'softwer' → 'software'
      - 'calculater' → 'calculator'
      - 'hak' → 'hack'
    - Implement `fuzzy_match_software_terms(command: str) -> str` function
    - Function should replace misspellings with correct terms (case-insensitive)
    - Handle both lowercase and capitalized versions
    - _Bug_Condition: isBugCondition(input) where containsMisspelledSoftwareTerms(input) returns True_
    - _Expected_Behavior: System SHALL use fuzzy matching to recognize misspellings (Req 2.2)_
    - _Preservation: No impact on correctly spelled commands_
    - _Requirements: 2.2_

  - [ ] 3.3 Add Mixed Language Parser
    - Implement tokenization that handles both English and Bengali words
    - Create `parse_mixed_language_command(command: str) -> str` function
    - Extract software type from mixed language input
    - Combine English and Bengali components to understand complete intent
    - Handle commands like "phone call aplition toiri koro" → extract "phone call application"
    - _Bug_Condition: isBugCondition(input) where command contains mixed English-Bengali words_
    - _Expected_Behavior: System SHALL parse both language components and combine them (Req 2.8)_
    - _Preservation: No impact on single-language commands_
    - _Requirements: 2.8_

  - [ ] 3.4 Add Intent Detection System
    - Implement keyword-based intent analysis
    - Create `detect_software_creation_intent(command: str) -> bool` function
    - Check for creation verbs: 'create', 'make', 'build', 'generate', 'develop', 'toiri', 'tiri', 'banao', 'tairi', 'koro', 'korbo', 'korta', 'বানাও', 'তৈরি', 'বানা', 'বানিয়ে'
    - Check for software keywords: 'application', 'app', 'software', 'tool', 'program', 'hack', 'panel', 'pack', 'calculator', 'game', 'website', 'system', 'script', 'utility'
    - Return True if creation verb OR software keyword found
    - Create `extract_software_description(command: str) -> str` function
    - Remove command prefixes: 'jarvis', 'hey jarvis', 'ok jarvis', 'amr jonno', 'amr', 'akta', 'একটা'
    - Remove Bengali creation verbs: 'toiri koro', 'toiri', 'tiri', 'banao', 'tairi', 'koro', 'korbo', 'korta', 'বানাও', 'তৈরি'
    - Remove English creation verbs: 'create', 'make', 'build', 'generate'
    - Return cleaned software description
    - _Bug_Condition: isBugCondition(input) where indicatesSoftwareCreationIntent(input) returns True_
    - _Expected_Behavior: System SHALL detect intent using keyword analysis before falling back to generic response (Req 2.7)_
    - _Preservation: No impact on commands that don't indicate software creation_
    - _Requirements: 2.1, 2.3, 2.7, 2.9_

  - [ ] 3.5 Enhance Software Type Recognition
    - Expand software type detection to include multi-word types
    - Recognize: "phone call application", "free fire hack", "game panel", "pack panel"
    - Recognize common software categories: calculator, notepad, browser, messenger
    - Recognize gaming-related terms: hack, mod, panel, pack, cheat
    - Implement `recognize_software_type(command: str) -> Optional[str]` function
    - Extract multi-word software types from command
    - _Bug_Condition: isBugCondition(input) where command contains multi-word software types_
    - _Expected_Behavior: System SHALL recognize multi-word software types like "phone call application" (Req 2.6)_
    - _Preservation: No impact on single-word software types_
    - _Requirements: 2.6_

  - [ ] 3.6 Add Language-Aware Response System
    - Implement bilingual response generation
    - Create `generate_bilingual_response(message: str, has_bengali: bool) -> str` function
    - If Bengali detected, provide response in both Bengali and English
    - Create Bengali translation mapping for common terms:
      - 'Creating' → 'তৈরি করছি'
      - 'software' → 'সফটওয়্যার'
      - 'application' → 'অ্যাপ্লিকেশন'
      - 'for you' → 'আপনার জন্য'
    - Format: "English message (বাংলা: Bengali translation)"
    - _Bug_Condition: isBugCondition(input) where command contains Bengali words_
    - _Expected_Behavior: System SHALL provide responses in both Bengali and English when Bengali detected (Req 2.10)_
    - _Preservation: English-only commands receive English-only responses_
    - _Requirements: 2.10_

  - [ ] 3.7 Integrate with Existing SuperBrain
    - Route detected software creation requests to SuperBrain
    - Pass extracted software description to SuperBrain.create_software()
    - Include language context parameter: 'bengali' if Bengali detected, 'english' otherwise
    - Handle SuperBrain unavailability gracefully (check if superbrain attribute exists and is not None)
    - Catch exceptions from SuperBrain and return error message
    - Generate bilingual error messages if Bengali detected
    - _Bug_Condition: isBugCondition(input) where software creation intent detected_
    - _Expected_Behavior: System SHALL extract description and pass to SuperBrain with language context (Req 2.9)_
    - _Preservation: SuperBrain unavailability handled gracefully (Req 3.12)_
    - _Requirements: 2.9, 3.12_

  - [ ] 3.8 Modify Command Processing Flow in process_command()
    - Open jarvis_offline_brain.py
    - Locate process_command(self, command: str) -> str method
    - **PRESERVE all existing handlers** (calculation, search, file ops, application opener, learning, website builder, autonomous system, help, greeting, question, existing software creation)
    - **DO NOT modify existing handler logic or order**
    - After all existing handlers, before smart_response() fallback, insert new intent detection layer:
      1. Detect Bengali language using detect_bengali_language(command)
      2. Apply fuzzy matching using fuzzy_match_software_terms(command)
      3. Detect software creation intent using detect_software_creation_intent(corrected_command)
      4. If intent detected:
         - Extract software description using extract_software_description(corrected_command)
         - Check if SuperBrain is available (hasattr and not None)
         - Invoke SuperBrain.create_software(description, language_context)
         - Generate bilingual response using generate_bilingual_response()
         - Return response
      5. If no intent detected, fall back to smart_response()
    - _Bug_Condition: isBugCondition(input) where command fails to match existing handlers_
    - _Expected_Behavior: System SHALL attempt intelligent intent detection before falling back to generic response (Req 2.7)_
    - _Preservation: All existing handlers remain unchanged and execute in same order (Req 3.1-3.12)_
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12_

  - [ ] 3.9 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - Bengali Software Creation Commands Recognized
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior
    - When this test passes, it confirms the expected behavior is satisfied
    - Run bug condition exploration test from step 1
    - Verify all test cases now pass:
      - "jarvis amr jonno akta phone call aplition toiri koro" invokes SuperBrain
      - "jarvis amr free fire pac panql hack lqgba" invokes SuperBrain
      - "create game panal software" recognizes "panal" as "panel"
      - "jarvis calculator toiri koro" detects Bengali creation intent
      - "make phone call aplition" fuzzy matches "aplition" to "application"
    - **EXPECTED OUTCOME**: Test PASSES (confirms bug is fixed)
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10_

  - [ ] 3.10 Verify preservation tests still pass
    - **Property 2: Preservation** - Non-Bengali Command Behavior Unchanged
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run preservation property tests from step 2
    - Verify all existing command handlers still work correctly:
      - English software creation commands work as before
      - Calculation commands route to calculation handler
      - Search commands route to search handler
      - Application opening commands route to application opener
      - File operation commands route to file operation handlers
      - Learning commands route to learning system
      - Website builder commands route to website builder
      - Autonomous system commands route to autonomous system
      - Help command displays help menu
      - Greeting commands respond with smart greetings
      - Question commands attempt to answer using knowledge base
      - SuperBrain unavailability handled gracefully
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions)
    - Confirm all tests still pass after fix (no regressions)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12_

- [ ] 4. Checkpoint - Ensure all tests pass
  - Run all bug condition exploration tests - should PASS
  - Run all preservation property tests - should PASS
  - Run any unit tests for helper functions
  - Verify no regressions in existing functionality
  - Test edge cases:
    - Empty commands
    - Very long commands
    - Commands with special characters
    - Commands mixing Bengali script and romanized Bengali
    - Commands with multiple misspellings
  - If any test fails, debug and fix before marking complete
  - Ask the user if questions arise or if manual testing is needed
  - _Requirements: All (1.1-1.8, 2.1-2.10, 3.1-3.12)_

---

## Notes

- **Test-First Approach**: Tasks 1 and 2 MUST be completed before task 3 (implementation)
- **Property-Based Testing**: Recommended for preservation tests to generate many test cases automatically
- **Observation-First**: Preservation tests should observe behavior on unfixed code first
- **No Modifications to Existing Handlers**: The fix adds new detection capabilities without modifying existing command routing logic
- **Graceful Degradation**: SuperBrain unavailability should be handled without crashing
- **Bilingual Support**: Responses should include both Bengali and English when Bengali detected
- **Fuzzy Matching Threshold**: Use appropriate similarity threshold (e.g., 80%) for misspelling detection
- **Edge Cases**: Test with Bengali script, romanized Bengali, mixed languages, and various misspellings
