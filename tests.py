import unittest
from main import input_check, result_check, target_function, InputVerificationError, ResultVerificationError


class VallidAllTestCase(unittest.TestCase):

    def test_input_parameters(self):
        """Валидация строки по регулярному выражению."""
        self.assertTrue(input_check("user@innopolis.com"))

    def test_output_parameters(self):
        """Валидация входного json-параметра."""
        self.assertTrue(result_check({"email": "user@innopolis.com"}))

    def test_result(self):
        """Проверка валидации возвращаемого результата."""
        self.assertEqual(target_function("user@innopolis.com"), {"email": "user@innopolis.com"})

    def test_error_input(self):
        """Проверка возникновения исключения InputParameterVerificationError."""
        self.assertRaises(InputVerificationError, target_function, "a")

    def test_error_output(self):
        """Проверка возникновения исключения ResultVerificationError."""
        self.assertRaises(ResultVerificationError, target_function, "user777777777777777@innopolis.com")


if __name__ == '__main__':
    unittest.main()
