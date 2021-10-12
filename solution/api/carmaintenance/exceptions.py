class EnoughGasException(Exception):
    def __init__(self, message="The car should NOT be refueled before it has less than 5% gas on tank"):
        self.message = message
        super().__init__(self.message)


class NotSwappabledTyresException(Exception):
    def __init__(self, message="A car's tyre should NOT be swapped before it hits more than 94% degradation"):
        self.message = message
        super().__init__(self.message)


class EnoughUsableTyresException(Exception):
    def __init__(self, message="A tyre should NOT be created while there is 4 usable tyres with less than 95% degradation"):
        self.message = message
        super().__init__(self.message)


class NotUsableCarException(Exception):
    def __init__(self, message="The car cannot travel without gas or one of its tyres"):
        self.message = message
        super().__init__(self.message)
