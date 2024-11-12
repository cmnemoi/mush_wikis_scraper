from typer.testing import CliRunner

from mushpedia_scraper.cli import cli

runner = CliRunner()


def test_cli():
    result = runner.invoke(cli, ["--limit", "2", "--format", "markdown"])
    assert result.exit_code == 0
    assert (
        "Happens automatically when taking **any** other action, or clicking on anywhere in the room other than inventory (clicking on people makes you stand up too)"
        in result.stdout
    )
    assert "#  Actions" in result.stdout
