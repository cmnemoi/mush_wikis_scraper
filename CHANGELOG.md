# CHANGELOG


## v0.4.0 (2024-11-14)

### Bug Fixes

- Scraper now supports HTTP redirections
  ([`bb9cb69`](https://github.com/cmnemoi/mushpedia_scraper/commit/bb9cb6966089756ae0289748b9468da4b5d2cbff))

### Features

- Output format is now a valid JSON
  ([`78da433`](https://github.com/cmnemoi/mushpedia_scraper/commit/78da433d27b1532760cf215394d045f2b7859f60))

- Do not remove line break for plain text and markdown output formats
  ([`7ab2245`](https://github.com/cmnemoi/mushpedia_scraper/commit/7ab2245d5a9379174c41c4fd138717810c1263d4))


## v0.3.1 (2024-11-13)

### Bug Fixes

- Migrate from `html2text` to `markdownify`
  ([`c3a46d4`](https://github.com/cmnemoi/mushpedia_scraper/commit/c3a46d4307482af63e8e74ea8e695667b9998fcf))

### Documentation

- Update README with the new `--format` option
  ([`f76ee89`](https://github.com/cmnemoi/mushpedia_scraper/commit/f76ee896b20534fc78cb2638bccfa2a937168055))


## v0.3.0 (2024-11-13)

### Bug Fixes

- Remove line breaks from scrapped HTML markup
  ([`1e93e1c`](https://github.com/cmnemoi/mushpedia_scraper/commit/1e93e1c40c6d6e98cdb6ed994999b599d14f7855))

### Chores

- Launch pytest with full verbosity
  ([`0a4b240`](https://github.com/cmnemoi/mushpedia_scraper/commit/0a4b24059c6e7a2c9c8ce9f32b578c849269d9c6))

- Bump to 100% code coverage by not covering no-op paths
  ([`66fd499`](https://github.com/cmnemoi/mushpedia_scraper/commit/66fd4991138b4e2278f5e70a8d554992a165b5c4))

### Features

- Add `--format` with HTML, raw text and Markdown options
  ([`c4d300d`](https://github.com/cmnemoi/mushpedia_scraper/commit/c4d300dda4b78d38a4446cad010dbc3fb0ed80d0))

- Add a `--limit` option to the CLI
  ([`9510499`](https://github.com/cmnemoi/mushpedia_scraper/commit/9510499a543238b53dbd8e7ad08300ba7cefcb95))


## v0.2.1 (2024-11-12)

### Bug Fixes

- Package supports Python 3.9+
  ([`585d143`](https://github.com/cmnemoi/mushpedia_scraper/commit/585d14351904450911a95fe0f12047ac230bf58f))

### Continuous Integration

- Add a matrix to ensure the package works on all Python 3.9+ versions
  ([`b79dbfe`](https://github.com/cmnemoi/mushpedia_scraper/commit/b79dbfea52e836f1226936ef2addc73ab8148292))

### Documentation

- Add PyPI badge to RADME
  ([`2d4354d`](https://github.com/cmnemoi/mushpedia_scraper/commit/2d4354d6a62d87fb8ea58a47652b9acb90c5be36))


## v0.2.0 (2024-11-12)

### Continuous Integration

- Update CD Pypi workflow to allow pushing
  ([`140dc77`](https://github.com/cmnemoi/mushpedia_scraper/commit/140dc7799e997382b0bf54fb981b9fb3e71cd0f8))

### Documentation

- Add CD pipeline and code coverage badges
  ([`7c515ce`](https://github.com/cmnemoi/mushpedia_scraper/commit/7c515cee0533fbf9c78d21fc4a9771ee85ae02a0))

### Features

- Update package name
  ([`58b1cd2`](https://github.com/cmnemoi/mushpedia_scraper/commit/58b1cd2bb74d067521b7c1ffe2a1970c1b5d6f16))


## v0.1.0 (2024-11-12)

### Features

- First working version ([#1](https://github.com/cmnemoi/mushpedia_scraper/pull/1),
  [`9d9b6e3`](https://github.com/cmnemoi/mushpedia_scraper/commit/9d9b6e34d1018fa60e449ef25ef3037403b05891))
