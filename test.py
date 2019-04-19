# from gameTree import Node, Tree
# root = Node("SB", None, 10, 20, ["HA", "S5"], 2)
# tree = Tree(root)
# tree.build_tree()
# print "saving"
# import cPickle
# ouf = open('tree.pkl', 'w')
# cPickle.dump(tree, ouf)
# # inf = open('tree.pkl')
# # tree = cPickle.load(inf)
# # print "loaded"
# # print tree.root
import cPickle
inf = open('result49.pkl')
data = cPickle.load(inf)
print data