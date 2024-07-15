import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def buildGraph(self,a,b):
        self._graph.clear()
        nodes = DAO.getNodes(a, b)
        self._idMap = {node.GeneID: node for node in nodes}


        edges = DAO.getEdges(self._idMap, a, b)

        self._graph.add_nodes_from(nodes)
        # self._graph.add_weighted_edges_from(edges)
        for e in edges:
            # print(e[0].Chromosome, e[1].Chromosome)
            if e[0].Chromosome == e[1].Chromosome:
                self._graph.add_weighted_edges_from([(e[0], e[1], e[2])])
                self._graph.add_weighted_edges_from([(e[1], e[0], e[2])])
            elif e[0].Chromosome < e[1].Chromosome:
                self._graph.add_weighted_edges_from([(e[0], e[1], e[2])])
            else:
                self._graph.add_weighted_edges_from([(e[1], e[0], e[2])])
        print(self.getGraphDetails())

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getConnesse(self):
        return nx.weakly_connected_components(self._graph)

    def getChromosomeVals(self):
        return DAO.getChromosomeVals()

    def getLocalization(self):
        return DAO.getLocalization()

    def getNodesOfLocation(self, loc):
        res = []
        nodes = list(self._graph.nodes())
        for n in nodes:
            if n.Localization == loc:
                res.append(n)
        return res