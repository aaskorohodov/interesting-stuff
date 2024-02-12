class PrimeWithMultiple:
    def __init__(self, prime: int):
        self.prime: int = prime
        self.multiple: int = prime * prime

    def update_multiple(self) -> None:
        self.multiple += self.prime

    def __repr__(self):
        return f'{self.prime} ({self.multiple})'

    def __str__(self):
        return f'{self.prime} ({self.multiple})'


def is_prime(number: int) -> bool:
    if number == 1:
        return False
    if number == 2:
        return True

    number_two_is_prime = PrimeWithMultiple(2)
    primes_with_multiples = [number_two_is_prime]
    primes = {2, }

    for i in range(3, number + 1):
        smallest_multiples = []
        for prime in primes_with_multiples:
            if not smallest_multiples:
                smallest_multiples.append(prime)
                continue

            currently_smallest_multiple_prime = smallest_multiples[0]
            if currently_smallest_multiple_prime.multiple > prime.multiple:
                smallest_multiples = [prime]
            elif currently_smallest_multiple_prime.multiple == prime.multiple:
                smallest_multiples.append(prime)

        if i < smallest_multiples[0].multiple:
            this_is_prime = PrimeWithMultiple(i)
            primes_with_multiples.append(this_is_prime)
            primes.add(i)
            continue
        else:
            for smallest_multiple_prime in smallest_multiples:
                smallest_multiple_prime.update_multiple()

        if not (i % 1_000):
            print(i)

    if number in primes:
        return True


is_this_number_prime = 1_000_000
is_prime(is_this_number_prime)
