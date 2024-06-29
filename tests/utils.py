from typing import Any


def dummy_fn_factory(result: Any, sync: bool = True):
    def _dummy_fn(*_, **__):
        return result

    async def _dummy_fn_async(*_, **__):
        return result

    return _dummy_fn if sync else _dummy_fn_async
