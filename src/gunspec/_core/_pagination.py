from __future__ import annotations

from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    TypeVar,
)

from ._http_client import PaginatedResponse, PaginationMeta

T = TypeVar("T")


class SyncPage(Generic[T]):
    """A single page of results from a paginated endpoint (synchronous).

    Provides ``items`` access, ``has_next_page`` check, ``next_page()``
    navigation, and ``__iter__`` that yields items on the current page.
    """

    def __init__(
        self,
        response: PaginatedResponse[T],
        base_query: Dict[str, Any],
        fetcher: Callable[[Dict[str, Any]], PaginatedResponse[T]],
    ) -> None:
        self.data: List[T] = response.data
        self.pagination: PaginationMeta = response.pagination
        self.request_id: str = response.request_id
        self._base_query = base_query
        self._fetcher = fetcher

    @property
    def items(self) -> List[T]:
        return self.data

    def has_next_page(self) -> bool:
        if self.pagination.total_pages is not None:
            return self.pagination.page < self.pagination.total_pages
        return len(self.data) >= self.pagination.limit

    def next_page(self) -> SyncPage[T]:
        if not self.has_next_page():
            raise StopIteration("No more pages available.")
        query = {**self._base_query, "page": self.pagination.page + 1}
        response = self._fetcher(query)
        return SyncPage(response, self._base_query, self._fetcher)

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)


class AsyncPage(Generic[T]):
    """A single page of results from a paginated endpoint (asynchronous).

    Provides ``items`` access, ``has_next_page`` check, ``next_page()``
    navigation, and ``__aiter__`` that yields items on the current page.
    """

    def __init__(
        self,
        response: PaginatedResponse[T],
        base_query: Dict[str, Any],
        fetcher: Callable[..., Any],
    ) -> None:
        self.data: List[T] = response.data
        self.pagination: PaginationMeta = response.pagination
        self.request_id: str = response.request_id
        self._base_query = base_query
        self._fetcher = fetcher

    @property
    def items(self) -> List[T]:
        return self.data

    def has_next_page(self) -> bool:
        if self.pagination.total_pages is not None:
            return self.pagination.page < self.pagination.total_pages
        return len(self.data) >= self.pagination.limit

    async def next_page(self) -> AsyncPage[T]:
        if not self.has_next_page():
            raise StopAsyncIteration("No more pages available.")
        query = {**self._base_query, "page": self.pagination.page + 1}
        response = await self._fetcher(query)
        return AsyncPage(response, self._base_query, self._fetcher)

    async def __aiter__(self) -> AsyncIterator[T]:
        for item in self.data:
            yield item
