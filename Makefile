.PHONY: help build-agents build-claude build test install clean

# Default target
help:
	@echo "Claude Config Generator - Available Commands:"
	@echo ""
	@echo "  build-agents Build agent configurations from YAML files"
	@echo "  build-claude Build global CLAUDE.md configuration file"
	@echo "  build        Build both agents and global CLAUDE.md"
	@echo "  test         Run test suite"
	@echo "  install      Install built configurations to ~/.claude/ (clean install by default)"
	@echo "  clean        Clean build artifacts"
	@echo "  help         Show this help message"

# Build agent configurations
build-agents:
	@echo "🔨 Building agent configurations..."
	uv run claude-config build-agents --validate
	@echo "✅ Agent configurations built successfully!"

# Build global CLAUDE.md configuration
build-claude:
	@echo "🌍 Building global CLAUDE.md configuration..."
	uv run claude-config build-claude
	@echo "✅ Global CLAUDE.md built successfully!"

# Build everything
build: build-agents build-claude
	@echo "✅ All configurations built successfully!"

# Run tests
test:
	@echo "🧪 Running tests..."
	uv run pytest -v --cov=claude_config --cov-report=term-missing

# Install to Claude Code directory
install: build
	@echo "📦 Installing to ~/.claude/..."
	uv run claude-config install
	@echo "✅ Installed to ~/.claude/"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .mypy_cache/
	rm -rf src/claude_config/__pycache__/
	rm -rf tests/__pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "✅ Clean complete!"