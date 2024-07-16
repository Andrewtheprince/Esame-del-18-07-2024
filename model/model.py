import networkx as nx

from database.DAO import DAO
from model.gene import Gene


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._localization_map = {}
        self._correlations_map = {}
        self.get_all_correlations()

    def get_all_correlations(self):
        DAO.get_all_correlations(self._correlations_map)

    def get_chromosomes(self):
        return DAO.get_all_chromosomes()

    def get_localizations(self):
        return DAO.get_all_localizations()

    def get_peso(self, g1: Gene, g2: Gene):
        return DAO.get_peso(g1, g2)

    def get_localization_gene(self, g: Gene):
        if g.GeneID in self._localization_map:
            return self._localization_map[g.GeneID]
        else:
            return DAO.get_localization_gene(g, self._localization_map)

    def build_graph(self, ch_min, ch_max):
        self._graph.clear()
        nodes = DAO.get_nodes(ch_min, ch_max)
        self._graph.add_nodes_from(nodes)

        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if self.get_localization_gene(nodes[i]) == self.get_localization_gene(nodes[j]) and nodes[i].GeneID != nodes[j].GeneID:
                    if (nodes[i].GeneID, nodes[j].GeneID) in self._correlations_map:
                        peso = self._correlations_map[(nodes[i].GeneID, nodes[j].GeneID)]
                        if nodes[i].Chromosome < nodes[j].Chromosome:
                            self._graph.add_edge(nodes[i], nodes[j], weight=peso)

                        elif nodes[i].Chromosome > nodes[j].Chromosome:
                            self._graph.add_edge(nodes[j], nodes[i], weight=peso)
                        else:
                            self._graph.add_edge(nodes[i], nodes[j], weight=peso)
                            self._graph.add_edge(nodes[j], nodes[i], weight=peso)

        # self._idMap = {node.GeneID: node for node in nodes}
        #
        #
        # edges = DAO.getEdges(self._idMap, a, b)
        #
        # self._graph.add_nodes_from(nodes)
        # # self._graph.add_weighted_edges_from(edges)
        # for e in edges:
        #     # print(e[0].Chromosome, e[1].Chromosome)
        #     if e[0].Chromosome == e[1].Chromosome:
        #         self._graph.add_weighted_edges_from([(e[0], e[1], e[2])])
        #         self._graph.add_weighted_edges_from([(e[1], e[0], e[2])])
        #     elif e[0].Chromosome < e[1].Chromosome:
        #         self._graph.add_weighted_edges_from([(e[0], e[1], e[2])])
        #     else:
        #         self._graph.add_weighted_edges_from([(e[1], e[0], e[2])])
        # print(self.getGraphDetails())

    def num_nodes(self):
        return len(self._graph.nodes)

    def nodes(self):
        return self._graph.nodes

    def num_edges(self):
        return len(self._graph.edges)

    def edges(self):
        return self._graph.edges

    def get_node_max_uscenti(self):
        sorted_nodes = sorted(self._graph.nodes(), key=lambda n: self._graph.out_degree(n), reverse=True)
        result = []
        for i in range(min(len(sorted_nodes), 5) ):
            peso_tot = 0.0
            for e in self._graph.out_edges(sorted_nodes[i],data=True):
                peso_tot += float(e[2].get("weight"))
            result.append((sorted_nodes[i], self._graph.out_degree(sorted_nodes[i]), peso_tot ) )
        return result

    def get_connesse(self):
        return nx.weakly_connected_components(self._graph)

    def get_nodes_location(self, loc):
        res = []
        nodes = list(self._graph.nodes())
        for n in nodes:
            if self._localization_map[n.GeneID] == loc:
                res.append(n)
        return res