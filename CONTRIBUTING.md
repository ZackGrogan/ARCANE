# Contributing to ARCANE

Thank you for your interest in contributing to ARCANE! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Fork and clone the repository
2. Install dependencies:
```bash
pnpm install
```
3. Create a `.env.local` file with required environment variables
4. Start the development server:
```bash
pnpm dev
```

## Code Style

We use ESLint and Prettier to maintain consistent code style. Before submitting a PR:

1. Run the linter:
```bash
pnpm lint
```
2. Format your code:
```bash
pnpm format
```
3. Type check your code:
```bash
pnpm type-check
```

## Testing

All new features should include tests. Run the test suite:

```bash
pnpm test
```

For test coverage:
```bash
pnpm test:coverage
```

## Pull Request Process

1. Create a new branch for your feature/fix
2. Write clear commit messages
3. Update documentation as needed
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- feat: A new feature
- fix: A bug fix
- docs: Documentation changes
- style: Code style changes (formatting, etc)
- refactor: Code changes that neither fix bugs nor add features
- test: Adding or modifying tests
- chore: Changes to build process or auxiliary tools

## Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
