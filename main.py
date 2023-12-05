from types import MappingProxyType
from typing import Generator
from functools import cache
from collections import namedtuple
import logging

PARAMETERS = MappingProxyType(
    {
        "interval_start": int(1e5),
        "interval_length": int(1e6),
        "quantity_of_random_numbers": int(1e6),
    }
)
Factors = namedtuple("Factors", ["largest_prime_factor", "second_largest_prime_factor"])


def generate_random_number(
    *, seed: int, mod: int, multiplier: int, increment: int
) -> Generator[int, None, None]:
    while 1:
        yield seed
        seed = (multiplier * seed + increment) % mod


@cache
def is_prime(number: f"positive {int}") -> bool:
    assert type(number) is int
    assert number > 0
    for divisor in range(2, int(number**0.5) + 1):
        if number % divisor == 0:
            return False
    return number > 1


class NumberHasOnlyOnePrimeFactor(Exception):
    pass


@cache
def compute_last_2_prime_factors(number: f"positive {int}") -> Factors:
    factors = []
    for divisor in range(number, 1, -1):
        if is_prime(divisor) and number % divisor == 0:
            factors.append(divisor)
        if len(factors) == 2:
            return Factors(factors[0], factors[1])
    raise NumberHasOnlyOnePrimeFactor


@cache
def does_it_satisfy_golomb_dickman_condition(factors: Factors) -> bool:
    return factors.largest_prime_factor >= factors.second_largest_prime_factor**2


def symbol_of_small_lambda() -> chr:
    return chr(955)


def main(*args, **kwargs) -> None:
    g = generate_random_number(seed=1, mod=2**31, multiplier=134_775_813, increment=1)
    counter_favorable = counter_possible = 0

    next_g = None
    for _ in range(PARAMETERS["quantity_of_random_numbers"]):
        try:
            next_g = (
                next(g) % PARAMETERS["interval_length"] + PARAMETERS["interval_start"]
            )
            factors = compute_last_2_prime_factors(next_g)
            if does_it_satisfy_golomb_dickman_condition(factors):
                counter_favorable += 1
            counter_possible += 1
        except NumberHasOnlyOnePrimeFactor:
            logging.warning(f"Number {next_g} has only one factor.")
        logging.info(
            f"{symbol_of_small_lambda()}= {counter_favorable / counter_possible}"
        )


if __name__ == "__main__":
    """This algorithm approximates the Golomb-Dickman constant using pseudorandom numbers and
    prime divisors along with classical probability model."""
    logging.basicConfig(level=logging.INFO)

    main()
