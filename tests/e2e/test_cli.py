from typer.testing import CliRunner

from mush_wikis_scraper.cli import cli
from mush_wikis_scraper.links import LINKS

runner = CliRunner()


def test_cli_default():
    result = runner.invoke(cli, ["--limit", "2", "--format", "markdown"])
    assert result.exit_code == 0
    assert (
        "Happens automatically when taking **any** other action, or clicking on anywhere in the room other than inventory (clicking on people makes you stand up too)"
        in result.stdout
    )
    assert "Actions\\n=======" in result.stdout


def test_cli_with_valid_urls():
    # Test with two valid URLs from the LINKS list
    result = runner.invoke(cli, ["--url", LINKS[0], "--url", LINKS[1]])
    assert result.exit_code == 0
    # Check that both pages were scraped
    assert all(url in result.stdout for url in [LINKS[0], LINKS[1]])


def test_cli_with_invalid_urls():
    # Test with invalid URLs
    invalid_urls = ["https://invalid.url", "https://another.invalid"]
    result = runner.invoke(cli, ["--url", invalid_urls[0], "--url", invalid_urls[1]])
    assert result.exit_code == 1
    assert "Error: The following URLs are not in the predefined list:" in result.stdout
    assert all(url in result.stdout for url in invalid_urls)


def test_cli_with_mixed_urls():
    # Test with one valid and one invalid URL
    result = runner.invoke(cli, ["--url", LINKS[0], "--url", "https://invalid.url"])
    assert result.exit_code == 1
    assert "Error: The following URLs are not in the predefined list:" in result.stdout
    assert "https://invalid.url" in result.stdout


def test_cli_urls_with_limit():
    # Test combining --url with --limit
    result = runner.invoke(cli, ["--url", LINKS[0], "--url", LINKS[1], "--url", LINKS[2], "--limit", "2"])
    assert result.exit_code == 0
    # Only the first two URLs should be in the output
    assert LINKS[0] in result.stdout
    assert LINKS[1] in result.stdout
    assert LINKS[2] not in result.stdout


def test_cli_urls_with_format():
    # Test combining --url with --format
    result = runner.invoke(cli, ["--url", LINKS[0], "--format", "markdown"])
    assert result.exit_code == 0
    assert "Actions\\n=======" in result.stdout
