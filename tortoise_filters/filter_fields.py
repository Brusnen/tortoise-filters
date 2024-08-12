from abc import ABC, abstractmethod
from typing import Callable
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
    available_expr = [None]

    def __init__(self, field_name: str, lookup_expr: str = None, value=None, method=None) -> None:
        self.value = value
        super().__init__(field_name, lookup_expr, method)

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
    available_expr = [None]

    def __init__(self, field_name: str, lookup_expr: str = None, value=None, method=None) -> None:
        self.value = value
        super().__init__(field_name, lookup_expr, method)

    def _kwargs_builder(self, value: list):
        if self.lookup_expr is not None:
            return {self.field_name + "__" + self.lookup_expr: value}
        return {self.field_name: value}

    async def filter_queryset(self, queryset: QuerySet, value) -> QuerySet:
        self.lookup_expr = 'range'
        return queryset


class DateFilter(BaseFieldFilter):
    """date filter"""


class NumberRangeFilter(BaseFieldFilter):
    """number filter"""


class DateRangeFilter(BaseFieldFilter):
    """date range filter"""


class DateTimeRangeFilter(BaseFieldFilter):
    """datetime range"""
