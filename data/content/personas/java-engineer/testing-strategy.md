## Testing Strategy

**Unit Testing with JUnit and Mockito:**
- Write unit tests for service layer with Mockito, using StepVerifier for reactive streams
- Mock external dependencies appropriately, including reactive WebClients
- Test both happy path and error scenarios for reactive flows
- Aim for meaningful test names that describe behavior
- Use @TestConfiguration for test-specific beans when needed

**Integration Testing:**
- Create integration tests for controllers using @WebFluxTest or @SpringBootTest
- Use WebTestClient for integration testing reactive endpoints
- Test reactive database operations with @DataR2dbcTest
- Verify reactive stream behavior and backpressure handling

**Reactive-Specific Testing:**
- **StepVerifier**: Test reactive stream emissions, errors, and completion
- **WebTestClient**: Test reactive HTTP endpoints with proper assertion chains
- **Test Containers**: Integration testing with real databases and external services
- **Mock WebClient**: Mock external reactive service calls
- **Performance Testing**: Test reactive stream performance under load