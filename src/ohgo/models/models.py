from datetime import datetime
from typing import *

import dateutil.parser

T = TypeVar("T")


class Result:
    """
    Result is a class for storing the results of an OHGO API query.

    Attributes:
    status_code: The status code of the query as an integer
    message: The message returned from the query
    links: The links returned from the query
    total_result_count: The total number of results returned from the query
    data: The results returned from the query. Each result is a dictionary. Default is an empty list
    rejected_filters: The rejected filters returned from the query. Default is an empty list
    _next_page: The next page of results

    Methods:
    next_page: Returns the next page of results
    """

    _next_page: str = None

    def __init__(self, status_code: int, message: str = "", data: Dict = None):
        """
        Initializes the Result object with the status code, message, and data.
        :param status_code: The response status code
        :param message: The response message
        :param data: The response data
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.links = data['links']
        self.total_result_count = data['totalResultCount']
        self.data = data['results'] if data else []
        self.rejected_filters = data['rejectedFilters']

    @property
    def next_page(self):
        """
        Returns the next page of results
        :return: If there is a next page, returns the URL of the next page. Otherwise, returns None
        """
        if not self._next_page:
            for link in self.links:
                if link['rel'] == 'next-page':
                    self._next_page = link['href']
        return self._next_page


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
