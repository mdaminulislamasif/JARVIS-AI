# Implementation Plan

## Phase 1: Exploratory Testing (Before Fix)

- [ ] 1. Write bug condition exploration test
  - **Property 1: Bug Condition** - Network Failure Handling Without Retry
  - **CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
  - **DO NOT attempt to fix the test or the code when it fails**
  - **NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
  - **GOAL**: Surface counterexamples that demonstrate the bug exists
  - **Scoped PBT Approach**: For deterministic bugs, scope the property to the concrete failing case(s) to ensure reproducibility
  - Test implementation details from Bug Condition in design:
    - Mock `requests.get()` to raise `requests.exceptions.Timeout` for Wikipedia API calls
    - Mock `requests.get()` to raise `requests.exceptions.ConnectionError` for Google search
    - Mock `requests.get()` to return HTTP 500 status code
    - Mock `_search_word()` to return None in Auto Learner
    - Mock Wikipedia to succeed, Google to fail (timeout), Programming sites to fail (404) in Ultimate Learner
  - The test assertions should match the Expected Behavior Properties from design:
    - Systems should retry with exponential backoff (1s, 2s, 4s delays)
    - Systems should validate None values before processing
    - Ultimate Learner should return partial results when some sources succeed
    - Systems should provide detailed error messages with troubleshooting suggestions
    - Auto Learner should not crash on None values
  - Run test on UNFIXED code
  - **EXPECTED OUTCOME**: Test FAILS (this is correct - it proves the bug exists)
  - Document counterexamples found to understand root cause:
    - Internet Learner returns error without retry attempts
    - Ultimate Learner discards partial results and returns error
    - Auto Learner crashes with "NoneType: None" error
    - No exponential backoff observed
    - Generic error messages without troubleshooting info
  - Mark task complete when test is written, run, and failure is documented
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Successful Learning Behavior Unchanged
  - **IMPORTANT**: Follow observation-first methodology
  - Observe behavior on UNFIXED code for non-buggy inputs:
    - Mock Wikipedia API to return valid content (status 200 with 'extract' field)
    - Mock all sources (Wikipedia, Google, Programming) to succeed with valid data
    - Mock `_search_word()` to return valid content for all words
    - Observe that unfixed code saves content to database correctly
    - Observe that unfixed code returns success response with proper formatting
    - Observe that unfixed code creates database tables and folders without errors
  - Write property-based tests capturing observed behavior patterns from Preservation Requirements:
    - For all successful Wikipedia API calls, system saves to knowledge base and returns success
    - For all successful multi-source learning, system saves all content with proper categorization
    - For all successful word-by-word learning, system saves to files and database
    - Database operations (initialization, table creation, content saving) work correctly
    - Success response format and structure remain unchanged
  - Property-based testing generates many test cases for stronger guarantees
  - Run tests on UNFIXED code
  - **EXPECTED OUTCOME**: Tests PASS (this confirms baseline behavior to preserve)
  - Mark task complete when tests are written, run, and passing on unfixed code
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

## Phase 2: Implementation

- [ ] 3. Fix for Learning System Failures

  - [ ] 3.1 Add retry helper method to all three learning systems
    - Create `_retry_request(url, headers=None, max_retries=3)` method in InternetLearner class
    - Implement exponential backoff with delays: 1s, 2s, 4s between retries
    - Catch `requests.exceptions.RequestException` and retry on failure
    - Log each retry attempt with reason for failure
    - Return response object or None after all retries exhausted
    - Copy the same `_retry_request()` method to UltimateLearner class
    - Copy the same `_retry_request()` method to AutoLearner class
    - _Bug_Condition: isBugCondition(input) where networkRequestFails(input.topic) OR apiReturnsNone(input.topic) OR httpErrorOccurs(input.topic)_
    - _Expected_Behavior: Systems retry with exponential backoff (1s, 2s, 4s), validate None values, return partial results when available, provide detailed error messages_
    - _Preservation: Successful learning operations (when network succeeds) remain unchanged_
    - _Requirements: 2.1, 2.4_

  - [ ] 3.2 Update InternetLearner network requests to use retry logic
    - In `_learn_from_wikipedia()`: Replace `response = requests.get(url, timeout=10)` with `response = self._retry_request(url)`
    - Add None check: `if response is None: return None`
    - In `_learn_from_web()`: Replace `response = requests.get(search_url, headers=headers, timeout=10)` with `response = self._retry_request(search_url, headers=headers)`
    - Add None check: `if response is None: return None`
    - Keep existing logic for parsing JSON and HTML responses
    - _Bug_Condition: Network requests fail without retry attempts_
    - _Expected_Behavior: Retry up to 3 times with exponential backoff before returning None_
    - _Preservation: Successful Wikipedia and web learning behavior unchanged_
    - _Requirements: 2.1, 2.4, 3.1_

  - [ ] 3.3 Enhance InternetLearner error messages with troubleshooting
    - In `search_and_learn()`: Update error message when both Wikipedia and web search fail
    - Change from: `"❌ Could not learn about '{topic}' from internet"`
    - Change to: `"❌ Could not learn about '{topic}' from internet after 3 retry attempts.\n\nTroubleshooting:\n1. Check your internet connection\n2. Verify the topic spelling\n3. Try a different topic\n4. Check if Wikipedia and Google are accessible from your network"`
    - Include information about which sources were attempted and why they failed
    - _Bug_Condition: Generic error messages without actionable information_
    - _Expected_Behavior: Detailed error messages with troubleshooting suggestions_
    - _Preservation: Success response format unchanged_
    - _Requirements: 2.1_

  - [ ] 3.4 Update UltimateLearner network requests to use retry logic
    - In `_learn_from_wikipedia()`: Replace `response = requests.get(url, timeout=10)` with `response = self._retry_request(url)`
    - Add None check: `if response is None: return None`
    - In `_learn_from_google()`: Replace `response = requests.get(search_url, headers=headers, timeout=10)` with `response = self._retry_request(search_url, headers=headers)`
    - Add None check: `if response is None: return None`
    - In `_learn_programming()`: Replace `response = requests.get(so_url, headers=headers, timeout=10)` with `response = self._retry_request(so_url, headers=headers)`
    - Add None check: `if response is None: return None`
    - _Bug_Condition: Network requests fail without retry attempts_
    - _Expected_Behavior: Retry up to 3 times with exponential backoff before returning None_
    - _Preservation: Successful multi-source learning behavior unchanged_
    - _Requirements: 2.1, 2.4, 3.2_

  - [ ] 3.5 Implement partial results handling in UltimateLearner
    - In `learn_everything()`: After attempting all sources, check `if learned_content:` (if any sources succeeded)
    - Track success/failure status for each source: `wiki_status`, `google_status`, `prog_status`
    - If partial success (some sources succeeded), return:
      ```python
      {
          'status': 'partial_success',
          'response': f"✅ Learned from {len(learned_content)}/{total_sources} sources.\n\nWikipedia: {wiki_status}\nGoogle: {google_status}\nProgramming: {prog_status}\n\nPartial results saved to JARVIS memory!",
          'type': 'ultimate_learning',
          'sources': len(learned_content),
          'words': total_words
      }
      ```
    - Save partial results to database even if not all sources succeeded
    - Only return error if `learned_content` is completely empty (all sources failed)
    - _Bug_Condition: Partial results discarded when any source fails_
    - _Expected_Behavior: Return partial results when some sources succeed_
    - _Preservation: Behavior when all sources succeed remains unchanged_
    - _Requirements: 2.2, 3.2_

  - [ ] 3.6 Add None validation to AutoLearner `_search_word()` method
    - Ensure method always returns None or valid string (never undefined)
    - Add explicit `return None` at end of method if no content found
    - Add None checks before returning data: `if data and 'extract' in data: return data['extract']`
    - Add None check for Google search result: `if featured: return featured.get_text()`
    - Ensure all code paths return either valid string or None
    - _Bug_Condition: Method returns None causing crashes in calling code_
    - _Expected_Behavior: Method explicitly returns None when no content found_
    - _Preservation: Successful word search behavior unchanged_
    - _Requirements: 2.3, 2.5, 3.3_

  - [ ] 3.7 Add None validation to AutoLearner `learn_word_by_word()` method
    - After `result = self._search_word(clean_word)`, add None check
    - Change from: `result = self._search_word(clean_word)`
    - Change to:
      ```python
      result = self._search_word(clean_word)
      if result is None:
          print(f"⚠️ Could not learn word: {clean_word}")
          continue
      ```
    - Only append to `learned_words` if result is not None
    - Continue processing remaining words even if some return None
    - _Bug_Condition: Code attempts to process None values causing crashes_
    - _Expected_Behavior: Check for None and skip with warning message_
    - _Preservation: Successful word-by-word learning unchanged_
    - _Requirements: 2.3, 2.5, 3.3_

  - [ ] 3.8 Add None validation to AutoLearner `auto_learn_everything()` method
    - After `wiki_content = self._learn_from_wikipedia(topic)`, add check: `if wiki_content is not None:`
    - After `google_content = self._learn_from_google(topic)`, add check: `if google_content is not None:`
    - After `prog_content = self._learn_programming(topic)`, add check: `if prog_content is not None:`
    - In word-by-word learning loop, add check: `if result is not None:` before appending to `all_content`
    - Only process and save content when it's not None
    - _Bug_Condition: Code attempts to process None values causing crashes_
    - _Expected_Behavior: Validate all return values before processing_
    - _Preservation: Successful auto learning behavior unchanged_
    - _Requirements: 2.3, 2.5, 3.3_

  - [ ] 3.9 Update AutoLearner network requests to use retry logic
    - In `_learn_from_wikipedia()`: Replace `response = requests.get(url, timeout=10)` with `response = self._retry_request(url)`
    - Add None check: `if response is None: return None`
    - In `_learn_from_google()`: Replace `response = requests.get(search_url, headers=headers, timeout=10)` with `response = self._retry_request(search_url, headers=headers)`
    - Add None check: `if response is None: return None`
    - In `_learn_programming()`: Replace `response = requests.get(so_url, headers=headers, timeout=10)` with `response = self._retry_request(so_url, headers=headers)`
    - Add None check: `if response is None: return None`
    - In `_search_word()`: Replace `response = requests.get(url, timeout=5)` with `response = self._retry_request(url)`
    - Replace `response = requests.get(search_url, headers=headers, timeout=5)` with `response = self._retry_request(search_url, headers=headers)`
    - _Bug_Condition: Network requests fail without retry attempts_
    - _Expected_Behavior: Retry up to 3 times with exponential backoff before returning None_
    - _Preservation: Successful auto learning behavior unchanged_
    - _Requirements: 2.1, 2.4, 3.3_

  - [ ] 3.10 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - Graceful Failure Handling with Retry Logic
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior
    - When this test passes, it confirms the expected behavior is satisfied
    - Run bug condition exploration test from step 1
    - **EXPECTED OUTCOME**: Test PASSES (confirms bug is fixed)
    - Verify all assertions pass:
      - Systems retry with exponential backoff (1s, 2s, 4s delays)
      - Systems validate None values before processing
      - Ultimate Learner returns partial results when some sources succeed
      - Systems provide detailed error messages with troubleshooting suggestions
      - Auto Learner does not crash on None values
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ] 3.11 Verify preservation tests still pass
    - **Property 2: Preservation** - Successful Learning Behavior Unchanged
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run preservation property tests from step 2
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions)
    - Verify all preservation properties still hold:
      - Successful Wikipedia learning saves to knowledge base and returns success
      - Successful multi-source learning saves all content with proper categorization
      - Successful word-by-word learning saves to files and database
      - Database operations work correctly
      - Success response format unchanged
    - Confirm all tests still pass after fix (no regressions)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 4. Checkpoint - Ensure all tests pass
  - Run all exploration tests (Property 1) - should now PASS
  - Run all preservation tests (Property 2) - should still PASS
  - Verify no regressions in existing functionality
  - Test with real network failures (disconnect internet, use invalid URLs)
  - Test with successful learning operations (verify unchanged behavior)
  - If any tests fail, investigate and fix before proceeding
  - Ask the user if questions arise

## Notes

- **Test Execution Order**: Tasks 1 and 2 MUST be completed BEFORE task 3 (implementation)
- **Property-Based Testing**: Use property-based testing framework (e.g., Hypothesis for Python) for stronger guarantees
- **Mocking**: Use `unittest.mock` or `pytest-mock` to simulate network failures and None returns
- **Exponential Backoff**: Verify delays are approximately 1s, 2s, 4s (allow small timing variations)
- **Partial Results**: Ultimate Learner should save and return partial results even when some sources fail
- **None Validation**: All return values from network requests and API calls must be checked for None before processing
- **Error Messages**: Include actionable troubleshooting information in all error messages
- **Preservation**: All successful learning operations must remain completely unchanged by this fix
