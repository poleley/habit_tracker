from dataclasses import dataclass
from typing import Any, Callable, TypeAlias, TypeVar

FromType = TypeVar("FromType", contravariant=True)
ToType = TypeVar("ToType", covariant=True)

MapFunc: TypeAlias = Callable[[FromType], ToType]
DefaultFactory: TypeAlias = Callable[[], Any]


@dataclass
class MapperEntry:
    map_func: MapFunc[Any, Any]
    save_ctx: bool


class Mapper:
    def __init__(self) -> None:
        self.registry: dict[Any, MapperEntry] = {}

    def register(
        self,
        from_cls: type[FromType],
        to_cls: type[ToType],
        map_func: MapFunc[FromType, ToType],
        save_ctx: bool = False,
    ) -> None:
        self.registry[(from_cls, to_cls)] = MapperEntry(map_func, save_ctx)

    def map(self, v: Any, to_cls: type[ToType], **kwargs: Any) -> ToType:
        entry = self.registry.get((type(v), to_cls))
        if not entry:
            raise RuntimeError(f"Mapper {type(v)} -> {type(v)} not found")
        converted = entry.map_func(v, **kwargs)
        if entry.save_ctx:
            converted._mapper_ctx = v
        return converted  # type: ignore


def get_context(
    obj: Any, default: Any = None, default_factory: DefaultFactory | None = None
) -> Any:
    attr = getattr(obj, "_mapper_ctx", None)
    if attr is None and default_factory:
        return default_factory()
    if attr is None and default is not None:
        return default
    return attr


mapper = Mapper()
