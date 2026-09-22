from __future__ import annotations

from typing import Optional, Union

from ._core._auth import UNSET, AuthScheme, _Unset
from ._core._etag_cache import ETagStore
from ._core._http_client import (
    AsyncHttpClient,
    HttpClientConfig,
    SyncHttpClient,
)
from ._core._retry import RetryConfig
from ._resources import (
    Ammunition,
    AsyncAmmunition,
    AsyncAttachments,
    AsyncCalibers,
    AsyncCategories,
    AsyncCollections,
    AsyncConflicts,
    AsyncContent,
    AsyncCountries,
    AsyncDataQuality,
    AsyncDocs,
    AsyncFavorites,
    AsyncFirearms,
    AsyncGame,
    AsyncGameStats_,
    AsyncInterfaces,
    AsyncManufacturers,
    AsyncPlatforms,
    AsyncReports,
    AsyncStats,
    AsyncSupport,
    AsyncUsage,
    AsyncVendor,
    AsyncWebhooks,
    Attachments,
    Calibers,
    Categories,
    Collections,
    Conflicts,
    Content,
    Countries,
    DataQuality,
    Docs,
    Favorites,
    Firearms,
    Game,
    GameStats_,
    Interfaces,
    Manufacturers,
    Platforms,
    Reports,
    Stats,
    Support,
    Usage,
    Vendor,
    Webhooks,
)
from ._version import __version__


def _config(
    api_key: Union[str, _Unset, None],
    base_url: Optional[str],
    timeout: Optional[float],
    retry: Optional[RetryConfig],
    default_headers: Optional[dict[str, str]],
    auth_scheme: AuthScheme,
    etag_cache: Union[bool, ETagStore, None],
    allow_insecure: bool,
) -> HttpClientConfig:
    return HttpClientConfig(
        base_url=base_url or "https://api.gunspec.io",
        timeout=timeout or 30.0,
        api_key=api_key,
        retry=retry or RetryConfig(),
        auth_scheme=auth_scheme,
        etag_cache=etag_cache,
        allow_insecure=allow_insecure,
        headers={
            **(default_headers or {}),
            "User-Agent": f"gunspec-sdk/python/{__version__}",
            "X-SDK-Version": __version__,
            "X-SDK-Language": "python",
        },
    )


class GunSpec:
    """Synchronous GunSpec.io API client.

    Example::

        from gunspec import GunSpec

        client = GunSpec(api_key="gs_...")

        # List firearms
        result = client.firearms.list({"category": "pistol"})
        for firearm in result.data:
            handle(firearm)

        client = GunSpec(etag_cache=True)   # hold ETags; a 304 skips the daily cap

        # Context manager for clean shutdown
        with GunSpec() as client:
            data = client.firearms.get("glock-g17")

    An omitted ``api_key`` falls back to ``GUNSPEC_API_KEY``; an explicit
    ``api_key=None`` is anonymous on purpose (no header, environment ignored).
    A key is refused over plain ``http://`` to anything but localhost unless
    ``allow_insecure=True``.
    """

    firearms: Firearms
    manufacturers: Manufacturers
    calibers: Calibers
    categories: Categories
    stats: Stats
    game: Game
    game_stats: GameStats_
    ammunition: Ammunition
    countries: Countries
    conflicts: Conflicts
    content: Content
    docs: Docs
    collections: Collections
    attachments: Attachments
    interfaces: Interfaces
    platforms: Platforms
    vendor: Vendor
    data_quality: DataQuality
    favorites: Favorites
    reports: Reports
    support: Support
    webhooks: Webhooks
    usage: Usage

    def __init__(
        self,
        *,
        api_key: Union[str, _Unset, None] = UNSET,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        retry: Optional[RetryConfig] = None,
        default_headers: Optional[dict[str, str]] = None,
        auth_scheme: AuthScheme = "x-api-key",
        etag_cache: Union[bool, ETagStore, None] = None,
        allow_insecure: bool = False,
    ) -> None:
        self._client = SyncHttpClient(
            _config(
                api_key, base_url, timeout, retry, default_headers, auth_scheme, etag_cache, allow_insecure
            )
        )

        self.firearms = Firearms(self._client)
        self.manufacturers = Manufacturers(self._client)
        self.calibers = Calibers(self._client)
        self.categories = Categories(self._client)
        self.stats = Stats(self._client)
        self.game = Game(self._client)
        self.game_stats = GameStats_(self._client)
        self.ammunition = Ammunition(self._client)
        self.countries = Countries(self._client)
        self.conflicts = Conflicts(self._client)
        self.content = Content(self._client)
        self.docs = Docs(self._client)
        self.collections = Collections(self._client)
        self.attachments = Attachments(self._client)
        self.interfaces = Interfaces(self._client)
        self.platforms = Platforms(self._client)
        self.vendor = Vendor(self._client)
        self.data_quality = DataQuality(self._client)
        self.favorites = Favorites(self._client)
        self.reports = Reports(self._client)
        self.support = Support(self._client)
        self.webhooks = Webhooks(self._client)
        self.usage = Usage(self._client)

    @property
    def is_authenticated(self) -> bool:
        """Whether a credential will be sent. The key itself is never exposed."""
        return self._client.is_authenticated

    @property
    def http(self) -> SyncHttpClient:
        """The low-level transport, for endpoints the resources do not cover yet."""
        return self._client

    def __repr__(self) -> str:
        return f"GunSpec({self._client!r})"

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> GunSpec:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncGunSpec:
    """Asynchronous GunSpec.io API client.

    Example::

        from gunspec import AsyncGunSpec

        async with AsyncGunSpec(api_key="gs_...") as client:
            result = await client.firearms.list({"category": "rifle"})
            for firearm in result.data:
                handle(firearm)
    """

    firearms: AsyncFirearms
    manufacturers: AsyncManufacturers
    calibers: AsyncCalibers
    categories: AsyncCategories
    stats: AsyncStats
    game: AsyncGame
    game_stats: AsyncGameStats_
    ammunition: AsyncAmmunition
    countries: AsyncCountries
    conflicts: AsyncConflicts
    content: AsyncContent
    docs: AsyncDocs
    collections: AsyncCollections
    attachments: AsyncAttachments
    interfaces: AsyncInterfaces
    platforms: AsyncPlatforms
    vendor: AsyncVendor
    data_quality: AsyncDataQuality
    favorites: AsyncFavorites
    reports: AsyncReports
    support: AsyncSupport
    webhooks: AsyncWebhooks
    usage: AsyncUsage

    def __init__(
        self,
        *,
        api_key: Union[str, _Unset, None] = UNSET,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        retry: Optional[RetryConfig] = None,
        default_headers: Optional[dict[str, str]] = None,
        auth_scheme: AuthScheme = "x-api-key",
        etag_cache: Union[bool, ETagStore, None] = None,
        allow_insecure: bool = False,
    ) -> None:
        self._client = AsyncHttpClient(
            _config(
                api_key, base_url, timeout, retry, default_headers, auth_scheme, etag_cache, allow_insecure
            )
        )

        self.firearms = AsyncFirearms(self._client)
        self.manufacturers = AsyncManufacturers(self._client)
        self.calibers = AsyncCalibers(self._client)
        self.categories = AsyncCategories(self._client)
        self.stats = AsyncStats(self._client)
        self.game = AsyncGame(self._client)
        self.game_stats = AsyncGameStats_(self._client)
        self.ammunition = AsyncAmmunition(self._client)
        self.countries = AsyncCountries(self._client)
        self.conflicts = AsyncConflicts(self._client)
        self.content = AsyncContent(self._client)
        self.docs = AsyncDocs(self._client)
        self.collections = AsyncCollections(self._client)
        self.attachments = AsyncAttachments(self._client)
        self.interfaces = AsyncInterfaces(self._client)
        self.platforms = AsyncPlatforms(self._client)
        self.vendor = AsyncVendor(self._client)
        self.data_quality = AsyncDataQuality(self._client)
        self.favorites = AsyncFavorites(self._client)
        self.reports = AsyncReports(self._client)
        self.support = AsyncSupport(self._client)
        self.webhooks = AsyncWebhooks(self._client)
        self.usage = AsyncUsage(self._client)

    @property
    def is_authenticated(self) -> bool:
        """Whether a credential will be sent. The key itself is never exposed."""
        return self._client.is_authenticated

    @property
    def http(self) -> AsyncHttpClient:
        """The low-level transport, for endpoints the resources do not cover yet."""
        return self._client

    def __repr__(self) -> str:
        return f"AsyncGunSpec({self._client!r})"

    async def aclose(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncGunSpec:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()
