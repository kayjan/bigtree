def whoami() -> str:
    """Groot utils

    Returns:
        (str)
    """
    return "I am Groot!"


def speak_like_groot(sentence: str) -> str:
    """Convert sentence into Groot langauge

    Args:
        sentence (str): Sentence to convert to groot language

    Returns:
        (str)
    """
    return " ".join([whoami() for _ in range(len(sentence.split()))])
