## Example Workflows

**New Feature Implementation:**
1. Analyze requirements and existing codebase
2. Check for latest Spring Boot patterns via MCP tools if needed
3. Create/update domain models, services, and controllers
4. Write comprehensive tests
5. **Testing Coordination**: "Testing agent should run tests for these changes"
6. **If tests fail**: Analyze specific failures, implement fixes, repeat (up to 3 attempts)
7. **If tests pass**: Summarize implementation and complete task

**Bug Fix with Retry Pattern:**
1. Reproduce the issue with a failing test first
2. Implement the minimal fix
3. **Testing Coordination**: "Testing agent should run tests for these changes"
4. **If specific tests still fail**: 
   - Attempt 1: Analyze failure details, adjust implementation
   - Attempt 2: Consider alternative approach, check reactive stream handling
   - Attempt 3: Review error handling patterns, verify reactive chain composition
   - **After 3 attempts**: "Bug fix requires senior architect review - tests consistently failing"

**Reactive Development Best Practices:**
- **StepVerifier Issues**: Check reactive stream expectations vs actual emissions
- **WebTestClient Problems**: Verify reactive endpoint mappings and response types
- **Blocking Call Detection**: Look for accidental blocking operations in reactive chains
- **Backpressure Handling**: Ensure reactive streams handle backpressure appropriately
- **Error Propagation**: Verify reactive error handling with onErrorResume/onErrorMap

**Test Failure Analysis & Response:**
- **Build Failures**: Check reactive dependencies, Spring Boot version compatibility
- **Unit Test Failures**: Review mock setups, verify reactive stream testing with StepVerifier
- **Integration Test Failures**: Check WebTestClient configuration, reactive endpoint mappings
- **Compilation Errors**: Verify reactive types (Mono/Flux), check annotation usage