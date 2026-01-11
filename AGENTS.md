# AGENTS.md

Code conventions guide for agents working on the **mush_wikis_scraper** project.

Work exclusively in [TDD](ai/rules/tdd.md).

### Commandes essentielles
- **Build**: `make install` to install dependencies with uv
- **Tests**: `make test` to run all tests with coverage
- **Lint**: `make lint` to format and fix code (ruff + mypy)

See [Makefile](Makefile) for all available commands.

### Python Code Style (3.10-3.13)
- **Strict typing mandatory** - no untyped values tolerated
- Line length: 119 characters max
- Ordered imports: stdlib → third-party → local
- Naming conventions: `PascalCase` (classes), `snake_case` (functions/variables), `UPPER_SNAKE_CASE` (constants)
- Functions: max 20 lines, max 3 parameters (otherwise TypedDict)
- Numpy docstrings for all public code, not for private methods (`_method`)

→ See [ai/rules/clean-code.md](ai/rules/clean-code.md) for details on code organization and clean code principles
→ See [ai/rules/naming-conventions.md](ai/rules/naming-conventions.md) for details on naming conventions

### Tests
- Pytest with commented Given-When-Then pattern
- Only fakes/spies/stubs - **NEVER mocks**
- Test behavior, not implementation

→ See [ai/rules/testing-standards.md](ai/rules/testing-standards.md) for testing standards
→ See [ai/rules/testing-unit.md](ai/rules/testing-unit.md) for best practices in unit testing
→ See [ai/rules/testing-integration.md](ai/rules/testing-integration.md) for integration tests

### Architecture
- **Ports & Adapters** (Hexagonal): core domain depends on abstractions, not implementations
- Max 300 lines per file, one responsibility per file
- Composition rather than inheritance

→ See [ai/rules/clean-code.md](ai/rules/clean-code.md) for details on code organization and clean code principles