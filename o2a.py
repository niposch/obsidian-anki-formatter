from __future__ import annotations

strings_to_replace = [
    ("\$\$(.+?)\$\$" , "\[.\]"), # mathjax block
    ("\$(.+?)\$" , "\(.\)"), # mathjax inline
    # uncomment the following lines to convert input to anki latex 
    # "\$\$(.+?)\$\$" : "[$$].[/$$]", # latex block
    # "\$(.+?)\$" : "[$].[/$]", # latex inline

    ("\[\[([^|]+?)\]\]", "."), # obsidian link
    ("\[\[.+?\|(.+?)\]\]", "."), # obsidian link with alias
    (">.+?", "."), # get rid of blockquotes
]

inp = ""

try:
    while True:
        inp += input() + "\n"
except KeyboardInterrupt:
    pass

import re


def extractor_factory(prefix:str, postfix:str)->callable:
    def extract_content(match: re.Match)->str:
        try:
            return prefix + match.group(1) + postfix
        except IndexError:
            return ""
    return extract_content

def replace_all(inp, strings_to_replace):
    for replace in strings_to_replace:
        prefix, postfix = replace[1].split(".")
        inp = re.sub(replace[0], extractor_factory(prefix, postfix), inp)
    return inp

print("========================================")

print(replace_all(inp, strings_to_replace))