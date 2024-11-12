from typer.testing import CliRunner

from mushpedia_scraper.cli import cli

runner = CliRunner()


def test_app():
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "There are two teams of players on the ship. Humans who are trying to save Humanity" in result.stdout
