import re, sys

# LL(1) parsing table: (NonTerminal, terminal) -> production body
table = {
    ('E', 'id'): ['T', "E'"],  ('E', 'num'): ['T', "E'"],  ('E', '('): ['T', "E'"],
    ("E'", '+'): ['+', 'T', "E'"], ("E'", '-'): ['-', 'T', "E'"],
    ("E'", ')'): [], ("E'", '$'): [],
    ('T', 'id'): ['F', "T'"],  ('T', 'num'): ['F', "T'"],  ('T', '('): ['F', "T'"],
    ("T'", '*'): ['*', 'F', "T'"], ("T'", '/'): ['/', 'F', "T'"],
    ("T'", '+'): [], ("T'", '-'): [], ("T'", ')'): [], ("T'", '$'): [],
    ('F', 'id'): ['id'], ('F', 'num'): ['num'], ('F', '('): ['(', 'E', ')'],
}
nonterminals = {'E', "E'", 'T', "T'", 'F'}

def tokenize(src):
    toks = []
    for t in re.findall(r'\d+(?:\.\d+)?|[A-Za-z_]\w*|[()+\-*/]|\S', src):
        if re.fullmatch(r'\d+(?:\.\d+)?', t): toks.append('num')
        elif re.fullmatch(r'[A-Za-z_]\w*', t): toks.append('id')
        else: toks.append(t)
    return toks + ['$']

def parse(src):
    tokens = tokenize(src)
    stack = ['$', 'E']
    i = 0
    print(f"\nInput: {src}")
    print(f"{'STACK':<30}{'INPUT':<30}ACTION")
    while True:
        top, cur = stack[-1], tokens[i]
        print(f"{' '.join(stack):<30}{' '.join(tokens[i:]):<30}", end='')
        if top == '$' and cur == '$':
            print("ACCEPT"); print("Result: VALID string"); return True
        if top not in nonterminals:              # terminal on top
            if top == cur:
                print(f"match {cur}"); stack.pop(); i += 1
            else:
                print("ERROR"); print(f"Result: INVALID (expected {top}, got {cur})"); return False
        else:                                    # non-terminal on top
            prod = table.get((top, cur))
            if prod is None:
                print("ERROR"); print(f"Result: INVALID (no rule for {top}, {cur})"); return False
            print(f"{top} -> {' '.join(prod) if prod else 'ε'}")
            stack.pop()
            stack.extend(reversed(prod))

if __name__ == "__main__":
    tests = sys.argv[1:] or ["a + b * 3", "(x + 2) * y", "a + * b"]
    for t in tests:
        parse(t)