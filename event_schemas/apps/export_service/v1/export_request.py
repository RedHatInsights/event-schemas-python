from enum import Enum
from typing import Dict, Any, Optional, TypeVar, Callable, Type, cast
from uuid import UUID


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


class ExportRequestClass:
    """A request for data to be exported"""
    """The application being requested"""
    application: str
    """The filters to be applied to the data"""
    filters: Optional[Dict[str, Any]]
    """The format of the data to be exported"""
    format: Format
    """The resource to be exported"""
    resource: str
    """A unique identifier for the request"""
    uuid: UUID
    """The Base64-encoded JSON identity header of the user making the request"""
    x_rh_identity: str

    def __init__(self, application: str, filters: Optional[Dict[str, Any]], format: Format, resource: str, uuid: UUID, x_rh_identity: str) -> None:
        self.application = application
        self.filters = filters
        self.format = format
        self.resource = resource
        self.uuid = uuid
        self.x_rh_identity = x_rh_identity

    @staticmethod
    def from_dict(obj: Any) -> 'ExportRequestClass':
        assert isinstance(obj, dict)
        application = from_str(obj.get("application"))
        filters = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("filters"))
        format = Format(obj.get("format"))
        resource = from_str(obj.get("resource"))
        uuid = UUID(obj.get("uuid"))
        x_rh_identity = from_str(obj.get("x-rh-identity"))
        return ExportRequestClass(application, filters, format, resource, uuid, x_rh_identity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["application"] = from_str(self.application)
        if self.filters is not None:
            result["filters"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.filters)
        result["format"] = to_enum(Format, self.format)
        result["resource"] = from_str(self.resource)
        result["uuid"] = str(self.uuid)
        result["x-rh-identity"] = from_str(self.x_rh_identity)
        return result


class ExportRequest:
    """Event data for data export requests."""
    """A request for data to be exported"""
    export_request: ExportRequestClass

    def __init__(self, export_request: ExportRequestClass) -> None:
        self.export_request = export_request

    @staticmethod
    def from_dict(obj: Any) -> 'ExportRequest':
        assert isinstance(obj, dict)
        export_request = ExportRequestClass.from_dict(obj.get("exportRequest"))
        return ExportRequest(export_request)

    def to_dict(self) -> dict:
        result: dict = {}
        result["exportRequest"] = to_class(ExportRequestClass, self.export_request)
        return result


def export_request_from_dict(s: Any) -> ExportRequest:
    return ExportRequest.from_dict(s)


def export_request_to_dict(x: ExportRequest) -> Any:
    return to_class(ExportRequest, x)
