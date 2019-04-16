from gameTree import *
import msgpack
with open('rate_2c.msgpack') as data_file:
    rate = msgpack.unpack(data_file)
# node = Node("SB", None, 10, 20, ['SA', 'HA'], 2, rate.get("AAd"))
# tree = Tree(node)
# tree.set_my_role("SB")
# tree.build_tree(5)
# from pptree import *
# print_tree(node, "children", "description")
print rate