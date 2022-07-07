from wasmtime import _ffi as ffi
from ._config import Config, setter_property as pw
from ._error import WasmtimeError

from bases import Object, __main__
makeapi = __main__.makeapi

class Engine(Object):
    __slots__ = ('__locked__', '__proxydict__')
    def __init__(self, config: Config = None):
        super().__init__()
        if config is None:
            self._ptr = ffi.wasm_engine_new()
        elif not isinstance(config, Config):
            raise TypeError("expected Config")
        elif not hasattr(config, '_ptr'):
            raise WasmtimeError("Config already used")
        else:
            self._ptr = ffi.wasm_engine_new_with_config(config._moveout(pw))
        self.lockdown(makeapi)

    def __del__(self) -> None:
        if hasattr(self, '_ptr'):
            ffi.wasm_engine_delete(self._ptr)
Engine.lockclass()
