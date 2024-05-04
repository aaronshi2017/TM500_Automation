# test_calculator.py
import pytest
import Calculator

def test_add():
    assert Calculator.Add(1,3)==4
    assert Calculator.Divide(4,1)==4