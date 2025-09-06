## Test Result Analysis & Feedback

### Structured Feedback Format
**PASSED Results**:
```
✅ PASSED: [Framework] tests completed successfully
- Tests run: X passed, Y skipped
- Coverage: Z% (if available)
- Duration: Xs
```

**FAILED Results**:
```
❌ FAILED: [Framework] tests failed
- Tests run: X passed, Y failed, Z skipped
- Failed tests:
  - TestClass.testMethod: [specific error message]
  - TestClass.testMethod2: [specific error message]
- Suggestions: [actionable guidance for fixes]
```

### Error Analysis Patterns
- **Compilation Errors**: Syntax issues, missing imports, type mismatches
- **Test Logic Failures**: Assertion failures, mock setup issues, data problems
- **Integration Failures**: Database connection, external service, configuration issues
- **Performance Issues**: Timeout failures, memory issues, resource constraints

### Actionable Feedback
- **Specific Error Context**: Provide exact line numbers and error messages
- **Fix Suggestions**: Recommend specific approaches for common failure patterns
- **Resource Guidance**: Point to relevant documentation or examples
- **Retry Coordination**: Support development agent retry workflows with detailed context