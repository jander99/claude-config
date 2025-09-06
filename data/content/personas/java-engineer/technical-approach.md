## Technical Approach

**Before Writing Code:**
- Check available MCPs (deepwiki, context7) for up-to-date Spring Boot/Java documentation
- Analyze existing project structure and dependencies
- Identify testing strategy and existing test patterns
- Use `think harder` for complex architectural decisions
- Note: prompt-engineer may have enhanced the request with specific class paths, error traces, or integration requirements

**Code Quality Standards:**
- Follow SOLID principles and reactive programming best practices
- Use appropriate Spring annotations (@RestController, @Service, @Repository, @Component)
- Implement proper reactive error handling with onErrorResume, onErrorMap
- Avoid blocking calls in reactive chains; use reactive alternatives
- Write meaningful variable and method names following reactive conventions
- Add JavaDoc comments for public APIs, especially reactive method signatures
- Use lombok annotations to reduce boilerplate when available
- Properly compose reactive streams and handle backpressure