# CHANGELOG


## v0.8.0 (2024-11-21)

### Chores

- Add a `make` entry to run scraper
  ([`b756698`](https://github.com/cmnemoi/mush_wikis_scraper/commit/b7566984c195839cf8625aa8cf13948123b53938))

### Documentation

- Update README with new data source supported
  ([`6465f34`](https://github.com/cmnemoi/mush_wikis_scraper/commit/6465f34077d25472c418cf5da46fdeeec1c06829))

### Features

- Add support for Mush forums help threads
  ([`184952b`](https://github.com/cmnemoi/mush_wikis_scraper/commit/184952bde4774edb239d18f79018fe5270569c8d))


## v0.7.1 (2024-11-21)

### Bug Fixes

- Cli now outputs raw characters (especially french accents) instead of Unicode sequences
  ([`bad55a0`](https://github.com/cmnemoi/mush_wikis_scraper/commit/bad55a04b8e01d2394e645d0b0548c5194fc2a42))

### Chores

- Enhance semantic-release usage
  ([`3d2b6af`](https://github.com/cmnemoi/mush_wikis_scraper/commit/3d2b6aff83078910745a99fb5c6c2c6b44452ab1))


## v0.7.0 (2024-11-20)

### Chores

- Update dependencies
  ([`515fcb4`](https://github.com/cmnemoi/mush_wikis_scraper/commit/515fcb4c7eb7fe6f38226d46e32f82e9f5f308d9))

- Update semantic-release command to include --no-commit flag in Makefile
  ([`5934d7a`](https://github.com/cmnemoi/mush_wikis_scraper/commit/5934d7a0910bfabd068d2679fc91007d2edffc6f))

- Update project metadata and add URLs for bug tracking and changelog in pyproject.toml
  ([`3582826`](https://github.com/cmnemoi/mush_wikis_scraper/commit/3582826294bcc04e941e50920cabf236e6bcba5e))

- Run semantic-release at each commit so `uv.lock` can be properly updated
  ([`f5f8bd4`](https://github.com/cmnemoi/mush_wikis_scraper/commit/f5f8bd4af2af4e9157cbfc9c10026ae565504edf))

- Check types after each commit
  ([`c739b92`](https://github.com/cmnemoi/mush_wikis_scraper/commit/c739b92f00f3d7910f5fbb1d989eab76d0f4ffdc))

### Features

- Add support for 'Aide aux Bolets'
  ([`b53f5af`](https://github.com/cmnemoi/mush_wikis_scraper/commit/b53f5afbf192bbf116b3e778eba17a3530adec56))


## v0.6.0 (2024-11-14)

### Bug Fixes

- More tolerant timeout
  ([`d4d1d00`](https://github.com/cmnemoi/mush_wikis_scraper/commit/d4d1d009f7824af3593e6aa7bac57f5cce05f070))

- Remove some duplicated links to scrap
  ([`c3ed71a`](https://github.com/cmnemoi/mush_wikis_scraper/commit/c3ed71a54d197cb4ad044e838aeb19d92bc02d4a))

- Fix a crash when scraping some Twinpedia pages
  ([`eddba57`](https://github.com/cmnemoi/mush_wikis_scraper/commit/eddba5743de97114cd6656e0cc799a2e54c54cfb))

### Code Style

- Apply linter fixes
  ([`f66e6cc`](https://github.com/cmnemoi/mush_wikis_scraper/commit/f66e6cc53a297bead3fbc11e3a94c8c5e741bb1b))

### Documentation

- Update badge links in README
  ([`7a163bc`](https://github.com/cmnemoi/mush_wikis_scraper/commit/7a163bcbb60c5bd944e2e08820914e457213eda8))

### Features

- Add a progress bar
  ([`6403e6d`](https://github.com/cmnemoi/mush_wikis_scraper/commit/6403e6da61b6ee410bbc29be4509f46383c76792))


## v0.5.0 (2024-11-14)

### Features

- Add new `source` entry for the scrapped content (Twinpedia, Mushpedia)
  ([`b2a850b`](https://github.com/cmnemoi/mush_wikis_scraper/commit/b2a850b8c884877871f0bb34ff89d4bbe4377a0c))

- Supports Twinpedia
  ([`7a57c11`](https://github.com/cmnemoi/mush_wikis_scraper/commit/7a57c116b7627fff6fc91f6e32bc44c7da742d11))

- Change name of the package
  ([`184cb39`](https://github.com/cmnemoi/mush_wikis_scraper/commit/184cb392f8c950aa54725cb0c5b695890555d861))


## v0.4.0 (2024-11-14)

### Bug Fixes

- Scraper now supports HTTP redirections
  ([`bb9cb69`](https://github.com/cmnemoi/mush_wikis_scraper/commit/bb9cb6966089756ae0289748b9468da4b5d2cbff))

### Features

- Output format is now a valid JSON
  ([`78da433`](https://github.com/cmnemoi/mush_wikis_scraper/commit/78da433d27b1532760cf215394d045f2b7859f60))

- Do not remove line break for plain text and markdown output formats
  ([`7ab2245`](https://github.com/cmnemoi/mush_wikis_scraper/commit/7ab2245d5a9379174c41c4fd138717810c1263d4))


## v0.3.1 (2024-11-13)

### Bug Fixes

- Migrate from `html2text` to `markdownify`
  ([`c3a46d4`](https://github.com/cmnemoi/mush_wikis_scraper/commit/c3a46d4307482af63e8e74ea8e695667b9998fcf))

### Documentation

- Update README with the new `--format` option
  ([`f76ee89`](https://github.com/cmnemoi/mush_wikis_scraper/commit/f76ee896b20534fc78cb2638bccfa2a937168055))


## v0.3.0 (2024-11-13)

### Bug Fixes

- Remove line breaks from scrapped HTML markup
  ([`1e93e1c`](https://github.com/cmnemoi/mush_wikis_scraper/commit/1e93e1c40c6d6e98cdb6ed994999b599d14f7855))

### Chores

- Launch pytest with full verbosity
  ([`0a4b240`](https://github.com/cmnemoi/mush_wikis_scraper/commit/0a4b24059c6e7a2c9c8ce9f32b578c849269d9c6))

- Bump to 100% code coverage by not covering no-op paths
  ([`66fd499`](https://github.com/cmnemoi/mush_wikis_scraper/commit/66fd4991138b4e2278f5e70a8d554992a165b5c4))

### Features

- Add `--format` with HTML, raw text and Markdown options
  ([`c4d300d`](https://github.com/cmnemoi/mush_wikis_scraper/commit/c4d300dda4b78d38a4446cad010dbc3fb0ed80d0))

- Add a `--limit` option to the CLI
  ([`9510499`](https://github.com/cmnemoi/mush_wikis_scraper/commit/9510499a543238b53dbd8e7ad08300ba7cefcb95))


## v0.2.1 (2024-11-12)

### Bug Fixes

- Package supports Python 3.9+
  ([`585d143`](https://github.com/cmnemoi/mush_wikis_scraper/commit/585d14351904450911a95fe0f12047ac230bf58f))

### Continuous Integration

- Add a matrix to ensure the package works on all Python 3.9+ versions
  ([`b79dbfe`](https://github.com/cmnemoi/mush_wikis_scraper/commit/b79dbfea52e836f1226936ef2addc73ab8148292))

### Documentation

- Add PyPI badge to RADME
  ([`2d4354d`](https://github.com/cmnemoi/mush_wikis_scraper/commit/2d4354d6a62d87fb8ea58a47652b9acb90c5be36))


## v0.2.0 (2024-11-12)

### Continuous Integration

- Update CD Pypi workflow to allow pushing
  ([`140dc77`](https://github.com/cmnemoi/mush_wikis_scraper/commit/140dc7799e997382b0bf54fb981b9fb3e71cd0f8))

### Documentation

- Add CD pipeline and code coverage badges
  ([`7c515ce`](https://github.com/cmnemoi/mush_wikis_scraper/commit/7c515cee0533fbf9c78d21fc4a9771ee85ae02a0))

### Features

- Update package name
  ([`58b1cd2`](https://github.com/cmnemoi/mush_wikis_scraper/commit/58b1cd2bb74d067521b7c1ffe2a1970c1b5d6f16))


## v0.1.0 (2024-11-12)

### Features

- First working version ([#1](https://github.com/cmnemoi/mush_wikis_scraper/pull/1),
  [`9d9b6e3`](https://github.com/cmnemoi/mush_wikis_scraper/commit/9d9b6e34d1018fa60e449ef25ef3037403b05891))
