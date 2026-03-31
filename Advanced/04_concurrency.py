"""
04 - Concurrency: Threading, Multiprocessing, Asyncio
======================================================
This file covers:
  - threading.Thread for I/O-bound concurrency
  - threading.Lock for thread safety
  - concurrent.futures.ThreadPoolExecutor
  - multiprocessing.Process for CPU-bound tasks
  - concurrent.futures.ProcessPoolExecutor
  - asyncio for asynchronous I/O (async/await)

NOTE: Due to the GIL (Global Interpreter Lock), threads in Python do NOT
run Python code in true parallel — they are best for I/O-bound tasks.
Use multiprocessing for CPU-bound tasks.
"""

import threading
import multiprocessing
import concurrent.futures
import asyncio
import time
import queue

# ==============================================================================
# 1. THREADING — I/O-BOUND TASKS
# ==============================================================================

print("=" * 50)
print("THREADING")
print("=" * 50)

def download_task(url: str, result_store: list, index: int):
    """Simulate downloading from a URL (I/O-bound work)."""
    print(f"  Thread [{threading.current_thread().name}]: downloading {url}")
    time.sleep(0.1)   # simulate network latency
    result_store[index] = f"data_from_{url}"

urls = [f"https://example.com/page{i}" for i in range(1, 6)]

# Sequential (slow)
start = time.perf_counter()
results = [None] * len(urls)
for i, url in enumerate(urls):
    download_task(url, results, i)
seq_time = time.perf_counter() - start
print(f"  Sequential: {seq_time:.3f}s, results: {len(results)}")

# Threaded (fast for I/O)
results_threaded = [None] * len(urls)
threads = []
start = time.perf_counter()

for i, url in enumerate(urls):
    t = threading.Thread(
        target=download_task,
        args=(url, results_threaded, i),
        name=f"Downloader-{i+1}"
    )
    threads.append(t)
    t.start()

for t in threads:
    t.join()   # wait for all threads to complete

thread_time = time.perf_counter() - start
print(f"  Threaded:   {thread_time:.3f}s, results: {len(results_threaded)}")
print(f"  Speedup: {seq_time / thread_time:.1f}x")


# ==============================================================================
# 2. THREAD SAFETY WITH LOCK
# ==============================================================================

print("\n--- Thread Safety with Lock ---")

counter_unsafe = 0
counter_safe   = 0
lock = threading.Lock()

def increment_unsafe():
    global counter_unsafe
    for _ in range(10_000):
        counter_unsafe += 1   # NOT thread-safe: read-modify-write

def increment_safe():
    global counter_safe
    for _ in range(10_000):
        with lock:             # lock ensures only one thread at a time
            counter_safe += 1

# Run unsafe increment
threads = [threading.Thread(target=increment_unsafe) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"  Unsafe counter: {counter_unsafe} (expected: 50000, may differ)")

# Run safe increment
threads = [threading.Thread(target=increment_safe) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"  Safe counter:   {counter_safe} (expected: 50000, always correct)")


# ==============================================================================
# 3. concurrent.futures.ThreadPoolExecutor
# ==============================================================================

print("\n--- ThreadPoolExecutor ---")

def fetch(url: str) -> str:
    """Simulate fetching a URL."""
    time.sleep(0.05)
    return f"Response from {url}"

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    # map: applies fetch to each URL, maintains order
    responses = list(executor.map(fetch, urls))

print(f"  Got {len(responses)} responses via ThreadPoolExecutor")

# submit: get Future objects for more control
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(fetch, url): url for url in urls}
    for future in concurrent.futures.as_completed(futures):
        url = futures[future]
        try:
            result = future.result()
            print(f"  ✅ {result}")
        except Exception as e:
            print(f"  ❌ {url}: {e}")


# ==============================================================================
# 4. MULTIPROCESSING — CPU-BOUND TASKS
# ==============================================================================

print("\n--- Multiprocessing ---")

def cpu_bound_task(n: int) -> int:
    """Compute sum of squares (CPU-intensive)."""
    return sum(i * i for i in range(n))

numbers = [500_000, 600_000, 700_000, 800_000]

# Sequential
start = time.perf_counter()
seq_results = [cpu_bound_task(n) for n in numbers]
seq_time = time.perf_counter() - start
print(f"  Sequential: {seq_time:.3f}s")

# ProcessPoolExecutor (runs in separate processes — bypasses GIL)
start = time.perf_counter()
with concurrent.futures.ProcessPoolExecutor() as executor:
    mp_results = list(executor.map(cpu_bound_task, numbers))
mp_time = time.perf_counter() - start
print(f"  Multiprocessing: {mp_time:.3f}s")
print(f"  Results match: {seq_results == mp_results}")


# ==============================================================================
# 5. asyncio — ASYNCHRONOUS I/O
# ==============================================================================

print("\n--- asyncio ---")

async def async_fetch(url: str) -> str:
    """Simulate an async HTTP request."""
    await asyncio.sleep(0.1)   # non-blocking sleep (simulates I/O wait)
    return f"Async response from {url}"

async def fetch_all(urls: list) -> list:
    """Fetch all URLs concurrently using asyncio.gather."""
    tasks = [async_fetch(url) for url in urls]
    return await asyncio.gather(*tasks)

# Run the async event loop
start = time.perf_counter()
responses = asyncio.run(fetch_all(urls))
async_time = time.perf_counter() - start
print(f"  asyncio: {async_time:.3f}s, got {len(responses)} responses")

# More complex: async with semaphore for rate limiting
async def fetch_with_limit(url: str, sem: asyncio.Semaphore) -> str:
    async with sem:
        await asyncio.sleep(0.05)
        return f"Limited response: {url}"

async def main_limited():
    sem = asyncio.Semaphore(2)   # max 2 concurrent requests
    tasks = [fetch_with_limit(url, sem) for url in urls]
    return await asyncio.gather(*tasks)

limited = asyncio.run(main_limited())
print(f"  Rate-limited asyncio: {len(limited)} responses")


# ==============================================================================
# 6. WHEN TO USE WHICH
# ==============================================================================

print("\n--- When to Use Which ---")
guide = {
    "threading":        "I/O-bound tasks (network, disk, database) — limited by GIL",
    "multiprocessing":  "CPU-bound tasks (number crunching, image processing) — bypasses GIL",
    "asyncio":          "High-concurrency I/O (many concurrent network requests) — single thread",
    "concurrent.futures": "Simple parallel execution with thread or process pools",
}
for approach, desc in guide.items():
    print(f"  {approach:<22}: {desc}")
