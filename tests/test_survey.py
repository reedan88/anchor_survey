import numpy as np
from survey.survey import (
    dms_to_dd,
    latlon_to_xy,
    xy_to_latlon,
    calculate_anchor_position,
    rms_error,
    calculate_fallback,
    validate_survey_input,
)


def test_dms_to_dd_scalar():
    dd = dms_to_dd(35, 57, 4, 'N')
    assert np.isclose(dd, 35.9511, atol=1e-4)

    dd = dms_to_dd(75, 7, 49, 'W')
    assert np.isclose(dd, -75.1303, atol=1e-4)


def test_latlon_xy_conversion_roundtrip():
    lat, lon = 35.9511, -75.1303
    ref_lat, ref_lon = lat, lon
    x, y = latlon_to_xy(lat, lon, ref_lat, ref_lon)
    lat2, lon2 = xy_to_latlon(x, y, ref_lat, ref_lon)
    assert np.isclose(lat, lat2, atol=1e-6)
    assert np.isclose(lon, lon2, atol=1e-6)


def test_calculate_anchor_position():
    x = np.array([0.0, 100.0, 0.0])
    y = np.array([0.0, 0.0, 100.0])
    true_anchor = (50.0, 50.0)
    d = np.sqrt((x - true_anchor[0])**2 + (y - true_anchor[1])**2)
    xi, yi, iters = calculate_anchor_position(x, y, d)
    assert np.isclose(xi, true_anchor[0], atol=1e-3)
    assert np.isclose(yi, true_anchor[1], atol=1e-3)
    assert iters < 20


def test_calculate_anchor_position_max_iterations():
    # Degenerate geometry: all stations equidistant — should not converge
    x = np.array([0.0, 1000.0, 500.0])
    y = np.array([0.0, 0.0, 1000.0])
    d = np.array([100.0, 100.0, 100.0])
    xi, yi, iters = calculate_anchor_position(x, y, d, tol=1e-6, max_iter=10)
    assert iters == 9  # reached max_iter - 1 (0-indexed)


def test_rms_error_simple():
    x = np.array([0, 1])
    y = np.array([0, 0])
    dist = np.array([1, 0])
    p = (0, 0)
    err = rms_error(p, x, y, dist)
    assert err >= 0


def test_calculate_fallback_distance():
    drop_x, drop_y = 0.0, 0.0
    anchor_x, anchor_y = 50.0, 30.0
    fb = calculate_fallback(anchor_x, anchor_y, drop_x, drop_y)
    # sqrt(50^2 + 30^2) = sqrt(3400) ≈ 58.3095
    assert np.isclose(fb, 58.3095, atol=0.01)
    assert fb > 0


def test_validate_survey_input():
    x = np.array([0.0, 100.0, 50.0])
    y = np.array([0.0, 0.0, 100.0])
    d = np.array([70.71, 70.71, 70.71])
    validate_survey_input(x, y, d)  # should not raise

    try:
        validate_survey_input(
            np.array([0.0, 100.0]),
            np.array([0.0, 0.0]),
            np.array([70.71, 70.71]),
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "3 stations" in str(e)

    try:
        validate_survey_input(x, y, np.array([-1.0, 70.71, 70.71]))
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "positive" in str(e)
