from OpenGL import GL


class BlockVar:

    def __init__(self, blocks, name: str) -> None:
        self._blocks = blocks
        self._name: str = name
        self._bound_var: object = None
        self._binding_point: int = 0

        atom_info_list = blocks.info[self._name].atoms
        if not atom_info_list:
            return

        self._atom_info_map = {}

        structure_key_list = []
        for atom_info in atom_info_list:
            atom_name = atom_info.name
            self._atom_info_map[atom_name] = atom_info
            structure_key_list.append(
                "(" + atom_info.type + ", " + atom_name + ")"
            )
        self._structure_key: str = ", ".join(structure_key_list)

    @property
    def blocks(self):
        return self._blocks

    def bind(self, var: object) -> None:
        if var is self._bound_var:
            return

        if var is None:
            self.unbind()
            return

        self.unbind()

        cls = self.blocks.__class__
        id_var = id(var)
        if id_var not in cls._bound_vars:
            cls._bound_vars[id_var] = {}

        if self._structure_key not in cls._bound_vars[id_var]:
            ssubo = cls.BO()
            ssubo._bound_var = var
            cls._bound_vars[id_var][self._structure_key] = ssubo
        ssubo = cls._bound_vars[id_var][self._structure_key]

        ssubo._atom_info_map = self._atom_info_map
        ssubo._bound_block_vars.add(self)

        self._bound_var = var

    def unbind(self) -> None:
        if self._bound_var is None:
            return

        id_var = id(self._bound_var)
        cls = self.blocks.__class__

        if (
            id_var not in cls._bound_vars
            or self._structure_key not in cls._bound_vars[id_var]
        ):
            return

        ssubo = cls._bound_vars[id_var][self._structure_key]
        if self in ssubo._bound_block_vars:
            ssubo._bound_block_vars.remove(self)
        if not ssubo._bound_block_vars:
            ssubo.unbind_from_point()

        self._bound_var = None
        self._binding_point = 0

    def binding_point(self) -> int:
        return self._binding_point

    def __del__(self) -> None:
        try:
            self.unbind()
        except:
            pass

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other) -> bool:
        return id(self) == id(other)

    def bind_to_point(self, binding_point: int) -> None:
        if binding_point < 0:
            return

        if self._binding_point == binding_point:
            return

        blocks = self.blocks
        cls_name = blocks.__class__.__name__
        if cls_name == "UniformBlocks":
            GL.glUniformBlockBinding(
                blocks.program.id,
                blocks.info[self._name].index,
                binding_point,
            )
        elif cls_name == "ShaderStorageBlocks":
            GL.glShaderStorageBlockBinding(
                blocks.program.id,
                blocks.info[self._name].index,
                binding_point,
            )

        self._binding_point = binding_point

    def upload(self, force_upload: bool = False) -> None:
        if self._bound_var is None:
            return

        cls = self.blocks.__class__
        id_var = id(self._bound_var)
        if id_var not in cls._bound_vars:
            return

        if self._structure_key not in cls._bound_vars[id_var]:
            return

        ssubo = cls._bound_vars[id_var][self._structure_key]
        assert self in ssubo._bound_block_vars

        if force_upload:
            ssubo.upload(force_upload)
        elif hasattr(self._bound_var, "upload"):
            self._bound_var.upload()

        binding_point = ssubo.bind_to_point(force_bind=False)
        self.bind_to_point(binding_point)
