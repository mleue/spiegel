class Calculator:
    def __init__(self):
        self._last_result = None

    @property
    def last_result(self):
        return self._last_result

    def sum(self, a: float, b: float):
        self._last_result = a + b
        return self.last_result
