
class Map:

    def __init__(self, row = 3, column = 4, grid =  [['q', 'v', 'p', 4],['v', 6, 'q', 8], ['p', 'q', 'v', 'v']]):
        self.row = row
        self.column = column
        self.grid = grid
        self.edges = list(list())
        x = 65
        for i in range(row+1):
            self.edges.append(list())
            for j in range(column+1):
                self.edges[i].append(chr(x))
                x+=1
       

    def printEdges(self):
       for x in range(len(self.edges)):
           for y in range(len(self.edges[x])):
               print((self.edges[x][y]), end=', ')
           print('\n')

class AStarPath:
    def __init__(self, start, destination):
        pass

def main():
    myMap = Map()
    myMap.printEdges()

   # print(for x in myMap.edges)

main()