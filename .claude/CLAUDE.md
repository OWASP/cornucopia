# Contributing with Claude AI Assistant

This guide helps contributors use Claude (an AI assistant) effectively when working on OWASP Cornucopia, while maintaining code quality and adhering to [project standards](/.github/copilot-instructions.md).

> This document is supposed to be the primary source of context for **all** AI tools. Context files of tools other than Claude should refer to [this `CLAUDE.md` file](CLAUDE.md) for detailed guidelines. This is already the case for:
> * GitHub CoPilot ([`.github/copilot-instructions.md`](../.github/copilot-instructions.md))

## Security Guidelines

You are an AI programming assistant that helps developers write secure code in accordance with the OWASP Application Security Verification Standard (ASVS) 5.0. All code suggestions must adhere to these security standards (Link to [ASVS 5.0 requirements](/.github/chatmodes/asvs.md) when vulnerabilities are found, and suggestions are made).
Take directions according to what is stated for the [OWASP Security Champion mode](/.github/chatmodes/owasp-security-champion.md)

## ✅ Good Use Cases

- **Code Analysis**: Understanding existing code structure and patterns
- **Refactoring**: Improving code quality while maintaining functionality
- **Test Writing**: Creating unit, integration, and e2e tests
- **Bug Fixing**: Identifying and resolving issues
- **Documentation**: Writing clear comments and documentation

## ⚠️ Use with Caution

- **Security Vulnerabilities**: Ensure AI-suggested vulnerabilities are intentional and appropriate for the project
- **Dependencies**: Verify any suggested package updates for compatibility
- **Architecture Changes**: Discuss major structural changes with maintainers first

## Essential Guidelines

### 1. Clean Up AI-Generated Noise

**Required** per CONTRIBUTING.md rule #6: Remove unnecessary AI-generated content before submitting PRs.

Remove:
- Verbose comments explaining obvious code
- Generic placeholder comments
- Overly detailed docstrings for simple functions
- Repetitive explanations

Keep:
- Meaningful comments for complex logic
- Challenge hints and metadata
- Security-relevant documentation

### 2. Code Style Compliance

Always run Black before committing Python code:
```bash
pipenv run black --line-length=120 --check .
```
For Python code, Claude should suggest code following PEP 8 style guidelines and type hints (PEP 484) for function signatures, but always verify.

### 3. Testing Requirements

For any code changes, Claude helps with:
- **Unit/Integration Tests**: New features and changes should have tests
- **E2E Tests**: Required for new/modified code

### 4. Commit Sign-off

All commits must be signed off (DCO):
```bash
git commit -s -m "Your commit message"
```

### 5. Branch and PR Strategy

- Keep PRs focused on a single scope
- Reference related issues in PR descriptions

## Development Workflow with Claude

### 1. Understanding the Codebase
```
Ask Claude to:
- Explain specific components or patterns
- Identify where to implement new features
- Trace code execution paths
```

### 2. Implementation
```
Ask Claude to:
- Generate initial implementation
- Suggest test cases
- Review for security implications
```

### 3. Quality Assurance
```
Before committing:
1. Remove AI-generated noise
2. Run npm run lint
3. Run relevant test suites
5. Manually verify functionality
6. Check for unintended changes
7. Follow the [project standards](/.github/copilot-instructions.md)
```

### 4. Documentation
```
Ask Claude to:
- Write clear commit messages
- Draft PR descriptions
- Document complex logic
```

## Anti-Patterns to Avoid

❌ **Don't**: Accept AI suggestions blindly without understanding them
✅ **Do**: Review and understand all AI-generated code

❌ **Don't**: Submit PRs with verbose AI-generated comments
✅ **Do**: Clean up and keep only meaningful comments

❌ **Don't**: Skip testing because AI "seems confident"
✅ **Do**: Always run the full test suite

❌ **Don't**: Use AI for contribution farming or trivial changes
✅ **Do**: Make meaningful contributions that add value

## Example: Fixing a Bug

```bash
# 1. Ask Claude to analyze the issue
"Help me understand why the basket total calculation is incorrect"

# 2. Locate the problematic code
"Show me where basket totals are calculated"

# 3. Implement the fix with Claude's help
"Fix the calculation to properly handle discount edge cases"

# 4. Generate tests
"Create unit tests to cover the discount calculation edge cases"

# 5. Quality checks
npm run lint
npm test
npm run rsn  # If the fix affects code used in a coding challenge

# 6. Clean up and commit with sign-off
git commit -s -m "Fix basket total calculation for discount edge cases"
```

## Quality Checklist

Before submitting a Claude-assisted PR:

- [ ] Code follows the project coding standard and style
- [ ] AI-generated noise removed
- [ ] Tests added/updated and passing
- [ ] Manual testing completed
- [ ] Commits are signed off
- [ ] Single, focused scope
- [ ] All CI checks passing

## Claude-Specific Context

The following context is provided to help Claude better assist with contributions to this project:

### Project Overview

- **Project**: OWASP Cornucopia - The project contains 3 projects:
  - [/scripts](scripts): Converter scripts to convert translations for editions of the Cornucopia game into IDML and PDF files that can be printed.
  - [/cornucopia.owasp.org](/cornucopia.owasp.org): The Website for OWASP Cornucopia written in Typescript.
  - [/copi.owasp.org](/copi.owasp.org): The Cornucopia game engine written in Elixir that can be hosted as an online game engine where it is possible to play Cornucopia and EoP-related games.
- **Primary Languages**: Python, TypeScript and Elixir
- **Key Technologies**: Node.js, Svelte, Phoenix
- **Testing**: mix test (/copi.owasp.org), vitest (/cornucopia.owasp.org), Python unittest (/scripts) 
- **Code Style**:
  - For Python code, use PEP 8 style guidelines
