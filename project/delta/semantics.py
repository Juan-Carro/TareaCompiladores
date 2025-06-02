# Author: A01748640 Juan Carlos Carro Cruz

from arpeggio import PTNodeVisitor


class SemanticMistake(Exception):

    def __init__(self, message):
        super().__init__(f'Semantic error: {message}')


class SemanticVisitor(PTNodeVisitor):

    RESERVED_WORDS = ['true', 'false', 'var', 'if', 'else', 'while', 'do']

    def __init__(self, parser, **kwargs):
        super().__init__(**kwargs)
        self.__parser = parser
        self.__symbol_table = []

    def position(self, node):
        return self.__parser.pos_to_linecol(node.position)

    @property
    def symbol_table(self):
        return self.__symbol_table

    def visit_decl_variable(self, node, children):
        name = node.value
        if name in self.RESERVED_WORDS:
            raise SemanticMistake(
                'Reserved word not allowed as variable name at position '
                f'{self.position(node)} => {name}'
            )
        if name in self.__symbol_table:
            raise SemanticMistake(
                'Duplicate variable declaration at position '
                f'{self.position(node)} => {name}'
            )
        self.__symbol_table.append(name)

    def visit_lhs_variable(self, node, children):
        name = node.value
        if name not in self.__symbol_table:
            raise SemanticMistake(
                'Assignment to undeclared variable at position '
                f'{self.position(node)} => {name}'
            )


    def visit_decimal(self, node, children):
        value = int(node.value)
        if value >= 2 ** 31:
            raise SemanticMistake(
                'Out of range decimal integer literal at position '
                f'{self.position(node)} => {value}'
            )
        
    def visit_binary(self, node, children):
        value_str = node.value[2:]
        if not value_str:
            raise SemanticMistake(
                f'Empty binary literal at position {self.position(node)}'
            )
        value = int(value_str, 2)
        if value >= 2**31:
            raise SemanticMistake(
                'Out of range binary integer literal at position '
                f'{self.position(node)} => {value}'
            )

    def visit_octal(self, node, children):
        value_str = node.value[2:]
        if not value_str:
            raise SemanticMistake(
                f'Empty octal literal at position {self.position(node)}'
            )
        value = int(value_str, 8)
        if value >= 2**31:
            raise SemanticMistake(
                'Out of range octal integer literal at position '
                f'{self.position(node)} => {value}'
            )


    def visit_hexadecimal(self, node, children):
        value_str = node.value[2:]
        if not value_str:
            raise SemanticMistake(
                f'Empty hexadecimal literal at position {self.position(node)}'
            )
        value = int(value_str, 16)
        if value >= 2**31:
            raise SemanticMistake(
                'Out of range hexadecimal integer literal at position '
                f'{self.position(node)} => {value}'
            )
    

    def visit_rhs_variable(self, node, children):
        name = node.value
        if name not in self.__symbol_table:
            raise SemanticMistake(
                'Undeclared variable reference at position '
                f'{self.position(node)} => {name}'
            )
