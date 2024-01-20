from multiprocessing import cpu_count, Pool
from time import time
import concurrent.futures


def factorize(*numbers):
    result = tuple()

    for number in numbers:
        factors = []
        divider = 1

        while True:
            if divider > number:
                break

            if number % divider == 0:
                factors.append(divider)

            divider += 1

        result = result + tuple([factors])

    return result


numbers = (10651060,) * cpu_count()


if __name__ == "__main__":
    start_time = time()
    factorize(*numbers)
    print(f"Sync execution time: {time() - start_time}")

    start_time = time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(numbers)) as executor:
        executor.map(factorize, numbers)

    print(f"Thread execution time: {time() - start_time}")

    start_time = time()

    with Pool(processes=cpu_count()) as pool:
        pool.map(factorize, numbers)

    print(f"Process execution time: {time() - start_time}")
