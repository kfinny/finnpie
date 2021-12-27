import re


SHA256_REGEX = re.compile("[a-f0-9]{64}", re.IGNORECASE)
HASH_REGEX = re.compile("\\b((?P<sha256>[a-f0-9]{64})|(?P<sha1>[a-f0-9]{40})|(?P<md5>[a-f0-9]{32}))\\b", re.I)


def normalize(data):
    """Normalizes the input to a upper-case string

    :param data: the data to normalize
    """
    return data.strip().upper()


def yield_hashes_from_text(text, validate=True):
    seen = set()
    for line in text.split('\n'):
        line = normalize(line)
        if validate is False:
            if line in seen:
                continue
            seen.add(line)
            yield line
        else:
            for h in HASH_REGEX.finditer(line):
                h = h.group()
                if h in seen:
                    continue
                seen.add(h)
                yield h


def yield_hashes_from_file(hash_file, validate=True):
    """Yields SHA-256 hashes from an input file.

    The default behavior guarantees unique, normalized (see normalize) SHA-256 hashes are yielded in the order they
    are encountered. If validate is set to False, each unique, normalized line is simply yielded.
    :param hash_file: The input file.
    :param validate: The validation behavior. If True, file is searched using a regular expression.
    """
    seen = set()
    with open(hash_file, 'r', encoding='utf-8') as fd:
        for line in fd:
            line = normalize(line)
            if validate is False:
                if line in seen:
                    continue
                seen.add(line)
                yield line
            else:
                for h in SHA256_REGEX.finditer(line):
                    h = h.group()
                    if h in seen:
                        continue
                    seen.add(h)
                    yield h


def get_hashes_from_file(hash_file, validate=False, sort=True):
    """ Returns a list of strings (nominally SHA-256 hashes) from a file.

    This function is intended to extract hashes from an input file. The original implementation found in the tg_script
    simply returned a unique list of 'normalized' strings in sorted order.  The normalization included stripping
    whitespace (e.g. '\r\n'), encoding as UTF-8 and upper-casing.  For the additional parameters with default values,
    this behavior is maintained.

    Notably, setting validate to 'True' returns all SHA-256 hashes found in a file using a regular expression. This
    means all hashes WILL be guaranteed to be SHA-256 hashes and multiple hashes can be included on a line.
    :param hash_file: The input file.
    :param validate: Defaults to False. If True, the file is searched for SHA-256 hashes.
    :param sort: If True, returns a sorted list.  Default is True.
    :return: A list of unique strings from the input file.
    """
    hashes = list(yield_hashes_from_file(hash_file, validate))
    if sort:
        return sorted(hashes)
    return hashes
