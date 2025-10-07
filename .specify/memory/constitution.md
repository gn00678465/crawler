<!--
SYNC IMPACT REPORT
==================
Version change: [NEW] → 1.0.0
Rationale: Initial constitution ratification

Principles added:
- I. Python 3 Development Standard
- II. UV Package Management (NON-NEGOTIABLE)
- III. Test-Driven Development (NON-NEGOTIABLE)
- IV. Integration Testing
- V. Code Quality & Documentation

Sections added:
- Technology Stack Requirements
- Development Workflow

Templates requiring updates:
- ✅ plan-template.md (Constitution Check section will reference these principles)
- ✅ spec-template.md (Testing requirements aligned)
- ✅ tasks-template.md (TDD workflow enforced in task ordering)

Follow-up TODOs:
- None

Last updated: 2025-10-08
-->

# Crawler Project Constitution

## Core Principles

### I. Python 3 Development Standard

All development MUST use Python 3 as the primary programming language.

**Requirements**:
- Python 3.10 or higher MUST be used for all new code
- Type hints MUST be used for all function signatures and class attributes
- Code MUST follow PEP 8 style guidelines
- Async/await patterns SHOULD be used for I/O-bound operations

**Rationale**: Python 3 provides modern language features, strong community support, and
excellent libraries for web crawling and data processing tasks.

### II. UV Package Management (NON-NEGOTIABLE)

UV MUST be used exclusively for all package management and dependency resolution.

**Requirements**:
- All dependencies MUST be declared in `pyproject.toml`
- `uv.lock` file MUST be committed to version control
- Package installation MUST use `uv pip install` or `uv sync`
- Virtual environments MUST be created with `uv venv`
- No other package managers (pip, poetry, pipenv) are permitted for production code

**Rationale**: UV provides fast, reliable dependency resolution and ensures consistent
environments across all development and deployment scenarios. Standardizing on a single
tool eliminates dependency conflicts and simplifies onboarding.

### III. Test-Driven Development (NON-NEGOTIABLE)

TDD MUST be followed for all feature development without exception.

**Mandatory Workflow**:
1. Write test cases FIRST (before any implementation)
2. Ensure tests FAIL initially (red phase)
3. Implement minimal code to pass tests (green phase)
4. Refactor while keeping tests green (refactor phase)
5. Repeat for each feature increment

**Requirements**:
- Tests MUST be written and approved before implementation begins
- All tests MUST fail before implementation (proves tests are valid)
- Red-Green-Refactor cycle MUST be strictly enforced
- Test files MUST be created in `tests/` directory before implementation files
- Each commit SHOULD represent a complete red-green-refactor cycle

**Rationale**: TDD ensures code correctness, prevents regressions, enables confident
refactoring, and serves as living documentation. The discipline catches bugs early and
reduces long-term maintenance costs.

### IV. Integration Testing

Integration tests MUST be written for all inter-component communication and contracts.

**Focus areas requiring integration tests**:
- API endpoint contracts and response schemas
- Database query interfaces and data models
- External service integrations (web scraping targets, APIs)
- Message queue producers and consumers
- File I/O and data serialization formats

**Requirements**:
- Integration tests MUST be in `tests/integration/` directory
- Contract tests MUST be in `tests/contract/` directory
- Tests MUST use realistic data (not mocked at integration boundaries)
- Tests MUST validate error handling and edge cases

**Rationale**: Unit tests alone cannot catch interface mismatches, data format issues,
or integration failures that emerge when components interact.

### V. Code Quality & Documentation

All code MUST meet quality and documentation standards before merge.

**Requirements**:
- Public functions and classes MUST have docstrings (Google or NumPy style)
- Complex algorithms MUST include inline comments explaining the approach
- Type hints MUST be validated with mypy (strict mode)
- Code coverage MUST be ≥ 80% for new code
- Linting MUST pass (ruff or flake8 + black for formatting)
- Security scanning MUST be run (bandit) for production code

**Rationale**: High-quality, well-documented code reduces technical debt, improves
maintainability, and enables team members to understand and modify code safely.

## Technology Stack Requirements

### Required Stack Components

**Language & Runtime**:
- Python 3.10+ (REQUIRED)
- UV package manager (REQUIRED)

**Testing Framework**:
- pytest (REQUIRED for unit and integration tests)
- pytest-asyncio (for async test support)
- pytest-cov (for coverage reporting)

**Code Quality Tools**:
- mypy (type checking in strict mode)
- ruff or flake8 + black (linting and formatting)
- bandit (security scanning)

**Development Environment**:
- Virtual environments MUST be managed with `uv venv`
- Pre-commit hooks SHOULD enforce linting and type checking
- CI/CD MUST run all tests and quality checks

**Dependency Management**:
- All dependencies MUST be pinned in `uv.lock`
- Security updates MUST be reviewed monthly
- Dependency upgrades MUST pass all tests before merge

### Prohibited Practices

- Using package managers other than UV (pip, poetry, pipenv)
- Skipping tests or TDD workflow ("I'll write tests later")
- Merging code without type hints or docstrings
- Committing code that fails linting or type checking
- Using mutable default arguments in function signatures
- Ignoring security warnings from bandit without documented justification

## Development Workflow

### Feature Development Process

1. **Specification Phase**:
   - Create feature spec using `/speckit.specify` command
   - Define user stories with acceptance criteria
   - Identify testable requirements

2. **Planning Phase**:
   - Create implementation plan using `/speckit.plan` command
   - Design data models and contracts
   - Review against Constitution Check gates

3. **TDD Implementation Phase**:
   - Generate tasks using `/speckit.tasks` command
   - Write tests FIRST for each task
   - Verify tests FAIL (red phase)
   - Implement minimal code to pass (green phase)
   - Refactor while keeping tests green
   - Commit after each complete cycle

4. **Integration Phase**:
   - Write integration tests for component interactions
   - Validate contracts between modules
   - Test error handling and edge cases

5. **Review Phase**:
   - Code review MUST verify TDD workflow was followed
   - All tests MUST pass (unit + integration)
   - Coverage MUST meet ≥ 80% threshold
   - Type checking and linting MUST pass
   - Documentation MUST be complete

### Code Review Requirements

All pull requests MUST satisfy:
- [ ] Tests were written BEFORE implementation
- [ ] All tests pass (pytest exit code 0)
- [ ] Type checking passes (mypy --strict)
- [ ] Linting passes (ruff or flake8)
- [ ] Code coverage ≥ 80% for new code
- [ ] Docstrings present for all public APIs
- [ ] No security issues from bandit
- [ ] UV lock file updated if dependencies changed

### Quality Gates

**Pre-commit** (automated via pre-commit hooks):
- Format code with black or ruff format
- Run type checking with mypy
- Run linting with ruff or flake8
- Run security scan with bandit

**Pre-merge** (automated via CI):
- All unit tests pass
- All integration tests pass
- Code coverage meets threshold
- Type checking passes in strict mode
- No linting errors
- No security vulnerabilities

**Pre-release** (manual checklist):
- All features have complete test coverage
- Integration tests validate all contracts
- Documentation updated (README, API docs)
- Security audit completed
- Performance benchmarks met (if applicable)

## Governance

### Authority and Compliance

This constitution supersedes all other development practices and conventions. All team
members MUST adhere to these principles. Deviations require documented justification
and approval through the amendment process.

### Amendment Process

1. Propose amendment via pull request to this file
2. Document rationale and impact analysis
3. Update affected templates and guidance documents
4. Increment version according to semantic versioning rules
5. Require team consensus before merge
6. Provide migration plan if backward incompatible

### Version Policy

- **MAJOR**: Backward incompatible changes (principle removal/redefinition)
- **MINOR**: New principles or materially expanded guidance
- **PATCH**: Clarifications, typo fixes, non-semantic refinements

### Complexity Justification

Any deviation from these principles (e.g., skipping TDD, using alternative package
managers) MUST be justified in the implementation plan's Complexity Tracking section
with clear reasoning why the standard approach is insufficient.

### Enforcement

- All PRs MUST be reviewed against constitutional compliance
- CI/CD MUST enforce technical requirements (tests, linting, typing)
- Constitutional violations MUST be addressed before merge
- Repeated violations require architecture review

**Version**: 1.0.0 | **Ratified**: 2025-10-08 | **Last Amended**: 2025-10-08
