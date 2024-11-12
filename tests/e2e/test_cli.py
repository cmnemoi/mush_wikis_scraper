from typer.testing import CliRunner

from mushpedia_scraper.cli import cli

runner = CliRunner()


def test_app():
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert (
        "A basic action is an action that all players have and does not need to be unlocked by choosing a skill."
        in result.stdout
    )
