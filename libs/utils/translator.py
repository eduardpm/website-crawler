TRANSLATOR = None


def get_translator():
    """
    Get the translator instance.
    """
    global TRANSLATOR
    if TRANSLATOR is None:
        from translate import Translator

        TRANSLATOR = Translator(from_lang="nl", to_lang="en")
    return TRANSLATOR
