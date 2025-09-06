"""
Custom exceptions for Claude Config Generator.

Provides specific exception types for better error handling and debugging.
"""


class ClaudeConfigError(Exception):
    """Base exception for all Claude Config errors."""
    pass


class PersonaNotFoundError(ClaudeConfigError):
    """Raised when a referenced persona cannot be found."""
    
    def __init__(self, persona_name: str, search_path: str = None):
        self.persona_name = persona_name
        self.search_path = search_path
        msg = f"Persona '{persona_name}' not found"
        if search_path:
            msg += f" in {search_path}"
        super().__init__(msg)


class TraitNotFoundError(ClaudeConfigError):
    """Raised when a referenced trait cannot be found."""
    
    def __init__(self, trait_name: str, search_path: str = None):
        self.trait_name = trait_name
        self.search_path = search_path
        msg = f"Trait '{trait_name}' not found"
        if search_path:
            msg += f" in {search_path}"
        super().__init__(msg)


class ContentNotFoundError(ClaudeConfigError):
    """Raised when referenced content cannot be found."""
    
    def __init__(self, content_path: str, base_path: str = None):
        self.content_path = content_path
        self.base_path = base_path
        msg = f"Content file '{content_path}' not found"
        if base_path:
            msg += f" in {base_path}"
        super().__init__(msg)


class ValidationError(ClaudeConfigError):
    """Raised when configuration validation fails."""
    
    def __init__(self, message: str, errors: list = None):
        self.errors = errors or []
        super().__init__(message)


class TemplateError(ClaudeConfigError):
    """Raised when template processing fails."""
    pass


class CircularDependencyError(ClaudeConfigError):
    """Raised when circular dependencies are detected."""
    
    def __init__(self, dependency_chain: list):
        self.dependency_chain = dependency_chain
        chain_str = " -> ".join(dependency_chain)
        super().__init__(f"Circular dependency detected: {chain_str}")