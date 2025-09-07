.PHONY: help install dev build clean test lint format validate install-to-claude watch docs build-global install-global

# Default target
help:
	@echo "Claude Config Generator - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  install           Install package and dependencies"
	@echo "  dev              Install in development mode with dev dependencies"
	@echo "  install-to-claude Install generated config to ~/.claude/"
	@echo ""
	@echo "Development:"
	@echo "  build            Build agent configurations from data/"
	@echo "  validate         Validate all configurations"
	@echo "  test             Run test suite"
	@echo "  lint             Run linting (black, isort, mypy)"
	@echo "  format           Auto-format code with black and isort"
	@echo "  watch            Watch for changes and rebuild automatically"
	@echo ""
	@echo "Global Configuration:"
	@echo "  build-global     Build universal global CLAUDE.md with agent delegation"
	@echo "  install-global   Build and install global configuration to ~/.claude/"
	@echo "  verify-global    Check if global configuration is installed"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean            Clean build artifacts and cache files"
	@echo "  docs             Build documentation"
	@echo ""

# Installation
install:
	uv sync

dev:
	uv sync --dev
	uv run pre-commit install

# Building
build:
	@echo "🔨 Building agent configurations..."
	uv run claude-config build --validate
	@echo "✅ Build complete! Generated files are in dist/"

validate:
	@echo "🔍 Validating configurations..."
	uv run claude-config validate

# Testing
test:
	@echo "🧪 Running tests..."
	uv run pytest -v --cov=claude_config --cov-report=term-missing

test-watch:
	@echo "🧪 Running tests in watch mode..."
	uv run pytest-watch

# Code Quality
lint:
	@echo "🔍 Running linters..."
	uv run black --check src/ tests/
	uv run isort --check-only src/ tests/
	uv run mypy src/

format:
	@echo "🎨 Formatting code..."
	uv run black src/ tests/
	uv run isort src/ tests/

# Installation to Claude Code
install-to-claude: build
	@echo "📦 Installing to ~/.claude/..."
	uv run claude-config install
	@echo "✅ Installed to ~/.claude/"

# Development utilities
watch:
	@echo "👀 Watching for changes..."
	uv run claude-config build --watch

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

# Documentation
docs:
	@echo "📚 Building documentation..."
	# TODO: Add documentation build command
	@echo "⚠️  Documentation build not yet implemented"

# Quick development workflow
dev-cycle: format lint test build
	@echo "🚀 Development cycle complete!"

# Full CI/CD simulation
ci: lint test build validate
	@echo "✅ CI pipeline complete!"

# List available agents and traits
list:
	@echo "📋 Available configurations:"
	uv run claude-config list-agents
	@echo ""
	uv run claude-config list-traits

# One-command setup for new contributors
setup: dev
	@echo "🎉 Development environment setup complete!"
	@echo "Run 'make build' to generate your first configuration."
# Global Configuration Build System
PROFILE ?= developer
ENV ?= development

build-global:
	@echo "🌍 Building trait-aware global Claude Code configuration..."
	uv run python src/build_trait_aware_global.py

install-global: build-global
	@echo "📦 Installing universal global configuration to ~/.claude/..."
	@mkdir -p ~/.claude
	@if [ -f ~/.claude/CLAUDE.md ]; then \
		echo "💾 Backing up existing ~/.claude/CLAUDE.md to ~/.claude/CLAUDE.md.backup"; \
		cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup; \
	fi
	cp dist/global/CLAUDE.md ~/.claude/CLAUDE.md
	@echo "✅ Universal global configuration installed!"
	@echo "🔄 Restart Claude Code to apply mandatory agent delegation"

verify-global:
	@if [ -f ~/.claude/CLAUDE.md ]; then \
		echo "✅ Global configuration installed at ~/.claude/CLAUDE.md"; \
		echo "📊 Configuration size: $(wc -l ~/.claude/CLAUDE.md | cut -d' ' -f1) lines"; \
	else \
		echo "❌ No global configuration found at ~/.claude/CLAUDE.md"; \
		echo "💡 Run 'make install-global' to install"; \
	fi

clean-global:
	@echo "🧹 Cleaning global configuration artifacts..."
	rm -rf dist/global/
	@echo "✅ Global clean complete"