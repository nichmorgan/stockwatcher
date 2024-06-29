from typing import Any


def dummy_fn_factory(result: Any = None, sync: bool = True):
    def dummy_fn(*_, **__):
        return result

    async def dummy_fn_async(*_, **__):
        return result

    return dummy_fn if sync else dummy_fn_async
