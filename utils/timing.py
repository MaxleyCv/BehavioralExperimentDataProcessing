class UET:
    """
    UET is the measure of time that is used in this experiment.
    It is a timezone-dependent time in microseconds from the start of the day.
    """
    def __init__(self, timestamp: str):
        # Just to save the main culprit.
        self.__timestamp = timestamp
        self.__needs_shift = False
        self.__uet = self._split_hh_mm_ss_us(timestamp)

    @staticmethod
    def from_integer(uet: int):
        """
        An alternative constructor to construct UET from an integer.
        :param uet: a formalized uet. Make sure it is in the same UET space
        :return: UET instance
        """
        us = uet % 10 ** 6
        uet //= 10 ** 6
        s = uet % 60
        uet //= 60
        m = uet % 60
        h = uet // 60
        return UET(f"{h}:{m}:{s}.{us}")

    def __str__(self):
        return str(self.__uet)

    def __call__(self, *args, **kwargs) -> int:
        """
        Get the value of the UET itself as an integer
        """
        return self.__uet

    def __cmp__(self, other) -> int:
        if isinstance(other, UET):
            return self() - other()
        else:
            raise ValueError("Sorry. Not the valid UET to compare.")

    def __add__(self, other):
        if isinstance(other, int):
            return UET.from_integer(self.__uet + other)
        elif isinstance(other, UET):
            return UET.from_integer(self.__uet + other())
        else:
            raise ValueError("To add UETs they should be ints or UETs. Only right side adds count for ints.")

    def __sub__(self, other) -> int:
        """
        Returns the time difference between two UETs
        :param other:
        :return:
        """
        if isinstance(other, UET):
            return self.__uet - other()
        elif isinstance(other, int):
            return self.__uet - other
        else:
            raise ValueError("UETs are only subtracted with int or UET")

    def shift(self, us: int) -> None:
        if self.__needs_shift:
            self.__uet += us
        else:
            raise ValueError("This timestamp is not shiftable since it has microsecond data.")
        return  None

    def _split_hh_mm_ss_us(self, stamp) -> int:
        main_part, microseconds = stamp.split('.')
        h, m, s, us = 0, 0, 0, 0
        if len(microseconds) == 3:
            # This kind of assignment comes in TCP traffic analysis
            main_part = main_part.split('T')[1]
            h, m, s = map(int, main_part.split(':'))
            us = microseconds * 10 ** 3
        elif len(microseconds) == 0:
            # this comes from video timestamps. Can be used for their production.
            self.needs_shift = True
            h, m, s = map(int, main_part.split(':'))
        else:
            h, m, s = map(int, main_part.split(':'))
            us = int(microseconds)

        # Calculating number of microseconds
        uet = us + 10 ** 6 * (s + 60 * (m + 60 * h))
        return uet
