import math

class Graph:
    def __init__(self, roads, passengers):
        """
        Approach Description:
        The approach used in this question would be of a layered graph, whereby a forever_alone(graph1) and carpool(graph2)
        is created and intersecting when a passenger's found. In this initial function, I've initialised the basic attributes
        of the graphs, then adding edges for vertices found in both graphs forever_alone and carpool. Start by initialising
        the passenger's and roads attributes and assigning the values of the argugment to its corresponding attributes. Then
        finding the maximum of the start and end vertices in each of the graphs by iterating over the roads list. Lastly the
        initialise method creates two list of vertices, one for forever alone and one for the carpool graph, the adding edges to
        each connected to them, based on the roads given. If there are any passengers, it adds edges from the forever_alone graph
        to the carpool graph, hence the "layered graph" approach, if a passenger's picked up from the forever_alone graph, it goes
        directly (through an edge/ road) to the carpool graph.

        Input:
            roads(list): A list of roads, where each road is a tuple of(current_vertex(u), next_vertex(v), weight(w))
                                                                        # Based on lecture slides for u,v,w naming convention
        Returns:
            None
        Time Complexity:
            O(|L|+|R|)
        Aux Space Complexity:
            O(|L|+|R|)
        """

        self.passengers = passengers
        self.roads = roads

        # find the maximum vertex number in a list of roads
        maximum_vertex = 0
        for i in roads:
            # checking if the first or second element of the road is greater than the current maximum
            # vertex. If it is, it updates the max number vertex to the element.
            if i[0] > maximum_vertex:
                maximum_vertex = i[0]
            if i[1] > maximum_vertex:
                maximum_vertex = i[1]

        # creating two list of vertices(forever_alone and carpool), containing vertices with location ranging from 0 to the maximum vertex
        self.forever_alone = list(Vertex(location) for location in range(maximum_vertex + 1))
        self.carpool = list(Vertex(location2) for location2 in range (maximum_vertex + 1))

        for edges in roads:
            # adding an edge towards the forever_alone graph through abtaining the vertices on the current road of current_vertex and next
            # vertex and its weight(distance).
            self.forever_alone[edges[0]].edges.append(Edge(self.forever_alone[edges[0]], self.forever_alone[edges[1]], edges[2]))
            #If there are any passengers, add an edge to the carpool graph
            if len(self.passengers) >= 0:
                 self.carpool[edges[0]].edges.append(Edge(self.carpool[edges[0]], self.carpool[edges[1]], edges[3]))

        if len(passengers) > 0:
            for passenger in passengers:
                # adding and edge from the forever alone graph to the carpool graph if a passenger's found.
                # the weight(distance) is 0 because the passenger is already at the forever_alone vertex, waiting to be picked up.
                self.forever_alone[passenger].edges.append(Edge(self.forever_alone[passenger], self.carpool[passenger], 0))

    def dijkstra_backtracking(self, start, end, graph):
        """
        Approach description: After creating graph for both forever_alone and carpool, a backtrack and the dijkstra algorithm's
        implemented to find the shortest path between two vertices in a graph. Technically the start will be at the end vertex
        and the end will be at the start vertex. It start from the back to front to check if it would be an optimal route for the
        person to get from one end to the other, by only running dijkstra once to obtain the shortest distance from both carpool
        and forever_alone graphs.

        Inputs:
            start (int): the start vertex (starting from the back)
            end (int): the end vertex (front)
            graph: the graph
        Returns:
            a list of vertices that represents the shortest path
        Time Complexity:
            O(|R|log|L|)
        Aux Space Complexity:
            O(|L|+|R|)
        """
        start.distance = 0
        heap = MinHeap(graph)
        heap.insert(start)
        # while the heap's not empty
        while heap:
            current_vertex = heap.serve()
            current_vertex.visited = True
            path = []
            #If the current vertex is the end vertex
            if current_vertex.node_id == end.node_id:
                while current_vertex is not None:
                    # if the current vertex has a previous vertex
                    if current_vertex.previous is not None :
                        # if the current vertex and it's previous vertex are not the same
                        if current_vertex.node_id != current_vertex.previous.node_id:
                            # addd the current vertex to the path
                            path.append(current_vertex.node_id)
                    current_vertex = current_vertex.previous

                # adding the vertex id of the start vertex to a list called `path`,
                # returning the reversed version of that list.
                path.append(start.node_id)
                return list(reversed(path))

            for edge in current_vertex.edges:
                next_vertex = edge.next_vertex
                weight = edge.weight

                if next_vertex.visited == True:
                    pass

                elif next_vertex.distance > current_vertex.distance + weight:
                    next_vertex.distance = current_vertex.distance + weight
                    next_vertex.previous = current_vertex
                    # insert the next vertex into the MinHeap
                    heap.insert(next_vertex)

class Vertex:
    def __init__(self, node_id):
        """
        Function description:
            Initialising a node object
        Input:
            node_id: the id of the node/vertex
        Time complexity:
            O(1)
        Space complexity:
            O(1)
        """
        # id of the node
        self.node_id = node_id
        # a list of edges connecting to the vertex
        self.edges = []
        # indicates whether the node has been visited (bool)
        self.visited = False
        # distance from a vertex to a different vertex
        self.distance = math.inf
        # the vertex before the current vertex
        self.previous = None
        # a list of passengers that are on the vertex
        self.passengers = []

class Edge:
    def __init__(self, current_vertex, next_vertex, weight):
        """
        Function description:
            Initialising an edge object
        Input:
            current_vertex: id of current vertex
            next_vertex: id of next vertex
            weight: The weight of the edge(distance)
        Time complexity:
            O(1)
        Space complexity:
            O(1)
        """
        self.current_vertex = current_vertex
        self.next_vertex = next_vertex
        self.weight = weight

"""
MinHeap concept taken from CourseNote FIT2004by Daniel Anderson
What else is needed for dijkstra?
1) Modify the Minheap implementation to account for vertices
2) Account for vertex's index
"""
class MinHeap():
    def __init__(self, graph) -> None:
        """
        MinHeap concept taken from CourseNote FIT2004 by Daniel Anderson
        Function description:
            Initialising a MinHeap
        Input:
            graph: graph that the heapq is associated with
        Time complexity:
            O(1)
        Aux Space complexity:
            O(V), V's the number of elements in the MinHeap
        """
        # list of elements in the MinHeap
        self.array = [None]
        # number of elements in the MinHeap
        self.length = 0

        # keeps track of the index of each vertex in the MinHeap, then access and
        # update the position of a vertex in the heap when its distance is updated
        self.index = [None] * (len(graph.forever_alone))
        for i in range (1, len(self.array)):
            self.index[self.heap[i].node_id] = i

    def insert(self, element):
        """
        MinHeap concept taken from CourseNote FIT2004 by Daniel Anderson
        Function description:
            Inserts an element into the MinHeap
        Input:
            element: the element to be inserted
        Time Complexity:
            O(log V), V's the number of elements in the MinHeap
        Aux Space Complexity:
            O(1)
        """

        self.array.append(element)
        self.length += 1
        self.rise(self.length)

    def serve(self):
        """
        MinHeap concept taken from CourseNote FIT2004 by Daniel Anderson
        Function description:
            Removes and returning the element with the highest priority in the MinHeap
        Returns:
            The element with the highest priority
        Time Complexity:
            O(log V), V's the number of elements in the MinHeap
        Aux Space Complexity:
            O(1)
        """
        self.swap(1, self.length)
        self.length -= 1
        self.sink(1)
        return self.array.pop()

    def swap(self, x, y):
        """
        MinHeap concept taken from CourseNote FIT2004 by Daniel Anderson
        Function description:
            The given indices in the MinHeap and the index array will have
            its elements swapped
        Input:
            x(int): the index of the first element to be swapped
            y(int): the index of the second element to be swapped
        Time Complexity:
            O(1)
        Aux Space Complexity:
            O(1)
        """
        self.array[x], self.array[y] = self.array[y], self.array[x]
        self.index[self.array[x].node_id], self.index[self.array[y].node_id] = self.index[self.array[y].node_id], self.index[self.array[x].node_id]

    def rise(self, element_int: int):
        """
        MinHeap concept taken from CourseNote FIT2004 by Daniel Anderson
        Function description:
            Rise the element at the given index on the heap, bring it up
        Input:
            element_int: The index of the element to be rise
        Time Complexity:
            O(logV), V's the number of elements in the MinHeap
        Aux Space Complexity:
            O(1)
        """
        element = self.array[element_int]
        parent_index = element_int // 2
        while parent_index >= 1:
            parent = self.array[parent_index]

            # checking if the parent node is greater than the distance of the current element node.
            if parent.distance > element.distance:
                #swaps the positions of the parent and element nodes.
                self.swap(parent_index, element_int)
                #It then updates the indices of the element and parent nodes
                element_int = parent_index
                parent_index = element_int // 2
            else:
                break

    def sink(self, element_int: int):
        """
        MinHeap concept taken from CourseNote FIT2004 by Daniel Anderson
        Function description:
            Sink the element at the given index on the heap, basically bring it down
        Input:
            element_int: The index of the element to be sunk down
        Time Complexity:
            O(logV), V's the number of elements in the MinHeap
        Aux Space Complexity:
            O(1)
        """
        child_index = 2 * element_int
        while child_index <= self.length:
            child = self.array[child_index]

            # Checking if the index of the child node is less than the length of the array and if the
            # distance of the right child node is less than the distance of the left child node.
            if child_index < self.length and self.array[child_index+1].distance < child.distance:
                child = self.array[child_index+1]
                child_index += 1
            # Comparing the distance value of a node in the heap with its child node's distance value.
            if self.array[element_int].distance > child.distance:
                # swaps the positions of the two nodes in the heap
                self.swap(element_int, child_index)
                element_int = child_index
                child_index = 2 * element_int
            else:
                break

def optimalRoute(start: int, end: int, passengers, roads):
    """
    Function description:
        Approach has been explain above in functions within Graph class and how it operates
        by finding the optimal route between two nodes in the graph. Most operations have been
        done above.
    Input:
        start: The start vertex
        end: The end vertex
        passenger: The number of passengers
        roads(list): A list of roads, where each road is a tuple
    Returns:
        A list of integers that represents the optimal route
    Time Complexity:
        O(|R|log|L|), where |L| represents the key locations and |R| roads, represnts roads
    Aux Space Complexity:
        O(|R|+|L|), where |L| represents the key locations and |R| roads, represnts roads
    """
    graph = Graph(roads, passengers)
    start = graph.forever_alone[start]
    end = graph.forever_alone[end]
    return graph.dijkstra_backtracking(start, end, graph)