from __future__ import annotations
from typing import Callable, NoReturn


class Result:
    @property
    def is_success(self): return self._is_success

    @property
    def is_failure(self): return not self._is_success

    @is_failure.setter
    def is_failure(self, value):
        self.is_success = not value

    @property
    def error_text(self): return self._error_text

    def __init__(self, is_success: bool, error: str):
        if is_success and error:
            raise ValueError("Invalid argument!")

        if not is_success and error == "":
            raise ValueError("Invalid argument!")

        self._is_success = is_success
        self._error_text = error

    @staticmethod
    def create(is_success: bool, error: str = "") -> Result:
        return Result(is_success, error)

    @staticmethod
    def fail(error: str) -> Result:
        return Result(False, error)

    @staticmethod
    def ok() -> Result:
        return Result(True, "")

    def on_success(self, function: Callable[..., Result]) -> Result:
        return function(self) if self.is_success else self

    def on_failure(self, function: Callable[..., Result]) -> Result:
        return function(self) if self.is_failure else self


def run() -> NoReturn:
    result = success().on_success(failure)
    print(f"Is success? {result.is_success}")


def success() -> Result:
    print('Success called!')
    return Result.ok()


def failure(result: Result) -> Result:
    print('Failure called!')
    return Result.fail('Error!')


if __name__ == '__main__':
    run()
