import random
import time


def generate_secret_number() -> str:
    """Generuje náhodné 4místné číslo s unikátními číslicemi.
    První číslice nemůže být nula.
    """
    digits = list("0123456789")
    first = random.choice(digits[1:])  # první číslice 1-9
    digits.remove(first)                # odstraníme první číslici, aby se neopakovala
    remaining = random.sample(digits, 3)  # vybereme tři unikátní číslice
    number = first + "".join(remaining)
    return number


def validate_guess(guess: str) -> tuple[bool, str]:
    """Ověří, zda je tip hráče validní:
    - pouze číslice
    - délka přesně 4
    - první číslice není nula
    - číslice nejsou duplicitní
    """
    if not guess.isdigit():
        return False, "Only digits are allowed."
    if len(guess) != 4:
        return False, "Guess must be 4 digits."
    if guess[0] == "0":
        return False, "Number cannot start with zero."
    if len(set(guess)) != 4:
        return False, "Digits must be unique."
    return True, ""


def count_bulls_and_cows(secret: str, guess: str) -> tuple[int, int]:
    """Spočítá bulls a cows.
    
    - Bulls = správná číslice na správném místě
    - Cows = správná číslice, ale na špatném místě
    - Pozice, které jsou bulls, se nezapočítávají do cows
    """
    bulls = sum(s == g for s, g in zip(secret, guess))
    secret_rest = [s for s, g in zip(secret, guess) if s != g]
    guess_rest = [g for s, g in zip(secret, guess) if s != g]

    cows = 0
    for g in guess_rest:
        if g in secret_rest:
            cows += 1
            secret_rest.remove(g)
    return bulls, cows


def plural(word: str, n: int) -> str:
    """Vrátí slovo ve správném čísle podle počtu."""
    return f"{n} {word}" + ("" if n == 1 else "s")


def play_game() -> int:
    """Hraje jednu hru:
    - generuje tajné číslo
    - kontroluje tipy hráče
    - vypisuje bulls a cows
    - měří počet pokusů a čas
    - vrací počet pokusů
    """
    secret = generate_secret_number()
    attempts = 0
    start = time.time()

    print("\nHi there!")
    print("-" * 47)
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print("-" * 47)

    while True:
        guess = input("Enter a number: ").strip()
        valid, msg = validate_guess(guess)
        if not valid:
            print(msg)
            print("-" * 47)
            continue

        attempts += 1
        bulls, cows = count_bulls_and_cows(secret, guess)
        print(f"{plural('bull', bulls)}, {plural('cow', cows)}")
        print("-" * 47)

        if bulls == 4:
            elapsed = round(time.time() - start)
            print("Correct, you've guessed the right number")
            print(f"in {attempts} guesses!")
            print("-" * 47)
            print(f"That's amazing! You needed {elapsed} seconds.")
            break

    return attempts


def main() -> None:
    """Opakuje hry a uchovává statistiku počtu pokusů."""
    stats = []
    while True:
        attempts = play_game()
        stats.append(attempts)

        again = input("Do you want to play again? (y/n): ").strip().lower()
        if again != "y":
            print("\nThanks for playing! Goodbye.")
            if stats:
                print(f"You played {len(stats)} games. Attempts: {stats}")
                print(f"Best game: {min(stats)} attempts, Worst game: {max(stats)} attempts")
            break


if __name__ == "__main__":
    main()