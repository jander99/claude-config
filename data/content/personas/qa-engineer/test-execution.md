## Test Execution Strategy

### Go Projects  
**Detection**: Look for `go.mod`
**Test Execution**:
- Primary: `go test ./...`
- With coverage: `go test -cover ./...`
- Verbose: `go test -v ./...`
- Specific package: `go test ./path/to/package`

### Rust Projects
**Detection**: Look for `Cargo.toml`
**Test Execution**:
- Primary: `cargo test`
- With output: `cargo test -- --nocapture`
- Specific test: `cargo test test_name`

### Multi-Language Support
- **Auto-Detection**: Analyze project structure to identify primary language and testing framework
- **Framework-Specific**: Use appropriate test runners and assertion patterns
- **Result Parsing**: Parse language-specific test output formats
- **Coverage Integration**: Support coverage reporting across different languages
- **Parallel Testing**: Execute tests efficiently with proper resource management