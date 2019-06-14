import click
from click.testing import CliRunner

import datetime as dt

from locomotive.cli import cli


def test_helper():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert "🚆 Search SNCF journeys from your terminal" in result.output
    assert result.exit_code == 0


def test_search_with_origin_and_destination():
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "FRBES", "FRPAR"])

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
    result = runner.invoke(
        cli, ["search", "FRBES", "FRPAR", "--date", str(dt.date.today())]
    )

    assert "km) on" in result.output
    assert result.exit_code == 0


def test_search_with_class_provided():
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "FRBES", "FRPAR", "--class", "first"])

    assert "km) on" in result.output
    assert result.exit_code == 0


def test_search_with_formatter_provided():
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "FRBES", "FRPAR", "--format", "json"])

    assert "km) on" in result.output
    assert result.exit_code == 0
