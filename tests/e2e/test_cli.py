from typer.testing import CliRunner

from mush_wikis_scraper.cli import cli

runner = CliRunner()
EMUSHPEDIA_LINKS = [
    "https://fr.emushpedia.com/wiki/Abnégation",
    "https://fr.emushpedia.com/wiki/Accueil",
    "https://fr.emushpedia.com/wiki/Accueil/fr",
]


def test_cli_default():
    result = runner.invoke(cli, ["--limit", "2", "--format", "markdown"])
    assert result.exit_code == 0
    assert "Abnégation — eMushpedia" in result.stdout


def test_cli_does_not_offer_hardcoded_links():
    # Given the CLI
    # When its help is requested
    result = runner.invoke(cli, ["--help"])

    # Then no offline hardcoded source is offered
    assert "--use-local-links" not in result.stdout  # @spec supported-wiki::api-only-discovery


def test_cli_with_valid_urls():
    result = runner.invoke(cli, ["--url", EMUSHPEDIA_LINKS[0], "--url", EMUSHPEDIA_LINKS[1]])
    assert result.exit_code == 0
    assert all(url in result.stdout for url in EMUSHPEDIA_LINKS[:2])


def test_cli_with_invalid_urls():
    invalid_urls = ["https://invalid.url", "https://another.invalid"]
    result = runner.invoke(cli, ["--url", invalid_urls[0], "--url", invalid_urls[1]])
    assert result.exit_code == 1
    assert "Error: The following URLs are not in the available links:" in result.stderr
    assert all(url in result.stderr for url in invalid_urls)


def test_cli_rejects_legacy_wiki_url():
    legacy_url = "https://emushpedia.miraheze.org/wiki/Actions"
    result = runner.invoke(cli, ["--url", legacy_url])
    assert result.exit_code == 1  # @spec supported-wiki::rejects-legacy-links


def test_cli_with_mixed_urls():
    result = runner.invoke(cli, ["--url", EMUSHPEDIA_LINKS[0], "--url", "https://invalid.url"])
    assert result.exit_code == 1
    assert "https://invalid.url" in result.stderr


def test_cli_urls_with_limit():
    result = runner.invoke(
        cli,
        [
            "--url",
            EMUSHPEDIA_LINKS[0],
            "--url",
            EMUSHPEDIA_LINKS[1],
            "--url",
            EMUSHPEDIA_LINKS[2],
            "--limit",
            "2",
        ],
    )
    assert result.exit_code == 0
    assert EMUSHPEDIA_LINKS[0] in result.stdout
    assert EMUSHPEDIA_LINKS[1] in result.stdout
    assert EMUSHPEDIA_LINKS[2] not in result.stdout


def test_cli_urls_with_format():
    result = runner.invoke(cli, ["--url", EMUSHPEDIA_LINKS[0], "--format", "markdown"])
    assert result.exit_code == 0
    assert "Abnégation — eMushpedia" in result.stdout
