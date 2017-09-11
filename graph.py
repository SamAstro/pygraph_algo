""" This is the docstring for the graph.py module.

This module implements graph representation

Version:  1.0
Created:  2017-09-11
Compiler: python

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Affiliation:
Notes:
"""

import abc
import numpy as np

class Graph(abc.ABC):
    r"""The base class representation of a graph

    """
    def __init__(self, nbvertices, directed=False):
        self.nbvertices = nbvertices
        self.directed = directed

    @abc.abstractmethod
    def add_edge(self, vertex1, vertex2, weight):
        pass

    @abc.abstractmethod
    def get_adjacent_vertices(self, vertex):
        pass

    @abc.abstractmethod
    def get_indegree(self, vertex):
        pass

    @abc.abstractmethod
    def get_edge_weight(self, vertex1, vertex2):
        pass

    @abc.abstractmethod
    def display(self):
        pass


class Node:
    r""" A single node in a graph represented by an adjacency set.

    Every node has a vertex id. Each node is associated with a set of adjacent
    vertices

    """
    def __init__(self, vertexid):
        self.vertexid = vertexid
        self.adjacency_set = set()

    def add_edge(self, vertex):
        if self.vertexid == vertex:
            raise ValueError("The vertex {0} cannot be adjacent to itself".format(vertex))
        self.adjacency_set.add(vertex)

    def get_adjacent_vertices(self):
        return sorted(self.adjacency_set)


class AdjacencySetGraph(Graph):
    r"""Represents a graph as an adjacency set.

    A graph is a list of Nodes and each Node has a  set of adjacent vertices.
    This graph in this current form cannot be used to represent weighted edges
    only unweighted edges can be represented

    """
    def __init__(self, nbvertices, directed=False):
        super(AdjacencySetGraph, self).__init__(nbvertices, directed)

        self.vertex_list = []
        for i in range(nbvertices):
            self.vertex_list.append(Node(i))

    def add_edge(self, v1, v2, weight=1):
        if v1 >= self.nbvertices or v2 >= self.nbvertices or v1 < 0 or v2 < 0:
            raise ValueError("Vertices %d and %d are out of bounds" % (v1, v2))

        if weight != 1:
            raise ValueError("An adjacency set cannot represent edge weights >1")

        self.vertex_list[v1].add_edge(v2)
        if self.directed == False:
            self.vertex_list[v2].add_edge(v1)


    def get_adjacent_vertices(self, v):
        if v < 0 or v >= self.nbvertices:
            raise ValueError("Cannot access vertex %d" % v)

        return self.vertex_list[v].get_adjacent_vertices()

    def get_indegree(self, v):
        if v < 0 or v >= self.nbvertices:
            raise ValueError("Cannot access vertex %d" % v)

        indegree = 0
        for i in range(self.nbvertices):
            if v in self.get_adjacent_vertices(i):
                indegree = indegree + 1

        return indegree

    def get_edge_weight(self, v1, v2):
        return 1

    def display(self):
        for i in range(self.nbvertices):
            for v in self.get_adjacent_vertices(i):
                print(i, v, sep='-->')

class AdjacencyMatrixGraph(Graph):
    r"""Represents a graph as an adjacency matrix

    A cell in the matrix has a value when there exists an edge between the vertex represented by the row and column numbers

    Weighted graphs can hold values > 1 in the matrix cells

    A value of 0 in the cell indicates that there is no edge

    """

    def __init__(self, nbvertices, directed=False):
        super(AdjacencyMatrixGraph, self).__init__(nbvertices, directed)

        self.matrix = np.zeros((nbvertices, nbvertices))

    def add_edge(self, v1, v2, weight=1):
        if v1 >= self.nbvertices or v2 >= self.nbvertices or v1 < 0 or v2 < 0:
            raise ValueError("Vertices %d and %d are out of bounds" % (v1, v2))

        if weight < 1:
            raise ValueError("An edge cannot have weight < 1")

        self.matrix[v1][v2] = weight
        if self.directed == False:
            self.matrix[v2][v1] = weight

    def get_adjacent_vertices(self, v):
        if v < 0 or v >= self.nbvertices:
            raise ValueError("Cannot access vertex %d" % v)

        adjacent_vertices = []
        for i in range(self.nbvertices):
            if self.matrix[v][i] > 0:
                adjacent_vertices.append(i)

        return adjacent_vertices

    def get_indegree(self, v):
        if v < 0 or v >= self.nbvertices:
            raise ValueError("Cannot access vertex %d" % v)

        indegree = 0
        for i in range(self.nbvertices):
            if self.matrix[i][v] > 0:
                indegree = indegree + 1

        return indegree

    def get_edge_weight(self, v1, v2):
        return self.matrix[v1][v2]

    def display(self):
        for i in range(self.nbvertices):
            for v in self.get_adjacent_vertices(i):
                print(i, v, sep='-->')
def main():
    g = AdjacencyMatrixGraph(4, directed=True)
    g.add_edge(0, 1, 43)
    g.add_edge(0, 2, 55)
    g.add_edge(2, 3, 10)

    for i in range(4):
        print("Adjacent to:", i, g.get_adjacent_vertices(i), sep=' ')

    for i in range(4):
        print("Indegree:", i, g.get_indegree(i), sep=' ')

    for i in range(4):
        for j in g.get_adjacent_vertices(i):
            print("Edge weight:", i, j, "weight:", g.get_edge_weight(i, j), sep=' ')

    g.display()

if __name__ == "__main__":
    main()
