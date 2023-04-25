from typing import Optional, List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
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


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Recipients:
    """Notification recipients. Should be in a top-level field named "notification_recipients\""""
    """Setting to true ignores all the user preferences on this Recipient setting (It doesn’t
    affect other configuration that an Administrator sets on their Notification settings).
    Setting to false honors the user preferences.
    """
    ignore_user_preferences: Optional[bool]
    """Setting to true sends an email to the administrators of the account. Setting to false
    sends an email to all users of the account.
    """
    only_admins: Optional[bool]
    """List of users to direct the notification to. This won’t override notification's
    administrators settings. Users list will be merged with other settings.
    """
    users: Optional[List[str]]

    def __init__(self, ignore_user_preferences: Optional[bool], only_admins: Optional[bool], users: Optional[List[str]]) -> None:
        self.ignore_user_preferences = ignore_user_preferences
        self.only_admins = only_admins
        self.users = users

    @staticmethod
    def from_dict(obj: Any) -> 'Recipients':
        assert isinstance(obj, dict)
        ignore_user_preferences = from_union([from_bool, from_none], obj.get("ignore_user_preferences"))
        only_admins = from_union([from_bool, from_none], obj.get("only_admins"))
        users = from_union([lambda x: from_list(from_str, x), from_none], obj.get("users"))
        return Recipients(ignore_user_preferences, only_admins, users)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ignore_user_preferences is not None:
            result["ignore_user_preferences"] = from_union([from_bool, from_none], self.ignore_user_preferences)
        if self.only_admins is not None:
            result["only_admins"] = from_union([from_bool, from_none], self.only_admins)
        if self.users is not None:
            result["users"] = from_union([lambda x: from_list(from_str, x), from_none], self.users)
        return result


class Notification:
    """Notification event. Appropriate when an event has no data aside from recipient settings.
    If the event requires data, then it should reference the Recipient object definition in a
    separate schema.
    """
    notification_recipients: Optional[Recipients]

    def __init__(self, notification_recipients: Optional[Recipients]) -> None:
        self.notification_recipients = notification_recipients

    @staticmethod
    def from_dict(obj: Any) -> 'Notification':
        assert isinstance(obj, dict)
        notification_recipients = from_union([Recipients.from_dict, from_none], obj.get("notification_recipients"))
        return Notification(notification_recipients)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.notification_recipients is not None:
            result["notification_recipients"] = from_union([lambda x: to_class(Recipients, x), from_none], self.notification_recipients)
        return result


def notification_from_dict(s: Any) -> Notification:
    return Notification.from_dict(s)


def notification_to_dict(x: Notification) -> Any:
    return to_class(Notification, x)
