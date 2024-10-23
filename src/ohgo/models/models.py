from dataclasses import dataclass
from datetime import datetime
from typing import *

import dateutil.parser

T = TypeVar("T")


def from_str(x: Any) -> str:
    if x is None:
        return ""
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


class Link:
    """
    Link is a class for storing a link object.

    Attributes:
    href: The URL of the link
    rel: The relationship of the link to the object
    """
    href: str
    rel: str

    def __init__(self, href="", rel=""):
        """
        Initializes the Link object with the href and rel.
        :param href: The URL of the link
        :param rel: The relationship of the link to the object
        """
        self.href = href
        self.rel = rel

    @staticmethod
    def from_dict(obj: Any) -> "Link":
        assert isinstance(obj, dict)
        href = from_str(obj.get("href"))
        rel = from_str(obj.get("rel"))
        return Link(href, rel)

    def to_dict(self) -> dict:
        result: dict = {"href": from_str(self.href), "rel": from_str(self.rel)}
        return result
