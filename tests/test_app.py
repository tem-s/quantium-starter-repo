import pytest

# Import the Dash app instance from your app.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app import app
def test_header_is_present(dash_duo):
    dash_duo.start_server(app)
    assert dash_duo.wait_for_element("h1", timeout=10)

@pytest.mark.parametrize("viewport", [(1280, 720)])
def test_header_is_present(dash_duo, viewport):
    dash_duo.driver.set_window_size(*viewport)
    dash_duo.start_server(app)

    # Header title should exist (your H1)
    header = dash_duo.wait_for_element("h1", timeout=10)
    assert header is not None
    assert "Pink Morsel" in header.text


@pytest.mark.parametrize("viewport", [(1280, 720)])
def test_visualisation_is_present(dash_duo, viewport):
    dash_duo.driver.set_window_size(*viewport)
    dash_duo.start_server(app)

    # Graph component should exist by id
    graph = dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    assert graph is not None


@pytest.mark.parametrize("viewport", [(1280, 720)])
def test_region_picker_is_present(dash_duo, viewport):
    dash_duo.driver.set_window_size(*viewport)
    dash_duo.start_server(app)

    # RadioItems container should exist by id
    picker = dash_duo.wait_for_element("#region-filter", timeout=10)
    assert picker is not None