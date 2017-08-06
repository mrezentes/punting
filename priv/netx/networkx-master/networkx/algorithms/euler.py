# -*- coding: utf-8 -*-
#
#    Copyright (C) 2010 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#
# Authors:
#   Nima Mohammadi <nima.irt@gmail.com>
#   Aric Hagberg <hagberg@lanl.gov>
"""
Eulerian circuits and graphs.
"""
import networkx as nx

from ..utils import arbitrary_element

__all__ = ['is_eulerian', 'eulerian_circuit']


def is_eulerian(G):
    """Returns True if and only if `G` is Eulerian.

    A graph is *Eulerian* if it has an Eulerian circuit. An *Eulerian
    circuit* is a closed walk that includes each edge of a graph exactly
    once.

    Parameters
    ----------
    G : NetworkX graph
       A graph, either directed or undirected.

    Examples
    --------
    >>> nx.is_eulerian(nx.DiGraph({0: [3], 1: [2], 2: [3], 3: [0, 1]}))
    True
    >>> nx.is_eulerian(nx.complete_graph(5))
    True
    >>> nx.is_eulerian(nx.petersen_graph())
    False

    Notes
    -----
    If the graph is not connected (or not strongly connected, for
    directed graphs), this function returns False.

    """
    if G.is_directed():
        # Every node must have equal in degree and out degree and the
        # graph must be strongly connected
        return (all(G.in_degree(n) == G.out_degree(n) for n in G)
                and nx.is_strongly_connected(G))
    # An undirected Eulerian graph has no vertices of odd degree and
    # must be connected.
    return all(d % 2 == 0 for v, d in G.degree()) and nx.is_connected(G)


def _simplegraph_eulerian_circuit(G, source):
    if G.is_directed():
        degree = G.out_degree
        edges = G.out_edges
    else:
        degree = G.degree
        edges = G.edges
    vertex_stack = [source]
    last_vertex = None
    while vertex_stack:
        current_vertex = vertex_stack[-1]
        if degree(current_vertex) == 0:
            if last_vertex is not None:
                yield (last_vertex, current_vertex)
            last_vertex = current_vertex
            vertex_stack.pop()
        else:
            _, next_vertex = arbitrary_element(edges(current_vertex))
            vertex_stack.append(next_vertex)
            G.remove_edge(current_vertex, next_vertex)


def _multigraph_eulerian_circuit(G, source):
    if G.is_directed():
        degree = G.out_degree
        edges = G.out_edges
    else:
        degree = G.degree
        edges = G.edges
    vertex_stack = [(source, None)]
    last_vertex = None
    last_key = None
    while vertex_stack:
        current_vertex, current_key = vertex_stack[-1]
        if degree(current_vertex) == 0:
            if last_vertex is not None:
                yield (last_vertex, current_vertex, last_key)
            last_vertex, last_key = current_vertex, current_key
            vertex_stack.pop()
        else:
            _, next_vertex, next_key = arbitrary_element(edges(current_vertex, keys=True))
            vertex_stack.append((next_vertex, next_key))
            G.remove_edge(current_vertex, next_vertex, next_key)


def eulerian_circuit(G, source=None, keys=False):
    """Returns an iterator over the edges of an Eulerian circuit in `G`.

    An *Eulerian circuit* is a closed walk that includes each edge of a
    graph exactly once.

    Parameters
    ----------
    G : NetworkX graph
       A graph, either directed or undirected.

    source : node, optional
       Starting node for circuit.

    keys : bool
       If False, edges generated by this function will be of the form
       ``(u, v)``. Otherwise, edges will be of the form ``(u, v, k)``.
       This option is ignored unless `G` is a multigraph.

    Returns
    -------
    edges : iterator
       An iterator over edges in the Eulerian circuit.

    Raises
    ------
    NetworkXError
       If the graph is not Eulerian.

    See Also
    --------
    is_eulerian

    Notes
    -----
    This is a linear time implementation of an algorithm adapted from [1]_.

    For general information about Euler tours, see [2]_.

    References
    ----------
    .. [1] J. Edmonds, E. L. Johnson.
       Matching, Euler tours and the Chinese postman.
       Mathematical programming, Volume 5, Issue 1 (1973), 111-114.
    .. [2] http://en.wikipedia.org/wiki/Eulerian_path

    Examples
    --------
    To get an Eulerian circuit in an undirected graph::

        >>> G = nx.complete_graph(3)
        >>> list(nx.eulerian_circuit(G))
        [(0, 2), (2, 1), (1, 0)]
        >>> list(nx.eulerian_circuit(G, source=1))
        [(1, 2), (2, 0), (0, 1)]

    To get the sequence of vertices in an Eulerian circuit::

        >>> [u for u, v in nx.eulerian_circuit(G)]
        [0, 2, 1]

    """
    if not is_eulerian(G):
        raise nx.NetworkXError("G is not Eulerian.")
    G = G.__class__(G)
    if G.is_directed():
        G.reverse(copy=False)
    if source is None:
        source = arbitrary_element(G)
    if G.is_multigraph():
        for u, v, k in _multigraph_eulerian_circuit(G, source):
            if keys:
                yield u, v, k
            else:
                yield u, v
    else:
        for u, v in _simplegraph_eulerian_circuit(G, source):
            yield u, v
