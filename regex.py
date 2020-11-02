METACHARACTERS = {'?', '*', '+'}
ESCAPE_SEQUENCES = {'\?', '\*', '\+', '\.', '\^'}


def find_metacharacters(regex, which='first'):
    if which == 'first':
        for i, ch in enumerate(regex):
            if ch in METACHARACTERS:
                if i != 0 and regex[i-1] != '\\':
                    return i
    elif which == 'last':
        for i, ch in enumerate(regex[::-1]):
            if ch in METACHARACTERS:
                if i != 0 and regex[-i-2] != '\\':
                    return len(regex) - i
    return -1


def match(regex, word):
    re_len = len(regex)
    re_third_char = regex[2] if re_len > 2 else ''

    if not regex:
        return True
    elif not word:
        return False
    elif re_len > 1 and regex[0] == '\\':
        if regex[1] == word[0]:
            return match(regex[2:], word[1:])
        else:
            return False
    elif re_len > 1 and regex[1] == '?':
        if regex[0] == word[0]:
            return match(regex[2:], word[1:])
        else:
            return match(regex[2:], word)
    elif re_len > 1 and regex[1] == '*':
        if regex[0] == word[0] or (re_third_char and regex[0] == '.' and word[0] != re_third_char):
            return match(regex, word[1:])
        else:
            return match(regex[2:], word)
    elif re_len > 1 and regex[1] == '+':
        if not re_third_char:
            return True
        elif regex[0] == word[0] or (re_third_char and regex[0] == '.' and word[0] != re_third_char):
            return True
        else:
            return False
    elif regex[0] == '.':
        return match(regex[1:], word[1:])
    elif regex[0] == word[0]:
        return match(regex[1:], word[1:])
    return False


def my_regex(regex, word):
    if not regex:
        return True
    elif not word:
        return False

    if regex[0:2] == '\^' and regex[1] != word[0]:
        return False

    if regex.startswith('^'):
        pos_min = find_metacharacters(regex, 'first')
        start_regex = regex[:pos_min]
        if match(start_regex[1:len(word)], word):
            regex = regex[1:]
        else:
            return False

    if regex.endswith('$'):
        pos_max = find_metacharacters(regex, 'last')
        end_regex = regex[pos_max+1:]
        if end_regex[:-1] in ESCAPE_SEQUENCES:
            if end_regex[-1] != word[-1]:
                return True
        return match(end_regex[:-1], word[-len(end_regex[:-1]):]) if end_regex[:-1] else False

    return True if match(regex, word) else my_regex(regex, word[1:])


def main():
    regex, word = input("").split('|')
    print(my_regex(regex, word))


if __name__ == '__main__':
    main()
