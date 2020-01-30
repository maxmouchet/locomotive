import datetime as dt

import click
from click.testing import CliRunner
from locomotive.cli import cli


def test_helper():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert "🚆 Search train journeys from your terminal" in result.output
    assert result.exit_code == 0


def test_search_with_origin_and_destination():
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "FRPAR", "FRLYS"])

    assert "km) on" in result.output
    assert result.exit_code == 0


def test_search_display_error_when_origin_not_found():
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "This station doesn't exist", "FRPAR"])

    assert "not found" in result.output
    assert result.exit_code == 1


def test_search_display_error_when_destination_not_found():
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "FRBES", "This station doesn't exist"])

    assert "not found" in result.output
    assert result.exit_code == 1


def test_search_with_date_provided():
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "FRBES", "FRPAR", "--date", "tomorrow"])

    assert "km) on" in result.output
    assert result.exit_code == 0


def test_search_with_class_provided():
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "FRPAR", "FRLYS", "--class", "first"])

    assert "km) on" in result.output
    assert result.exit_code == 0


def test_search_with_formatter_provided():
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "FRPAR", "FRLYS", "--format", "json"])

    assert "km) on" in result.output
    assert result.exit_code == 0
