from sys import version_info
from .filecache import FileCache

__all__ = ["FileCache"]

if version_info.major == 2:
    from .finnpie2 import xor, lsb, xshift, rot13, brot, parity
    __all__.extend(["xor", "lsb", "xshift", "rot13", "brot", "parity"])
else:
    from .util import get_hashes_from_file, yield_hashes_from_file
    from .finnpie import xor, lsb, xshift, rot13, brot, parity
    __all__.extend(["xor", "lsb", "xshift", "rot13", "brot", "parity", "get_hashes_from_file", "yield_hashes_from_file"])
