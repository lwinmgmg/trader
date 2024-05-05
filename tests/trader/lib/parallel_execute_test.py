import time
import asyncio
import pytest
from trader.lib.parallel_execute import parallel_execute


@pytest.mark.asyncio
async def test_parallel_execute():
    ...

    async def fun1():
        await asyncio.sleep(1)
        return 1

    async def fun2():
        await asyncio.sleep(2)
        return 2

    start_time = time.time()
    results = await parallel_execute([fun1(), fun2()])
    total_time_taken = time.time() - start_time
    assert int(total_time_taken) == 2
    assert results[0] == 1
    assert results[1] == 2
