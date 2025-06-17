# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [2.1.0] - 2025-06-16

### Fixed

- The backend `pyrsistent_as_rpds.auto.auto_backend` was reported incorrectly
  when using the `fake_rpds` workaround. Also expose attribute
  `pyrsistent_as_rpds.auto.is_pure_pyrsistent_as_rpds` consistently.

## [2.0.0] - 2025-06-14

### Added

- Add module `pyrsistent_as_rpds.auto` which tries to import the original
  `rpds-py` package first, then falls back to importing the pure-Python
  `pyrsistent`-based implementation.

### Changed

- Move the pure-Python implementation to `pyrsistent_as_rpds.pure`. This is
  a breaking change because the top-level package `pyrsistent_as_rpds` is now
  empty.

## [1.1.0] - 2025-06-13

### Changed

- Add much more of the API in order to make the `rpds-py` tests pass.

## [1.0.0] - 2025-06-13

### Added

- Initial release.

## [0.0.0] - 1970-01-01

### Added

- This is an example entry.
- See below for the other types of changes.

### Changed

- Change in functionality.

### Deprecated

- Feature that will be removed soon.

### Removed

- Feature that is now removed.

### Fixed

- Bug that was fixed.

### Security

- Security vulnerability notice.
