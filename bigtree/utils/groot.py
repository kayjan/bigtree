def whoami() -> str:
    """Groot utils.

    Returns:
        Groot reply
    """
    return "I am Groot!"


def speak_like_groot(sentence: str) -> str:
    """Convert sentence into Groot langauge.

    Args:
        sentence: sentence to convert to groot language

    Returns:
        Groot string
    """
    return " ".join([whoami() for _ in range(len(sentence.split()))])
