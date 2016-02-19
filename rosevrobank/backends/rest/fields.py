import datetime
from decimal import Decimal
import types


class Field(object):
    def to_python(self, value):
        return value

    def from_python(self, value):
        return value


class MoneyField(Field):
    def to_python(self, value):
        value = int(value)
        return Decimal(value) / Decimal('100')

    def from_python(self, value):
        if isinstance(value, (Decimal, types.FloatType)):
            value = int(value * 100)
        else:
            raise AttributeError('Value must be float or decimal types')
        return value


class BaseDatetimeField(Field):
    format = None
    type_ = datetime.datetime

    def to_python(self, value):
        return self.type_.strptime(value, self.format)

    def from_python(self, value):
        if not isinstance(value, self.type_):
            try:
                self.to_python(value)
            except:
                raise AttributeError(value)
        return value.strftime(self.format)


class DateTimeField(BaseDatetimeField):
    format = "%Y-%m-%d'T'%H:%M:%S"


class TimestampField(Field):
    def to_python(self, value):
        value = int(str(value)[:-3])
        return datetime.datetime.fromtimestamp(value)

    def from_python(self, value):
        return value.strftime('%s')


class CardDateField(BaseDatetimeField):
    format = '%Y%m'
    type_ = datetime.date
