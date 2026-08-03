# Supported wiki

## Why

The scraper must target the current French, English, and Spanish eMushpedia wikis instead of legacy wikis and archives.

## Scope

This spec covers links discovered and accepted by the CLI.

## Rules

### Localized eMushpedia wikis are offered

`{#supported-wiki::supports-localized-emushpedia}`

Link discovery returns pages hosted on `fr.emushpedia.com`, `en.emushpedia.com`, and `es.emushpedia.com`.

### Links are discovered from the API

`{#supported-wiki::api-only-discovery}`

The CLI discovers available pages from the French, English, and Spanish eMushpedia APIs. It does not expose a hardcoded or offline link source.

### Legacy links are rejected

`{#supported-wiki::rejects-legacy-links}`

A requested URL from another host is rejected as unavailable.

## Acceptance criteria

- Given link discovery, when links are fetched, then pages from the French, English, and Spanish eMushpedia wikis are returned.
- Given link discovery, when links are fetched, then no other host is returned.
- Given the CLI help, when its options are listed, then no local-links option is exposed.
- Given a legacy URL, when it is passed to the CLI, then the CLI exits with an error.

## Out of scope

- Redirecting legacy URLs.
- Offline scraping.
- Deleting historical test fixtures.
