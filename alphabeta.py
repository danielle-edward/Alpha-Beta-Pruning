import os # required to get the cwd

touches = 0 # will hold the number of leaf nodes that are examined for each tree

class Node(object): # defines the properties of a node of the tree
    def __init__(self, data, minMax):
        self.data = data
        self.children = []
        self.maxMin = minMax
        self.isLeaf = False
        self.isRoot = False

    def addChild(self, obj): # function to add children to a node. Will be used when creating edges
        self.children.append(obj)

def isNum(s): # function used when checking if the child value of an edge is a regualr node or leaf node
    try:
        int(s)
        return True
    except ValueError:
        return False

def generateTree(tree): # generates the tree based on the nodes and edges sets for that tree from the input file
    nodeList = []

    tree = tree.replace('{', '') # this and the two lines below format the input so that it can be handled properly
    tree = tree.replace(')}', ' ')
    tree = tree.replace('(', '')
    tree = tree.split() # splits input data into a node list and an edge list

    nodes = tree[0].split('),') # splits the indiviual nodes
    edges = tree[1].split('),') # splits the individual edges

    for node in nodes:
        node = node.split(',') # splits each individual node into data and minMax values
        newNode = Node(node[0], node[1]) # creates a node
        nodeList.append(newNode) # adds the new node to the node list

    nodeList[0].isRoot = True # the first node in this list will always be the root

    for edge in edges:
        edge = edge.split(',') # splits each individual edge into parent and child
        parent = edge[0]
        child = edge[1]
        for node in nodeList: # finding the parent node of this edge in our pre-existing list of nodes
            if node.data == parent:
                parentNode = node # we have found the parent node for this individual edge, so we can break out of this inner for loop and move on
                break
        if isNum(child): # if the child of the edge is a number, then it will be a leaf
            newNode = Node(child, None) # create a new node for the leaf, because this leaf nodes are not specified in the nodes input list
            newNode.isLeaf = True # specify that it is a leaf
            parentNode.addChild(newNode) # this should add itself to the children list of its parent node
        else: # if the child is a node rather than a number (i.e. it is not a leaf)
            for node in nodeList:
                if node.data == child: # find which pre-existing node is the child of this edge
                    childNode = node # we have found the child node for this individual edge
                    parentNode.addChild(childNode) # create the edge
                    break # break out of this for loop because we already created the edge

    return nodeList

def alpha_beta(current_node, alpha, beta): # this function performs the actual pruning
    if (current_node.isRoot): # set the initial values of alpha and beta
        alpha = float((-1) - (2**63))
        beta = float((-1) + (2**63))

    if (current_node.isLeaf): # if current node is leaf node:
        global touches
        touches +=1 # increment the count for number of leaf nodes examined
        return int(current_node.data) # return static evaluation of current node (i.e. its data)

    if current_node.maxMin == 'MAX': # if the current node is a max node
        for child in current_node.children: # go through its children
            alpha = max(alpha, alpha_beta(child, alpha, beta)) # compare children values
            if alpha >= beta: # determine if we found a new alpha
                return alpha
        return alpha

    if current_node.maxMin == 'MIN': # if the current node is a min node
        for child in current_node.children: # go through its children
            beta = min(beta, alpha_beta(child, alpha, beta)) # compare children values
            if alpha >= beta: # determine if we found a new beta
                return beta
        return beta

def printScore(graph, score): # print the results to the output file
    global f2
    string = "Graph %d, Score: %d; Leaf Nodes Examined: %d \n" %(graph, score, touches)
    f2.write(string)

def main():
    global f2 # making f2 global so that it can be accessed from the printScore function
    f2 = open("alpha_beta_out.txt", mode='w+') # f2 was placed here so that on each new run of the program, the output file will be cleared then added to.
                                               # if it was placed inside the printScore function, a new file would be created for every tree and only the results for the last tree would be displayed
                                               # if "append" was used, the results from the previus run would still be in the file, which is likely not what you would want

    graph = 0 # the holds the graph number we are on for printing purposes

    cwd = os.getcwd().replace('\\', '/') # gets the current working directory of this python file
    f1 = open(cwd + "/alphabeta.txt", mode='r') # opens the input file to be read from

    treeData = [line.rstrip('\n') for line in f1] # each index of treeData contains the 2 sets (nodes and edges) needed for that tree

    for tree in treeData:
        global touches
        touches = 0 # set touches back to 0
        nodeList = generateTree(tree) # generate the tree and store the nodes in nodeList
        graph += 1 # increment the graph number that we are on
        score = alpha_beta(nodeList[0], 0, 0) # perform the pruning
        printScore(graph, score) # print the results to the output file

if __name__ == "__main__":
    main()
