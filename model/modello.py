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
        interazioni = DAO.get_all_interactions(self._idMapGeni)
        for interazione in interazioni:
            if self._idMapGeni[interazione.GeneID1].Chromosome > self._idMapGeni[interazione.GeneID2].Chromosome:
                self._graph.add_edge(self._idMapGeni[interazione.GeneID2],self._idMapGeni[interazione.GeneID1], weight = interazione.Expression_Corr)
            elif self._idMapGeni[interazione.GeneID1].Chromosome < self._idMapGeni[interazione.GeneID2].Chromosome:
                self._graph.add_edge(self._idMapGeni[interazione.GeneID1],self._idMapGeni[interazione.GeneID2], weight = interazione.Expression_Corr)
            else:
                self._graph.add_edge(self._idMapGeni[interazione.GeneID1], self._idMapGeni[interazione.GeneID2], weight=interazione.Expression_Corr)
                self._graph.add_edge(self._idMapGeni[interazione.GeneID2], self._idMapGeni[interazione.GeneID1], weight=interazione.Expression_Corr)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getTop5Nodes(self):
        top5nodi = [(nodo, len(list(self._graph.successors(nodo))) ,sum(d["weight"] for _,_, d in self._graph.edges(nodo, data = True))) for nodo in self._graph.nodes()]
        top5nodiOrdinati = sorted(top5nodi, key=lambda x: x[1], reverse=True)
        return top5nodiOrdinati