#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pytest
from rop.result import Result

__author__ = "Sherry Ummen"
__copyright__ = "Sherry Ummen"
__license__ = "mit"

__counter__: int = 0

class ResultTest(unittest.TestCase):
    _counter = 0

    def setup_method(self, method):
        self._counter = 0
        

    def test_on_success(self):
        result = ResultTest.success() \
                    .on_success(lambda  : Result.ok())    
        assert result.is_success == True
        assert result.is_failure == False

    def test_on_failure(self):
        result = ResultTest.failure().on_success(lambda : Result.fail('Error!'))
        assert result.is_success == False
        assert result.is_failure == True

    def test_on_success_chain_failure(self):
        result = ResultTest.success() \
                    .on_success(lambda : self._func_increase_counter(Result.fail('Error!'))) \
                    .on_success(lambda : self._func_increase_counter(Result.ok()))

        assert result.is_failure == True
        assert result.error_text == 'Error!'
        assert self._counter == 1

    def test_on_success_chain_success(self):
        result = ResultTest.success() \
                    .on_success(lambda : self._func_increase_counter(Result.ok())) \
                    .on_success(lambda : self._func_increase_counter(Result.ok()))

        assert result.is_success == True
        assert self._counter == 2

    def test_on_failure_chain_failure(self):
        result = ResultTest.failure() \
                    .on_failure(lambda : self._func_increase_counter(Result.fail('Error!'))) \
                    .on_failure(lambda : self._func_increase_counter(Result.ok()))

        assert result.is_success == True
        assert self._counter == 2

    def test_on_failure_chain_success(self):
        result = ResultTest.failure() \
                    .on_failure(lambda : self._func_increase_counter(Result.ok())) \
                    .on_failure(lambda : self._func_increase_counter(Result.ok()))

        assert result.is_success == True
        assert self._counter == 1

    def _func_increase_counter(self, result: Result) -> Result:
        self._counter += 1
        return result

    
    @staticmethod
    def success() -> Result:
        return Result.ok()

    @staticmethod
    def failure() -> Result:
        return Result.fail('Error!')
