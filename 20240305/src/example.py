def foo(**kwargs):  # Cognitive: 3, Cyclomatic: 3
    res = []

    for key, value in kwargs.items():
        if key == value:
            res.append(key)
            continue

        res.append(f"{key}+{value}")

    return res


def bar(**kwargs):  # Cognitive: 1, Cyclomatic: 3
    res = [key if key == value else f"{key}+{value}" for key, value in kwargs.items()]

    return res
