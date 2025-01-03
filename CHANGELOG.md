# Change Log

All notable changes to this project will be documented in this file.

## [Unreleased] - mm-dd-2024

Currently, we're working on enhancing and fixing current functionality, as well as better maintenance of the codebase.

### Added

- Error handling / checking in 'setup.sh'.

### Changed

- New and improved linters: djlint, stylelint
  - Linted all template files with djlint!
  - Linted all css files!
- Updated Django version: 4.2.10 -> 4.2.17
- Passwords now have a minimum limit of eight characters.
- '.env_sample' has local development in mind.
- 'dashboard' app has been deprecated and reborn as 'base' - a place where global / similar attributes will live.

### Fixed

- Better documentation in 'ReeldIn' folder.
- Licenses no longer text files in 'documentation/external-licenses'.
- Server recognizes when a guest is visiting a page with preferences, no longer redirects or causes an error.

## [1.0.0] - 06-04-2024

The initial release!
