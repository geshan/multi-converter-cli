import math
from hypothesis import given, settings, assume
from hypothesis.strategies import floats

from converters.temperature import celsius_to_fahrenheit, fahrenheit_to_celsius


# Feature: unit-converter-cli, Property 1: For any float value c, celsius_to_fahrenheit(c) shall equal (c * 9/5) + 32 (before rounding)
@settings(max_examples=100)
@given(floats(allow_nan=False, allow_infinity=False))
def test_c_to_f_formula(c):
    """Validates: Requirements 5.1"""
    expected = (c * 9 / 5) + 32
    # Skip values that overflow to infinity after the formula is applied
    assume(math.isfinite(expected))
    result = celsius_to_fahrenheit(c)
    # result is rounded to 2 d.p., so it may differ from the exact formula by at most 0.005
    assert abs(result - expected) <= 0.005


# Feature: unit-converter-cli, Property 2: For any float value f, fahrenheit_to_celsius(f) shall equal (f - 32) * 5/9 (before rounding)
@settings(max_examples=100)
@given(floats(allow_nan=False, allow_infinity=False))
def test_f_to_c_formula(f):
    """Validates: Requirements 5.2"""
    expected = (f - 32) * 5 / 9
    # Skip values that overflow to infinity after the formula is applied
    assume(math.isfinite(expected))
    result = fahrenheit_to_celsius(f)
    # result is rounded to 2 d.p., so it may differ from the exact formula by at most 0.005
    assert abs(result - expected) <= 0.005
