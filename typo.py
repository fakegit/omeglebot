#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Typography functions"""

from random import choice

alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
vowels = "aeiouy"


def spin_content(content):
    start = content.find("{")
    end = content.find("}")
    if start == -1 and end == -1:
        return content
    elif start == -1:
        return content
    elif end == -1:
        pass
    elif end < start:
        return content
    elif start < end:
        rest = spin_content(content[start + 1:])
        end = rest.find("}")
        if end == -1:
            pass
        return (
            content[:start]
            + choice(rest[:end].split("|"))
            + spin_content(rest[end + 1:])
        )


def generate_typos(s, safe):
    words = s.split()
    if len(words) < 3:
        return s
    _words = [
        [index, word]
        for index, word in enumerate(words)
        if (
            len(word) > 3
            and "/" not in word
            and "." not in word
            and word.strip() not in safe.values()
        )
    ]

    for i in range(len(_words)):
        word = _words[i][1]
        kwd = choice(
            [
                double_letter(word),
                # These usually makes words really indecipherable
                # skip_letter(word),
                # reverse_letter(word),
                wrong_vowel(word),
            ]
        )
        if kwd:
            words[_words[i][0]] = kwd
    return " ".join(words)


def inserted_key(s):
    kwds = []
    for i in range(0, len(s)):
        for char in alphabet:
            kwds.append(s[: i + 1] + char + s[i + 1:])
    return choice(kwds)


def skip_letter(s):
    kwds = []
    for i in range(1, len(s) + 1):
        kwds.append(s[:i - 1] + s[i:])
    if kwds:
        return choice(kwds)


def double_letter(s):
    kwds = []
    for i in range(0, len(s) + 1):
        kwds.append(s[:i] + s[i - 1] + s[i:])
    if kwds:
        return choice(kwds)


def reverse_letter(s):
    kwds = []
    for i in range(1, len(s) - 1):
        letters = s[i - 1:i + 1:1]
        if len(letters) != 2:
            continue
        reverse_letters = letters[1] + letters[0]
        kwds.append(s[:i - 1] + reverse_letters + s[i + 1:])
    if kwds:
        return choice(kwds)


def wrong_vowel(s):
    kwds = []
    for i in range(0, len(s)):
        for letter in vowels:
            if s[i] in vowels:
                for vowel in vowels:
                    s_list = list(s)
                    s_list[i] = vowel
                    kwd = "".join(s_list)
                    kwds.append(kwd)
    if kwds:
        return choice(kwds)


def wrong_key(s):
    kwds = []
    for i in range(0, len(s)):
        for letter in alphabet:
            kwd = s[:i] + letter + s[i + 1:]
            kwds.append(kwd)
    if kwds:
        return choice(kwds)
