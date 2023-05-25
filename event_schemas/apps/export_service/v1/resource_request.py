from enum import Enum
from uuid import UUID
from typing import Dict, Any, Optional, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


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


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Format(Enum):
    """The format of the data to be exported"""
    CSV = "csv"
    JSON = "json"


class ResourceRequestClass:
    """A request for data to be exported"""
    """The application being requested"""
    application: str
    """The unique identifier of the export request that triggered the resource request"""
    export_request_uuid: UUID
    """The filters to be applied to the data"""
    filters: Optional[Dict[str, Any]]
    """The format of the data to be exported"""
    format: Format
    """The resource to be exported"""
    resource: str
    """A unique identifier for the resource request"""
    uuid: UUID
    """The Base64-encoded JSON identity header of the user making the request"""
    x_rh_identity: str

    def __init__(self, application: str, export_request_uuid: UUID, filters: Optional[Dict[str, Any]], format: Format, resource: str, uuid: UUID, x_rh_identity: str) -> None:
        self.application = application
        self.export_request_uuid = export_request_uuid
        self.filters = filters
        self.format = format
        self.resource = resource
        self.uuid = uuid
        self.x_rh_identity = x_rh_identity

    @staticmethod
    def from_dict(obj: Any) -> 'ResourceRequestClass':
        assert isinstance(obj, dict)
        application = from_str(obj.get("application"))
        export_request_uuid = UUID(obj.get("export_request_uuid"))
        filters = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("filters"))
        format = Format(obj.get("format"))
        resource = from_str(obj.get("resource"))
        uuid = UUID(obj.get("uuid"))
        x_rh_identity = from_str(obj.get("x-rh-identity"))
        return ResourceRequestClass(application, export_request_uuid, filters, format, resource, uuid, x_rh_identity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["application"] = from_str(self.application)
        result["export_request_uuid"] = str(self.export_request_uuid)
        if self.filters is not None:
            result["filters"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.filters)
        result["format"] = to_enum(Format, self.format)
        result["resource"] = from_str(self.resource)
        result["uuid"] = str(self.uuid)
        result["x-rh-identity"] = from_str(self.x_rh_identity)
        return result


class ResourceRequest:
    """Event data for data export requests"""
    """A request for data to be exported"""
    resource_request: ResourceRequestClass

    def __init__(self, resource_request: ResourceRequestClass) -> None:
        self.resource_request = resource_request

    @staticmethod
    def from_dict(obj: Any) -> 'ResourceRequest':
        assert isinstance(obj, dict)
        resource_request = ResourceRequestClass.from_dict(obj.get("resource_request"))
        return ResourceRequest(resource_request)

    def to_dict(self) -> dict:
        result: dict = {}
        result["resource_request"] = to_class(ResourceRequestClass, self.resource_request)
        return result


def resource_request_from_dict(s: Any) -> ResourceRequest:
    return ResourceRequest.from_dict(s)


def resource_request_to_dict(x: ResourceRequest) -> Any:
    return to_class(ResourceRequest, x)
