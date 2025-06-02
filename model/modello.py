import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapGeni = {}

    @staticmethod
    def getNCromosomi():
        return DAO.getNCromosomi()

    def buildGraph(self, nMin, nMax):
        geni = DAO.get_all_genes(nMin, nMax)
        self._graph.add_nodes_from(geni)
        for gene in geni:
            self._idMapGeni[gene.GeneID] = gene
        archi = DAO.get_all_interactions(self._idMapGeni)


    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getTop5Nodes(self):
        return [("ciao", 3, 4)]