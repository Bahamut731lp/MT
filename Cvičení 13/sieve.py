def generate_primes_in_range(start, end):
    """Funkce implementující Eratosthenovo síto pro generování prvočísel v zadaném rozsahu

    Parameters
    ----------
    start
        Dolní mez
    end
        Horní mez

    Returns
    -------
        Pole prvočísel
    """

    primes = []
    is_prime = [True] * (end + 1)
    is_prime[0] = is_prime[1] = False

    for number in range(2, int(end**0.5) + 1):
        if is_prime[number]:
            primes.append(number)
            for multiple in range(number * number, end + 1, number):
                is_prime[multiple] = False

    primes.extend(number for number in range(max(2, int(end**0.5) + 1), end + 1) if is_prime[number])

    return [prime for prime in primes if prime >= start]

# Definujeme rozsah
start_range = 1000
end_range = 10000

# Generujeme prvočísla v daném rozsahu
result = generate_primes_in_range(start_range, end_range)