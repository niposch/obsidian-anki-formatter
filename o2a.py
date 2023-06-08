from __future__ import annotations


# the resulting expression may contain a single dot, in its place the first group of the regex will be inserted
# if multiple capture groups are used, they can be inserted via $1, $2, etc.
# if dollar signs are supposed to be inserted, they need to be escaped with a backslash
strings_to_replace = [
    (r"\$\$(.+)=(.+)\$\$", "\n\$$1\$ \$=\$ \$$2\$\n"), # split multiline latex at equal signs and turn into single line latex
    (r"\$(.+)=(.+)\$", "\$$1\$ \$=\$ \$$2\$"), # split latex at equal signs
    ("\$\$(.+?)\$\$" , "\[.\]"), # mathjax block
    ("\$(.+?)\$" , "\(.\)"), # mathjax inline
    # uncomment the following lines to convert input to anki latex 
    # "\$\$(.+?)\$\$" : "[$$].[/$$]", # latex block
    # "\$(.+?)\$" : "[$].[/$]", # latex inline

    ("\[\[([^|]+?)\]\]", "."), # obsidian link
    ("\[\[.+?\|(.+?)\]\]", "."), # obsidian link with alias
    ("^> *?(.+)", "."), # get rid of blockquotes
    ("\{\{", "{ {"), # get rid of double curlies
    ("\}\}", "} }"), # get rid of double curlies
]
import re


def extractor_factory(prefix:str, postfix:str)->callable:
    def extract_content(match: re.Match)->str:
        try:
            return prefix + match.group(1) + postfix
        except IndexError:
            return ""
    return extract_content

def has_unescaped(string:str, symbol)->bool:
    unescaped_finder = re.compile(r"(?<!\\)" + symbol)
    return unescaped_finder.search(string) is not None

def run_replacement(inp:str, regex:str, replace:str)->str:
    if has_unescaped(replace, "\."):
        return execute_single_group_replacement(inp, regex, replace)
    elif has_unescaped(replace, "\$\d+"):
        return execute_multi_group_replacement(inp, regex, replace)
    else:
        # replace all occurences of the regex with the replacement string
        expression = re.compile(regex)
        return expression.sub(replace, inp)

def execute_single_group_replacement(inp:str, regex:str, replace:str)->str:
    # extract the content of the first group of the regex
    # replace the dot in the replacement string with the extracted content
    expression = re.compile(regex)
    current_pos = 0
    while True:
        matches = expression.finditer(inp, current_pos)
        match = next(matches, None)
        if match is None:
            break

        first_group = match.group(1)
        non_escaped_finder = re.compile(r"(?<!\\)\.")
        splits = re.split(non_escaped_finder, replace)
        replacement = first_group.join(splits)
        replacement = replacement.replace("\.", ".")
        inp = inp[:match.start()] + replacement + inp[match.end():]
        current_pos = match.start() + len(replacement)

    return inp

def execute_multi_group_replacement(inp:str, regex:str, replace:str)->str:
    # extract the content of the capture groups of the regex
    # replace the $n in the replacement string with the respective capure group's content
    expression = re.compile(regex)
    current_pos = 0
    while True:
        matches = expression.finditer(inp, current_pos)
        match = next(matches, None)
        if match is None:
            break

        groups = match.groups()
        replacement = replace
        for i, group in enumerate(groups):
            replacement = replacement.replace(f"${i+1}", group)
        replacement = replacement.replace("\$", "$")
        inp = inp[:match.start()] + replacement + inp[match.end():]
        current_pos = match.start() + len(replacement)
    return inp

def replace_all(inp, strings_to_replace):
    for replace in strings_to_replace:
        inp = run_replacement(inp, *replace)
    return inp

if __name__ == "__main__":
    inp = ""

    try:
        while True:
            inp += input() + "\n"
    except KeyboardInterrupt:
        pass


    print("========================================")

    print(replace_all(inp, strings_to_replace))