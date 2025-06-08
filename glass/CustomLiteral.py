from typing import Any, Tuple, Type


class _CustomLiteralMeta(type):

    def __getitem__(cls, args: Tuple[Any, ...] | Any) -> Type:
        if not isinstance(args, tuple):
            args = (args,)
        name = f"CustomLiteral[{', '.join(map(repr, args))}]"
        new_cls = type.__new__(_CustomLiteralMeta, name, (), {"__args__": args})
        return new_cls

    def __instancecheck__(cls, instance: Any) -> bool:
        return any(instance == arg for arg in getattr(cls, "__args__", ()))
    
    def __contains__(cls, item: Any)->bool:
        return (item in cls.__args__)

class CustomLiteral(metaclass=_CustomLiteralMeta):

    def __class_getitem__(cls, args) -> Type:
        return _CustomLiteralMeta.__getitem__(cls, args)