import datetime
from abc import ABC, abstractmethod
from typing import Callable, List, Annotated, Union, Any

from fastapi.params import Query
from tortoise.queryset import QuerySet
from tortoise.models import Model


class BaseFieldFilter(ABC):
    available_expr = None

    def __init__(self, field_name: str, lookup_expr: str, method: Callable = None) -> None:
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.method = method

    @abstractmethod
    async def filter_queryset(self, queryset: QuerySet, value) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def to_internal_value(self):
        raise NotImplementedError

    @classmethod
    def to_dependencies(cls):
        return cls.__class__.__annotations__

    def _kwargs_builder(self, value):
        if self.lookup_expr is not None:
            return {self.field_name + "__" + self.lookup_expr: value}
        return {self.field_name: value}

    def _check_lookup_exr(self):
        if self.lookup_expr not in list(self.available_expr):
            raise Exception(f'Invalid lookup expression: {self.lookup_expr}')

    def _method_filter(self, *args, **kwargs) -> QuerySet[Model]:
        pass


class NumberFilter(BaseFieldFilter):
    value: int

    available_expr = ['gt', 'gte', 'lt', 'lte', None]

    def __init__(self, field_name: str, lookup_expr: str = None, value=None, method=None) -> None:
        self.value: int = value
        super().__init__(field_name, lookup_expr, method)

    def to_internal_value(self):
        try:
            int(self.value)
        except TypeError:
            raise TypeError('Invalid type')

    async def filter_queryset(self, queryset: QuerySet[Model], value) -> QuerySet[Model]:
        if self.value is None:
            return queryset
        self._check_lookup_exr()
        self.to_internal_value()
        kwargs = self._kwargs_builder(value)
        queryset = queryset.filter(**kwargs)
        return queryset


class CharFilter(BaseFieldFilter):
    value: str

    available_expr = ['iexact', 'exact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith',
                      None]

    def __init__(self, field_name: str, lookup_expr: str = None, value=None, method=None) -> None:
        self.value = value
        super().__init__(field_name, lookup_expr, method)

    def to_internal_value(self):
        try:
            str(self.value)
        except TypeError:
            raise TypeError('Invalid type')

    async def filter_queryset(self, queryset: QuerySet, value) -> QuerySet:
        if self.value is None:
            return queryset
        self._check_lookup_exr()
        self.to_internal_value()
        kwargs = self._kwargs_builder(value)
        queryset = queryset.filter(**kwargs)
        return queryset


class InFilter(BaseFieldFilter):
    value: str

    available_expr = [None]

    def __init__(self, field_name: str, lookup_expr: str = None, value=None, method=None, type_field=int) -> None:
        self.value = value
        self._annotations = {'value': Annotated[Union[List[type_field], None], Query(...)]}
        super().__init__(field_name, lookup_expr, method)

    @property
    def __annotations__(self):
        return self._annotations

    def to_internal_value(self):
        if not isinstance(self.value, list):
            raise TypeError(f'Invalid type')

    async def filter_queryset(self, queryset: QuerySet, value) -> QuerySet:
        if self.value is None:
            return queryset
        self.lookup_expr = 'in'
        self.to_internal_value()
        kwargs = self._kwargs_builder(value)
        queryset = queryset.filter(**kwargs)
        return queryset


class DateTimeFilter(BaseFieldFilter):
    available_expr = [
        'exact',
        'iexact',
        'contains',
        'icontains',
        'gt',
        'gte',
        'lt',
        'lte',
        'range',
        'isnull',
        'year',
        'month',
        'day',
        'week_day',
        'hour',
        'minute',
        'second',
        None
    ]

    value: datetime.datetime

    def __init__(self, field_name: str, lookup_expr: str = None, value=None, method=None) -> None:
        self.value = value
        super().__init__(field_name, lookup_expr, method)

    def to_internal_value(self):
        if not isinstance(self.value, datetime.datetime):
            raise TypeError(f'Invalid type')

    def _kwargs_builder(self, value: datetime.datetime):
        if self.lookup_expr is not None:
            return {self.field_name + "__" + self.lookup_expr: value}
        return {self.field_name: value}

    async def filter_queryset(self, queryset: QuerySet, value) -> QuerySet:
        if self.value is None:
            return queryset
        self._check_lookup_exr()
        self.to_internal_value()
        kwargs = self._kwargs_builder(value)
        queryset = queryset.filter(**kwargs)
        return queryset


class DateFilter(BaseFieldFilter):
    available_expr = [
        'exact',
        'iexact',
        'contains',
        'icontains',
        'gt',
        'gte',
        'lt',
        'lte',
        'range',
        'isnull',
        'year',
        'month',
        'day',
        'week_day',
        'hour',
        'minute',
        'second',
        None
    ]

    value: datetime.date

    def __init__(self, field_name: str, lookup_expr: str = None, value=None, method=None) -> None:
        self.value = value
        super().__init__(field_name, lookup_expr, method)

    def to_internal_value(self):
        if not isinstance(self.value, datetime.date):
            raise TypeError(f'Invalid type')

    def _kwargs_builder(self, value: datetime.date):
        if self.lookup_expr is not None:
            return {self.field_name + "__" + self.lookup_expr: value}
        return {self.field_name: value}

    async def filter_queryset(self, queryset: QuerySet, value) -> QuerySet:
        if self.value is None:
            return queryset
        self._check_lookup_exr()
        self.to_internal_value()
        kwargs = self._kwargs_builder(value)
        queryset = queryset.filter(**kwargs)
        return queryset

class BaseRangeFilter(BaseFieldFilter):
    value_min: int
    value_max: int

    def __init__(self, field_name: str, lookup_expr: str, method: Callable = None) -> None:
        super().__init__(field_name, lookup_expr, method)


class NumberRangeFilter(BaseRangeFilter):

    value_min = int
    value_max = int

    available_expr = ['gte', 'gt', None]

    def __init__(self, field_name: str, lookup_expr: str = None, value=None, method=None) -> None:
        self.value: int = value
        super().__init__(field_name, lookup_expr, method)

    def to_internal_value(self):
        try:
            int(self.value)
        except TypeError:
            raise TypeError('Invalid type')

    def _kwargs_builder(self, value: int):
        if self.lookup_expr is not None:
            return {self.field_name + "__" + self.lookup_expr: value}
        return {self.field_name: value}

    async def filter_queryset(self, queryset: QuerySet[Model], value) -> QuerySet[Model]:
        if self.value is None:
            return queryset
        self._check_lookup_exr()
        self.to_internal_value()
        kwargs = self._kwargs_builder(value)
        queryset = queryset.filter(**kwargs)
        a = await queryset
        return queryset


class DateRangeFilter(BaseFieldFilter):
    value_min: datetime.date
    value_max: datetime.date

    available_expr = ['gte', 'lte', None]

    def __init__(
            self,
            field_name: str,
            lookup_expr: str = None,
            value_min: datetime.date = None,
            value_max: datetime.date = None,
            method: Callable = None
    ) -> None:
        self.value_min = value_min
        self.value_max = value_max
        super().__init__(field_name, lookup_expr, method)

    def to_internal_value(self):
        if self.value_min and not isinstance(self.value_min, datetime.date):
            raise TypeError("Invalid type for value_min. Expected a datetime.date instance.")
        if self.value_max and not isinstance(self.value_max, datetime.date):
            raise TypeError("Invalid type for value_max. Expected a datetime.date instance.")

    async def filter_queryset(self, queryset: QuerySet[Model], value: Any = None) -> QuerySet[Model]:
        self.to_internal_value()
        if self.value_min:
            queryset = queryset.filter(**{f"{self.field_name}__gte": self.value_min})
        if self.value_max:
            queryset = queryset.filter(**{f"{self.field_name}__lte": self.value_max})
        return queryset


class DateTimeRangeFilter(BaseFieldFilter):
    value_min: datetime.datetime
    value_max: datetime.datetime

    available_expr = ['gte', 'lte', None]

    def __init__(
            self,
            field_name: str,
            lookup_expr: str = None,
            value_min: datetime.datetime = None,
            value_max: datetime.datetime = None,
            method: Callable = None
    ) -> None:
        self.value_min = value_min
        self.value_max = value_max
        super().__init__(field_name, lookup_expr, method)

    def to_internal_value(self):
        if self.value_min and not isinstance(self.value_min, datetime.datetime):
            raise TypeError("Invalid type for value_min. Expected a datetime.datetime instance.")
        if self.value_max and not isinstance(self.value_max, datetime.datetime):
            raise TypeError("Invalid type for value_max. Expected a datetime.datetime instance.")

    async def filter_queryset(self, queryset: QuerySet[Model], value: Any = None) -> QuerySet[Model]:
        self.to_internal_value()
        if self.value_min:
            queryset = queryset.filter(**{f"{self.field_name}__gte": self.value_min})
        if self.value_max:
            queryset = queryset.filter(**{f"{self.field_name}__lte": self.value_max})
        return queryset


class MethodFilter(BaseFieldFilter):
    """
    Custom method-based filter allowing complex filtering logic.

    This filter enables defining custom filtering methods that can
    implement more complex querying logic beyond simple field comparisons.
    """
    available_expr = [None]
    value: Any

    def __init__(
            self,
            field_name: str,
            method: Callable[[QuerySet, Any], QuerySet],
            value: Any = None
    ):
        """
        Initialize a method-based filter.

        Args:
            field_name: Name of the field (used for identification)
            method: Custom filtering method
            value: Value to be used in filtering (optional)
        """
        self.value = value
        super().__init__(field_name, method=method)

    def to_internal_value(self):
        """
        Validate the method filter (no type checking by default).
        """
        pass

    async def filter_queryset(self, queryset: QuerySet, value) -> QuerySet:
        """
        Apply the custom method filter to the queryset.

        Args:
            queryset: Original Tortoise ORM queryset
            value: Value to filter by

        Returns:
            Filtered queryset
        """
        if self.value is None:
            return queryset

        if self.method:
            return self.method(queryset, value)

        return queryset

