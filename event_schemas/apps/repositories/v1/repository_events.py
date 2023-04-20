from typing import Optional, List, Any, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Repositories:
    distribution_arch: Optional[str]
    distribution_versions: Optional[List[Any]]
    failed_introspections_count: Optional[int]
    gpg_key: Optional[str]
    last_introspection_error: Optional[str]
    last_introspection_time: Optional[datetime]
    last_success_introspection_time: Optional[datetime]
    last_update_introspection_time: Optional[datetime]
    metadata_verification: Optional[bool]
    name: str
    package_count: Optional[int]
    status: Optional[str]
    url: str
    uuid: str

    def __init__(self, distribution_arch: Optional[str], distribution_versions: Optional[List[Any]], failed_introspections_count: Optional[int], gpg_key: Optional[str], last_introspection_error: Optional[str], last_introspection_time: Optional[datetime], last_success_introspection_time: Optional[datetime], last_update_introspection_time: Optional[datetime], metadata_verification: Optional[bool], name: str, package_count: Optional[int], status: Optional[str], url: str, uuid: str) -> None:
        self.distribution_arch = distribution_arch
        self.distribution_versions = distribution_versions
        self.failed_introspections_count = failed_introspections_count
        self.gpg_key = gpg_key
        self.last_introspection_error = last_introspection_error
        self.last_introspection_time = last_introspection_time
        self.last_success_introspection_time = last_success_introspection_time
        self.last_update_introspection_time = last_update_introspection_time
        self.metadata_verification = metadata_verification
        self.name = name
        self.package_count = package_count
        self.status = status
        self.url = url
        self.uuid = uuid

    @staticmethod
    def from_dict(obj: Any) -> 'Repositories':
        assert isinstance(obj, dict)
        distribution_arch = from_union([from_str, from_none], obj.get("distribution_arch"))
        distribution_versions = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("distribution_versions"))
        failed_introspections_count = from_union([from_int, from_none], obj.get("failed_introspections_count"))
        gpg_key = from_union([from_str, from_none], obj.get("gpg_key"))
        last_introspection_error = from_union([from_str, from_none], obj.get("last_introspection_error"))
        last_introspection_time = from_union([from_datetime, from_none], obj.get("last_introspection_time"))
        last_success_introspection_time = from_union([from_datetime, from_none], obj.get("last_success_introspection_time"))
        last_update_introspection_time = from_union([from_datetime, from_none], obj.get("last_update_introspection_time"))
        metadata_verification = from_union([from_bool, from_none], obj.get("metadata_verification"))
        name = from_str(obj.get("name"))
        package_count = from_union([from_int, from_none], obj.get("package_count"))
        status = from_union([from_str, from_none], obj.get("status"))
        url = from_str(obj.get("url"))
        uuid = from_str(obj.get("uuid"))
        return Repositories(distribution_arch, distribution_versions, failed_introspections_count, gpg_key, last_introspection_error, last_introspection_time, last_success_introspection_time, last_update_introspection_time, metadata_verification, name, package_count, status, url, uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.distribution_arch is not None:
            result["distribution_arch"] = from_union([from_str, from_none], self.distribution_arch)
        if self.distribution_versions is not None:
            result["distribution_versions"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.distribution_versions)
        if self.failed_introspections_count is not None:
            result["failed_introspections_count"] = from_union([from_int, from_none], self.failed_introspections_count)
        if self.gpg_key is not None:
            result["gpg_key"] = from_union([from_str, from_none], self.gpg_key)
        if self.last_introspection_error is not None:
            result["last_introspection_error"] = from_union([from_str, from_none], self.last_introspection_error)
        if self.last_introspection_time is not None:
            result["last_introspection_time"] = from_union([lambda x: x.isoformat(), from_none], self.last_introspection_time)
        if self.last_success_introspection_time is not None:
            result["last_success_introspection_time"] = from_union([lambda x: x.isoformat(), from_none], self.last_success_introspection_time)
        if self.last_update_introspection_time is not None:
            result["last_update_introspection_time"] = from_union([lambda x: x.isoformat(), from_none], self.last_update_introspection_time)
        if self.metadata_verification is not None:
            result["metadata_verification"] = from_union([from_bool, from_none], self.metadata_verification)
        result["name"] = from_str(self.name)
        if self.package_count is not None:
            result["package_count"] = from_union([from_int, from_none], self.package_count)
        if self.status is not None:
            result["status"] = from_union([from_str, from_none], self.status)
        result["url"] = from_str(self.url)
        result["uuid"] = from_str(self.uuid)
        return result


class RepositoryEvents:
    """Event data for Repository Events."""
    """List of repositories affected by the event"""
    repositories: List[Repositories]

    def __init__(self, repositories: List[Repositories]) -> None:
        self.repositories = repositories

    @staticmethod
    def from_dict(obj: Any) -> 'RepositoryEvents':
        assert isinstance(obj, dict)
        repositories = from_list(Repositories.from_dict, obj.get("repositories"))
        return RepositoryEvents(repositories)

    def to_dict(self) -> dict:
        result: dict = {}
        result["repositories"] = from_list(lambda x: to_class(Repositories, x), self.repositories)
        return result


def repository_events_from_dict(s: Any) -> RepositoryEvents:
    return RepositoryEvents.from_dict(s)


def repository_events_to_dict(x: RepositoryEvents) -> Any:
    return to_class(RepositoryEvents, x)
