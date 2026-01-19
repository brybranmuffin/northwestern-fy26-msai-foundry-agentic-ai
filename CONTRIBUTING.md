# Contributing to Azure AI Foundry Agent Extension

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment for all contributors.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/northwestern-msai-foundry-agent-extension.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`

## Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pre-commit

# Set up pre-commit hooks (optional but recommended)
pre-commit install
```

## Code Quality Standards

### 1. Code Style

- **PEP 8 Compliance**: All code must follow PEP 8 guidelines
- **Black Formatting**: Use Black for code formatting
- **Ruff Linting**: Code must pass Ruff linting checks

```bash
# Format code with Black
black src/ tests/

# Check with Ruff
ruff check src/ tests/
```

### 2. Type Hints

- All functions must have complete type annotations (PEP 484)
- Use `typing` module for complex types
- No use of `Any` unless absolutely necessary

```python
# Good
def process_data(values: List[int], operation: str) -> Dict[str, Any]:
    ...

# Bad
def process_data(values, operation):
    ...
```

### 3. Docstrings

- Follow PEP 257 conventions
- Include parameter descriptions, return types, and exceptions
- Use complete sentences

```python
def example_function(param: str) -> bool:
    """Check if parameter is valid.
    
    Args:
        param: The parameter to validate.
        
    Returns:
        True if valid, False otherwise.
        
    Raises:
        ValueError: If param is empty.
    """
    ...
```

### 4. Logging

- Use the `logging` module (NO `print()` statements)
- Include appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Add context to log messages

```python
# Good
import logging
logger = logging.getLogger(__name__)
logger.info(f"Processing {len(items)} items")

# Bad
print("Processing items")
```

### 5. Error Handling

- Use comprehensive try-except blocks
- Log errors before raising or returning
- Provide meaningful error messages

```python
# Good
try:
    result = risky_operation()
    logger.info("Operation completed successfully")
    return result
except SpecificError as e:
    logger.error(f"Operation failed: {str(e)}")
    raise

# Bad
result = risky_operation()  # No error handling
```

## Testing

### Writing Tests

- Write tests for all new functionality
- Maintain or improve code coverage (target: 80%+)
- Use pytest fixtures for test data
- Follow the Arrange-Act-Assert pattern

```python
def test_example_function(sample_data):
    """Test example function with sample data."""
    # Arrange
    config = FunctionConfig(**sample_data)
    
    # Act
    result = process_function(config)
    
    # Assert
    assert result.status == "success"
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_azure_functions.py -v

# Run tests with markers
pytest tests/ -v -m unit
```

### Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow-running tests

## Pull Request Process

1. **Update Documentation**: Update README.md and docs/ if needed
2. **Add Tests**: Include tests for new features
3. **Run Quality Checks**: Ensure all checks pass
   ```bash
   ruff check src/ tests/
   black --check src/ tests/
   mypy src/
   pytest tests/ -v
   ```
4. **Update CHANGELOG**: Add your changes to CHANGELOG.md (if exists)
5. **Write Clear Commit Messages**: Follow conventional commits format
6. **Create Pull Request**: Provide a clear description of changes

### Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(azure-functions): add retry logic with exponential backoff

Implements automatic retry for transient failures in Azure Functions
client with configurable retry attempts and backoff strategy.

Closes #123
```

## Project Structure

```
northwestern-msai-foundry-agent-extension/
├── src/                    # Source code
│   ├── abstractions/       # Azure service abstractions
│   └── agent_core.py       # Core agent implementation
├── tests/                  # Test suite
├── notebooks/              # Interactive tutorials
├── docs/                   # Documentation
└── .github/workflows/      # CI/CD pipelines
```

## Adding New Features

### Adding a New Azure Service Integration

1. Create abstraction in `src/abstractions/new_service.py`
2. Follow existing patterns (FunctionConfig, Client, etc.)
3. Add comprehensive docstrings and type hints
4. Create tests in `tests/test_new_service.py`
5. Update `src/abstractions/__init__.py`
6. Add usage example to README.md
7. Consider creating a notebook tutorial

### Adding a New Tool Type

1. Extend the agent core in `src/agent_core.py`
2. Add tool registration method
3. Update tool invocation logic
4. Add tests
5. Document in README.md and notebooks

## Documentation

- Update README.md for user-facing changes
- Update docs/ for architectural changes
- Add inline comments for complex logic
- Create notebooks for new features
- Include examples in docstrings

## Code Review Checklist

Before submitting, ensure:

- [ ] Code follows PEP 8 and is Black-formatted
- [ ] All functions have type hints
- [ ] All functions have docstrings
- [ ] Tests added for new functionality
- [ ] All tests pass
- [ ] Code coverage maintained or improved
- [ ] No print() statements (use logging)
- [ ] Error handling is comprehensive
- [ ] Documentation updated
- [ ] No hardcoded credentials or secrets

## Questions or Need Help?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Review existing issues and PRs

## Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Project documentation

Thank you for contributing! 🎉
