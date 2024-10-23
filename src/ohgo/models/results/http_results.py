from dataclasses import dataclass
from typing import Dict


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
    etag: The etag of the query

    Methods:
    next_page: Returns the next page of results
    """

    _next_page: str = None

    def __init__(self, status_code: int, message: str = "", data: Dict = None, etag: str = None):
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
        self.etag = etag

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


@dataclass
class CachedResult:
    status_code: int = 304
    message: str = "Data has not changed since the last request"
    etag: str = None