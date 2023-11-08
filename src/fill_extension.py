from solid2 import register_access_syntax
from solid2.core.object_base import OpenSCADObject

@register_access_syntax
class fill(OpenSCADObject):
    def __init__(self) -> None:
        super().__init__('fill', {})
