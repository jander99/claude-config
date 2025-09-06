## Project Detection & Test Execution

### Java Projects
**Detection**: Look for `build.gradle`, `build.gradle.kts`, or `pom.xml`

**Gradle Projects**:
- Primary: `./gradlew test` (if gradlew exists)
- Fallback: `gradle test`
- For specific tests: `./gradlew test --tests "ClassName.methodName"`
- Reactive testing: Supports JUnit 5, Mockito, StepVerifier

**Maven Projects**:
- Primary: `./mvnw test` (if mvnw exists)  
- Fallback: `mvn test`
- For specific tests: `mvn test -Dtest="ClassName#methodName"`

### Python Projects
**Detection**: Look for `pyproject.toml`, `requirements.txt`, `setup.py`, `pytest.ini`

**Test Execution**:
- Primary: `pytest` (if pytest is detected in dependencies)
- With coverage: `pytest --cov=src --cov-report=term-missing`
- XML output: `pytest --junit-xml=test-results.xml`
- Fallback: `python -m unittest discover`

### JavaScript/TypeScript Projects
**Detection**: Look for `package.json`

**Test Execution**:
- Read `package.json` scripts section for `test` command
- Primary: `npm test` or `yarn test`
- Jest-specific: `npx jest` or `yarn jest`
- With coverage: `npm run test -- --coverage`