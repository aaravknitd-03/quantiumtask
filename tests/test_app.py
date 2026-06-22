from app import app


def test_header_is_present(dash_duo):
    dash_duo.start_server(app)

    header = dash_duo.wait_for_element("#app-header", timeout=10)

    assert header is not None
    assert "Soul Foods Pink Morsels Sales Visualiser" in header.text


def test_visualisation_is_present(dash_duo):
    dash_duo.start_server(app)

    chart = dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    plot = dash_duo.wait_for_element("#sales-line-chart .js-plotly-plot", timeout=10)

    assert chart is not None
    assert plot is not None


def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app)

    region_picker = dash_duo.wait_for_element("#region-radio", timeout=10)
    radio_options = dash_duo.find_elements("#region-radio input[type='radio']")

    assert region_picker is not None
    assert len(radio_options) == 5