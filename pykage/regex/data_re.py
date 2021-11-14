import re

ul = '\u00a1-\uffff'
REGEX_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
REGEX_GIT_PROJECT = r'((git@|http(s)?:\/\/)([\w\.@]+)(\/|:))([\w,\-,\_]+)\/([\w,\-,\_]+)(.git){0,1}((\/){0,1})'
REGEX_VERSION_NUMBER = r'^(\d+)((\.{1}\d+)*)(\.{0})$'
REGEX_SITE = (
        r'\.'                                 # point
        r'(?!-)'                              # ne peut pas commencer par un tiret
        r'(?:[a-z'  +  ul  +  '-]{2,63}'          # étiquette de domaine
        r'|xn--[a-z0-9]{1,59})'               # ou étiquette punycode
        r'(?<!-)'                             # ne peut pas se terminer par un tiret
        r'\.?'                                # peut avoir un point final
    )

def is_valid_git_project(url):
    return bool(re.match(REGEX_GIT_PROJECT, url))

def is_valid_url(url):
    return bool(re.match(REGEX_GIT_PROJECT, url))

def get_name_from_git_repostery(url):
    if is_valid_git_project(url):
        return re.match(REGEX_GIT_PROJECT, url).group(7)
    else:
        return None
