from delta import Compiler, Phase


source = '''
            var t, u;
            t = false;
            u = true;
            !u || t || u/t
            '''

c = Compiler('program')
c.realize(source)
# print(c.parse_tree_str)
# print(c.wat_code)
print(c.result)
