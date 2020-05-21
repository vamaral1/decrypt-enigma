def _str_score(str_a, str_b):
    if len(str_a) != len(str_b):
        return 0

    n_correct = 0

    for a, b in zip(str_a, str_b):
        n_correct += int(a == b)

    return n_correct / len(str_a)


def score(predicted_plain, correct_plain):
    # Score predictions. If 80% of the chacacters are correct, we say it's correct
    correct = 0
    
    for p, c in zip(predicted_plain, correct_plain):
        if _str_score(p, c) > 0.8:
            correct += 1

    return correct / len(correct_plain)

def predict(cipher_list, func):
    # apply function func to predict each item in cipher_list
    return [func(cipher) for cipher in cipher_list]