import re
import sys

import jsonschema
from typing import Callable, Any


MY_SCHEMA = {
    "type": "object",
    "examples": [{"email": "john@gmail.com"}],
    "required": ["email"],
    "additionalProperties": False,
    "properties": {
        "email": {
            "title": "Email address",
            "type": "string",
            "format": "email",
            "minLength": 6,
            "maxLength": 20,
        }
    },
}


class ResultVerificationError(Exception):
    """Ошибка валидации результата выполнения функции."""

    def __init__(self, message: str, errors_list: Any):
        """Конструктор исключения."""
        super().__init__(message)
        self.errors_list = errors_list

    def __str__(self) -> str:
        return "Ошибка валидации результата: " + str(self.errors_list)


class InputVerificationError(Exception):
    """Ошибка валидации входных параметров функции."""

    def __init__(self, message: str, errors_list: Any):
        """Конструктор исключения."""
        super().__init__(message)
        self.errors_list = errors_list

    def __str__(self) -> str:
        return "Ошибка валидации входных параметров: " + str(self.errors_list)


class MyError(Exception):
    """Просто ошибка."""

    def __init__(self, message: str, errors_list: Any):
        """Конструктор исключения."""
        super().__init__(message)
        self.errors_list = errors_list

    def __str__(self) -> str:
        return "Открыт нулевой портал: " + str(self.errors_list)


def input_check(input_value: str) -> bool:
    """Проверяем входные параметры функции типа 'строка' в соответствии с шаблоном."""
    pattern = "^\\S+@\\S+\\.\\S+$"
    return bool(re.match(pattern, input_value))


def result_check(result: dict) -> bool:
    """Проверяем результат выполнения функции."""
    try:
        return not bool(jsonschema.validate(result, MY_SCHEMA))
    except jsonschema.ValidationError:
        return False


def default_func(a: int = 10, b: int = 5) -> None:
    """Вычисляем значение деления целых чисел."""
    print(f"При делении {a} на {b} получится", int(a / b))


def valid_all(
    input_validator: Callable,
    result_validator: Callable,
    on_fail_repeat_times: int = 1,
    default_behavior: Callable = None,
) -> Callable:
    """Декоратор для валидации входных параметров и результата выполнения функции."""

    def decorator_function(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                function_argument = [arg for arg in args]
                # Проверяем входные параметры функции под декоратором
                wright_input_return = all(input_validator(arg) for arg in args)
                # Если результат проверки отрицательный, вызываем ошибку
                if not wright_input_return:
                    raise InputVerificationError("Exception occur", function_argument)
                # Функция под декоратором
                function_result = func(*args, **kwargs)
                # Проверяем результат, который вернула функция под декоратором
                wright_result_return = result_validator(function_result)
                # В случае неудачной проверки, вызываем ошибку
                if not wright_result_return:
                    errors_occured = []
                    if on_fail_repeat_times >= 1:
                        for _ in range(on_fail_repeat_times):
                            function_result = func(*args, **kwargs)
                            errors_occured.append(
                                ResultVerificationError.__str__(
                                    ResultVerificationError("", function_result)
                                )
                            )
                        if default_behavior is not None:
                            default_behavior()
                            return function_result
                        raise ResultVerificationError(
                            "Exception occur", function_result
                        )
                    elif on_fail_repeat_times == 0:
                        raise MyError("Exception occur", on_fail_repeat_times)
                    else:
                        while not wright_result_return:
                            function_result = func(*args, **kwargs)
                return function_result
            # Исключение при провале проверки входных параметров функции
            except InputVerificationError:
                raise
            # Исключение при провале проверки результата выполнения функции
            except ResultVerificationError:
                raise
            # Самостоятельно написанное исключение
            except MyError:
                raise

        return wrapper

    return decorator_function


@valid_all(input_check, result_check)
def target_function(argument: str) -> dict:
    """Переданный в функцию строковый параметр возвращаем в значении словаря с заранее заданным ключом."""
    return {"email": str(argument)}


if __name__ == "__main__":
    try:
        print(target_function("user@innopolis.com"))
        sys.exit(0)
    except SystemExit:
        raise
