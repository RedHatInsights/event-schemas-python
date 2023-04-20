from uuid import UUID
from typing import Any, List, Optional, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Policy:
    condition: str
    description: str
    id: UUID
    name: str
    url: str

    def __init__(self, condition: str, description: str, id: UUID, name: str, url: str) -> None:
        self.condition = condition
        self.description = description
        self.id = id
        self.name = name
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'Policy':
        assert isinstance(obj, dict)
        condition = from_str(obj.get("condition"))
        description = from_str(obj.get("description"))
        id = UUID(obj.get("id"))
        name = from_str(obj.get("name"))
        url = from_str(obj.get("url"))
        return Policy(condition, description, id, name, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["condition"] = from_str(self.condition)
        result["description"] = from_str(self.description)
        result["id"] = str(self.id)
        result["name"] = from_str(self.name)
        result["url"] = from_str(self.url)
        return result


class RHELSystemTag:
    key: str
    namespace: str
    value: str

    def __init__(self, key: str, namespace: str, value: str) -> None:
        self.key = key
        self.namespace = namespace
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'RHELSystemTag':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        namespace = from_str(obj.get("namespace"))
        value = from_str(obj.get("value"))
        return RHELSystemTag(key, namespace, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["namespace"] = from_str(self.namespace)
        result["value"] = from_str(self.value)
        return result


class System:
    """A RHEL system managed by console.redhat.com"""
    """Timestamp of when the system did a check in. Must adhere to RFC 3339."""
    check_in: datetime
    display_name: str
    tags: List[RHELSystemTag]
    host_url: Optional[str]
    hostname: Optional[str]
    inventory_id: str
    rhel_version: Optional[str]

    def __init__(self, check_in: datetime, display_name: str, tags: List[RHELSystemTag], host_url: Optional[str], hostname: Optional[str], inventory_id: str, rhel_version: Optional[str]) -> None:
        self.check_in = check_in
        self.display_name = display_name
        self.tags = tags
        self.host_url = host_url
        self.hostname = hostname
        self.inventory_id = inventory_id
        self.rhel_version = rhel_version

    @staticmethod
    def from_dict(obj: Any) -> 'System':
        assert isinstance(obj, dict)
        check_in = from_datetime(obj.get("check_in"))
        display_name = from_str(obj.get("display_name"))
        tags = from_list(RHELSystemTag.from_dict, obj.get("tags"))
        host_url = from_union([from_str, from_none], obj.get("host_url"))
        hostname = from_union([from_str, from_none], obj.get("hostname"))
        inventory_id = from_str(obj.get("inventory_id"))
        rhel_version = from_union([from_str, from_none], obj.get("rhel_version"))
        return System(check_in, display_name, tags, host_url, hostname, inventory_id, rhel_version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["check_in"] = self.check_in.isoformat()
        result["display_name"] = from_str(self.display_name)
        result["tags"] = from_list(lambda x: to_class(RHELSystemTag, x), self.tags)
        if self.host_url is not None:
            result["host_url"] = from_union([from_str, from_none], self.host_url)
        if self.hostname is not None:
            result["hostname"] = from_union([from_str, from_none], self.hostname)
        result["inventory_id"] = from_str(self.inventory_id)
        if self.rhel_version is not None:
            result["rhel_version"] = from_union([from_str, from_none], self.rhel_version)
        return result


class PolicyTriggered:
    """Event data for triggered policies."""
    """Triggered policies for a system"""
    policies: List[Policy]
    system: System

    def __init__(self, policies: List[Policy], system: System) -> None:
        self.policies = policies
        self.system = system

    @staticmethod
    def from_dict(obj: Any) -> 'PolicyTriggered':
        assert isinstance(obj, dict)
        policies = from_list(Policy.from_dict, obj.get("policies"))
        system = System.from_dict(obj.get("system"))
        return PolicyTriggered(policies, system)

    def to_dict(self) -> dict:
        result: dict = {}
        result["policies"] = from_list(lambda x: to_class(Policy, x), self.policies)
        result["system"] = to_class(System, self.system)
        return result


def policy_triggered_from_dict(s: Any) -> PolicyTriggered:
    return PolicyTriggered.from_dict(s)


def policy_triggered_to_dict(x: PolicyTriggered) -> Any:
    return to_class(PolicyTriggered, x)
