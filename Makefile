.PHONY: help build-agents build-claude build-mcp build-mcp-prod build-all build-all-prod build test install install-mcp validate validate-mcp clean clean-mcp list-agents list-mcp dev-setup dev-build prod-build build-dev build-prod

# Default target
help:
	@echo "Claude Config Generator - Available Commands:"
	@echo ""
	@echo "Building:"
	@echo "  build-agents   Build agent configurations from YAML files"
	@echo "  build-claude   Build global CLAUDE.md configuration file"
	@echo "  build-mcp      Build MCP servers JSON configuration (dev)"
	@echo "  build-mcp-prod Build MCP servers JSON configuration (production)"
	@echo "  build-all      Build both agents and MCP servers (dev)"
	@echo "  build-all-prod Build both agents and MCP servers (production)"
	@echo "  build          Build agents and global CLAUDE.md (legacy)"
	@echo ""
	@echo "Environment Builds:"
	@echo "  build-dev      Complete development environment build"
	@echo "  build-prod     Complete production environment build"
	@echo "  dev-build      Quick development cycle (MCP only)"
	@echo "  prod-build     Production ready build (all components)"
	@echo ""
	@echo "Validation:"
	@echo "  validate     Validate all configurations (agents + MCP)"
	@echo "  validate-mcp Validate only MCP server configurations"
	@echo ""
	@echo "Installation:"
	@echo "  install      Install agents and global config to ~/.claude/"
	@echo "  install-mcp  Install MCP servers configuration to ~/.claude/"
	@echo ""
	@echo "Listing:"
	@echo "  list-agents  List available agent personas"
	@echo "  list-mcp     List available MCP server configurations"
	@echo ""
	@echo "Development:"
	@echo "  dev-setup      Set up development environment"
	@echo "  install-dev-deps Install development dependencies"
	@echo ""
	@echo "Maintenance:"
	@echo "  test         Run test suite"
	@echo "  clean        Clean all build artifacts"
	@echo "  clean-mcp    Clean only MCP build artifacts"
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

# Build MCP servers configuration (development)
build-mcp:
	@echo "🔧 Building MCP servers configuration for development..."
	uv run claude-config build-mcp --validate --env dev
	@echo "✅ MCP servers configuration built successfully!"

# Build MCP servers for production
build-mcp-prod:
	@echo "🚀 Building MCP servers configuration for production..."
	uv run claude-config build-mcp --validate --env prod
	@echo "✅ Production MCP servers configuration built successfully!"

# Build everything (development)
build-all: build-agents build-claude build-mcp
	@echo "✅ All configurations (agents + MCP servers) built successfully!"

# Build everything for production
build-all-prod: build-agents build-claude build-mcp-prod
	@echo "✅ All production configurations built successfully!"

# Build everything (legacy target - agents and global CLAUDE.md only)
build: build-agents build-claude
	@echo "✅ Agent configurations built successfully!"

# Validation targets
validate:
	@echo "🔍 Validating all configurations..."
	uv run claude-config validate
	@echo "✅ All configurations validated successfully!"

validate-mcp:
	@echo "🔍 Validating MCP configurations..."
	uv run claude-config validate-mcp
	@echo "✅ MCP configurations validated successfully!"

# Run tests
test:
	@echo "🧪 Running tests..."
	uv run pytest -v --cov=claude_config --cov-report=term-missing

# Install agents and global config to Claude Code directory
install: build
	@echo "📦 Installing agents and global config to ~/.claude/..."
	uv run claude-config install
	@echo "✅ Installed to ~/.claude/"

# Install MCP servers configuration to Claude Code directory
install-mcp: build-mcp
	@echo "📦 Installing MCP servers to ~/.claude/..."
	uv run claude-config install --output-dir dist
	@echo "✅ MCP servers installed to ~/.claude/"

# Listing targets
list-agents:
	@echo "📋 Available agent personas:"
	uv run claude-config list-agents

list-mcp:
	@echo "📋 Available MCP servers:"
	uv run claude-config list-mcp

# Clean all build artifacts
clean:
	@echo "🧹 Cleaning all build artifacts..."
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

# Clean only MCP build artifacts
clean-mcp:
	@echo "🧹 Cleaning MCP build artifacts..."
	rm -f dist/mcpServers.json
	@echo "✅ MCP clean complete!"

# Development workflow targets
dev-setup: install-dev-deps
	@echo "🔧 Setting up development environment..."
	uv sync --all-extras --dev
	pre-commit install
	@echo "✅ Development environment ready!"

install-dev-deps:
	@echo "📦 Installing development dependencies..."
	uv sync --all-extras --dev

# Quick development cycle
dev-build: validate-mcp build-mcp
	@echo "🚀 Quick development build complete!"

# Production ready build
prod-build: validate build-all-prod
	@echo "🚀 Production build complete!"

# Environment-specific complete builds
build-dev: validate
	@echo "🔧 Building complete development environment..."
	uv run claude-config build-all --validate --env dev
	@echo "✅ Development environment built!"

build-prod: validate
	@echo "🚀 Building complete production environment..."
	uv run claude-config build-all --validate --env prod --ignore-env-warnings
	@echo "✅ Production environment built!"