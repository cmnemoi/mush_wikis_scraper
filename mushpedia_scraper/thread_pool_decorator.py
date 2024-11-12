from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
from functools import wraps
from typing import TypeVar, List

T = TypeVar("T")


def thread_pool(func):
    @wraps(func)
    def wrapper(self, items: List[str], *args, **kwargs) -> List[T]:
        max_workers = cpu_count() * 2
        results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_item = {executor.submit(self._scrap_page, item, *args, **kwargs): item for item in items}

            for future in as_completed(future_to_item):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    item = future_to_item[future]
                    print(f"Operation generated an exception for {item}: {exc}")

        return results

    return wrapper
