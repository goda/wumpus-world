import getopt
import sys
from wumpus.src.WumpusWorld import WumpusWorld

if __name__ == '__main__':
    visualize = False
    opts, args = getopt.getopt(sys.argv[1:],"v",["visualize="])
    for opt, arg in opts:
        print(opt)
        if opt in ("-v", "--visualize"):
            visualize = True
            
    w = WumpusWorld(4, 4, 0.2, False)
    w.main(visualize)    