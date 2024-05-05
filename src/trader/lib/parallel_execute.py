from typing import List, Awaitable, Any
import asyncio


async def parallel_execute(funcs: List[Awaitable]) -> List[Any]:
    """Run multiple async function in parallel

    Args:
        funcs (List[Tuple[Callable, Tuple  |  None, Dict[str, Any]  |  None]]): _description_

    Returns:
        List[Any]: Each of the result
    """
    return await asyncio.gather(*[asyncio.ensure_future(func) for func in funcs])
