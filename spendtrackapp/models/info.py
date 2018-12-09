from __future__ import annotations

from typing import Union

from django.db import models


class Info(models.Model):
    """A class used to stores information"""

    name = models.CharField(
        max_length=100,
        unique=True
    )
    """Name of the info"""

    value_type = models.CharField(
        max_length=1,
        choices=(('i', 'integer'), ('f', 'float'), ('s', 'string'), ('b', 'boolean'))
    )
    """Type of the info (integer, float, string or boolean)"""

    _value = models.CharField(
        max_length=500
    )
    """String represent the info"""

    _converter = {
        'i': int,
        'f': float,
        's': str,
        'b': lambda value: value[0] in ['t', 'T', '1'] if isinstance(value, str) else value
    }
    """A dictionary matches value_type to a str-to-value_type converter"""

    @property
    def value(self) -> Union[int, float, str, bool]:
        """
        Getter of _value
        Return the actual info in the correct type, NOT as a string as in database
        """
        return self._converter[self.value_type](self._value)

    @value.setter
    def value(self, v: Union[int, float, str, bool]) -> None:
        """
        Setter of _value
        Set convert v to string and set to self._value

        :raise ValueError if v is invalid
        """
        str_value = str(v)
        self._converter[self.value_type](str_value)
        self._value = str_value

    def __str__(self):
        return self.name + "=" + self._value

    @classmethod
    def get(cls, name) -> Info:
        """Get the actual info with the given name in the correct type"""
        return cls.objects.get(name=name)

    @classmethod
    def set(cls, name, value) -> Info:
        """
        Set value of the info with given name and save to database

        :raise ValueError if value is invalid
        """
        info = cls.get(name)
        info.value = value
        info.save()
        return info

    ##############################################################
    #                   OVERRIDDEN OPERATORS                     #
    ##############################################################

    # --------------------- --------------------------------------

    def __iadd__(self, other: Union[Info, float, int, str]) -> Info:
        add_value = other.value if isinstance(other, Info) else other
        self.value = self.value + add_value
        return self

    def __isub__(self, other: Union[Info, float, int, str]) -> Info:
        sub_value = other.value if isinstance(other, Info) else other
        self.value = self.value - sub_value
        return self

    def __imul__(self, other: Union[Info, float, int, str]) -> Info:
        mul = other.value if isinstance(other, Info) else other
        self.value = self.value * mul
        return self

    def __ifloordiv__(self, other: Union[Info, float, int, str]) -> Info:
        div_value = other.value if isinstance(other, Info) else other
        self.value = self.value / div_value
        return self

    def __itruediv__(self, other: Union[Info, float, int, str]) -> Info:
        div_value = other.value if isinstance(other, Info) else other
        self.value = self.value // div_value
        return self

    def __imod__(self, other: Union[Info, float, int, str]) -> Info:
        mod_value = other.value if isinstance(other, Info) else other
        self.value = self.value % mod_value
        return self

    # --------------------- --------------------------------------

    def __add__(self, other: Union[Info, float, int, str]) -> Union[float, int, str]:
        add_value = other.value if isinstance(other, Info) else other
        return self.value + add_value

    def __sub__(self, other: Union[Info, float, int, str]) -> Union[float, int, str]:
        sub_value = other.value if isinstance(other, Info) else other
        return self.value - sub_value

    def __mul__(self, other: Union[Info, float, int, str]) -> Union[float, int, str]:
        mul_value = other.value if isinstance(other, Info) else other
        return self.value * mul_value

    def __floordiv__(self, other: Union[Info, float, int]) -> Union[float, int]:
        div_value = other.value if isinstance(other, Info) else other
        return self.value / div_value

    def __truediv__(self, other: Union[Info, float, int]) -> Union[float, int]:
        div_value = other.value if isinstance(other, Info) else other
        return self.value // div_value

    def __mod__(self, other: Union[Info, float, int]) -> Union[float, int]:
        mod_value = other.value if isinstance(other, Info) else other
        return self.value % mod_value

    # --------------------- --------------------------------------

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        sub_value = other.value if isinstance(other, Info) else other
        return sub_value - self.value

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rfloordiv__(self, other):
        div_value = other.value if isinstance(other, Info) else other
        return div_value / self.value

    def __rtruediv__(self, other):
        div_value = other.value if isinstance(other, Info) else other
        return div_value // self.value

    def __rmod__(self, other):
        div_value = other.value if isinstance(other, Info) else other
        return div_value % self.value
