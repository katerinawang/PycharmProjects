import os
import re
import sys
import ast

blank = 0
err = {
        1: 'S001 Too long',
        2: 'S002 Indent not good',
        3: 'S003 Unnecessary semicolon',
        4: 'S004 At least two spaces required before inline comments',
        5: 'S005 TODO found',
        6: 'S006 More than two blank lines used before this line',
        7: "S007 Too many spaces after '{0}'",
        8: "S008 Class name '{0}' should use CamelCase",
        9: "S009 Function name '{0}' should use snake_case",
        10: "S010 Argument name '{0} should be written in snake_case",
        11: "S011 Variable '{0} should be written in snake_case'",
        12: "S012 The default argument value is mutable"
        }


def add_dict(items, keys, value):
    try:
        items[keys].append(value)
    except KeyError:
        items[keys] = [value]


class Analyzer(ast.NodeVisitor):
    def __init__(self, dic):
        self.err_list = dic

    def visit_ClassDef(self, node):
        if not re.match(r'([A-Z][a-z]+)+', node.name):
            add_dict(self.err_list, node.lineno, (8, node.name))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if not re.match(r'_*([a-z]+_*)+', node.name):
            add_dict(self.err_list, node.lineno, (9, node.name))
        for v in node.args.defaults:
            if isinstance(v, ast.List) or isinstance(v, ast.Set) or isinstance(v, ast.Dict):
                add_dict(self.err_list, node.lineno, 12)
        for arg in node.args.args:
            if not re.match(r'_*([a-z]+_*)+', arg.arg):
                add_dict(self.err_list, node.lineno, (10, arg))
        self.generic_visit(node)

    def visit_Name(self, node):
        if not re.match(r'_*([a-z]+_*)+', node.id):
            add_dict(self.err_list, node.lineno, (11, node.id))

    def visit_Expr(self, node):
        pass


class RestAnalyzer:
    def __init__(self):
        self.line_num, self.line, self.file = None, None, None
        self.err_list = {}

    def check_len(self):
        if len(self.line) > 79:
            add_dict(self.err_list, self.line_num, 1)

    def check_indent(self):
        if re.match(r'^([^\S\r\n]*)(?=\w)', self.line):
            indent = len(re.match(r'^([^\S\r\n]*)(?=\w)', self.line).group(1)) if self.line else 0
            if indent % 4 != 0:
                add_dict(self.err_list, self.line_num, 2)

    def check_semicolon(self):
        if ';' in self.line and not re.search(r"'.*?;.*?'|#.*?;", self.line):
            add_dict(self.err_list, self.line_num, 3)

    def check_inline_comment_spaces(self):
        if '#' in self.line and not re.search(r'\s{2}#', self.line) and not re.match('#', self.line):
            add_dict(self.err_list, self.line_num, 4)

    def check_todo(self):
        if re.search(r'#\stodo', self.line, flags=re.I):
            add_dict(self.err_list, self.line_num, 5)

    def check_two_black_line(self):
        global blank
        if self.line == '\n':
            blank += 1
        if blank > 2 and self.line != '\n':
            add_dict(self.err_list, self.line_num, 6)
        if self.line != '\n':
            blank = 0

    def check_class_spaces(self):
        if re.search(r'(class|def)\s{2,}', self.line):
            sub = 'class' if 'class' in self.line else 'def'
            add_dict(self.err_list, self.line_num, (7, sub))

    def check_all(self, path):
        with open(path, 'r') as f:
            for item in enumerate(f, start=1):
                self.line_num, self.line, self.file = item[0], item[1], path
                self.check_len()
                self.check_indent()
                self.check_semicolon()
                self.check_inline_comment_spaces()
                self.check_todo()
                self.check_two_black_line()
                self.check_class_spaces()

        return self.err_list


def print_err(filepath, dic):
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    code = Analyzer(dic)
    code.visit(tree)
    for k, v in code.err_list.items():
        for i in v:
            if isinstance(i, tuple):
                print(f'{filepath}: Line {k}: {err[i[0]].format(i[1])}')
            else:
                print(f'{filepath}: Line {k}: {err[i]}')


def main(filepath):
    if re.search(r'\.py$', filepath):
        dic = RestAnalyzer().check_all(filepath)
        print_err(filepath, dic)
    else:
        for file in sorted(os.listdir(filepath)):
            dic = RestAnalyzer().check_all(os.path.join(filepath, file))
            print_err(os.path.join(filepath, file), dic)


if __name__ == '__main__':
    main(sys.argv[1])
