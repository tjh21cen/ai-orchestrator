# intentionally misformatted file to trigger Black in CI

x = 1 + 2


def f() -> int:
    return x + 3


if __name__ == "__main__":
    print(f())
