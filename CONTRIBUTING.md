# Contributing to Calendly MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- A clear description of the feature
- Why it would be useful
- Any implementation ideas you have

### Contributing Code

1. **Fork the repository**
2. **Create a branch** for your feature/fix:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test your changes** thoroughly
5. **Commit your changes** with clear messages:
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your test API key
4. Run the server: `python server.py`

## Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

## Testing

Before submitting a PR:
- Test all modified endpoints
- Ensure no breaking changes
- Update documentation if needed

## Adding New Features

When adding new Calendly API endpoints:

1. **Add the tool function** in `server.py`:
   ```python
   @app.tool()
   async def new_feature(param: str) -> str:
       """Description of what this does"""
       result = await calendly.request("GET", "/endpoint", params={"param": param})
       return str(result)
   ```

2. **Update API_REFERENCE.md** with documentation

3. **Add examples** to the README

4. **Test thoroughly** with real API calls

## Documentation

- Keep README.md up to date
- Update API_REFERENCE.md for new tools
- Add examples for complex features
- Update QUICKSTART.md if setup changes

## Commit Message Guidelines

Use clear, descriptive commit messages:
- `feat: Add support for XYZ endpoint`
- `fix: Resolve authentication issue`
- `docs: Update installation instructions`
- `refactor: Simplify error handling`

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update documentation as needed
3. Describe your changes in the PR description
4. Link any related issues
5. Wait for review and address feedback

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
