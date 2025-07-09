import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):

        self._grafo = nx.Graph()
        self._nodes=[]

        self._bestSol = []
        self._minConnesse = None

    def getAllLocalization(self):
        return DAO.getAllLocalization()

    def buildGraph(self, localization):

        self._grafo.clear()
        self._nodes = DAO.getAllNodes(localization)
        self._grafo.add_nodes_from(self._nodes)

        self._mapNodes={}
        for n in self._nodes:
            self._mapNodes[n.GeneID] = n

        for i in DAO.get_all_interactions():
            idGene1 = i.GeneID1
            idGene2 = i.GeneID2
            # class1 = self._mapNodes[idGene1]
            # class2 = self._mapNodes[idGene2]
            if idGene1 != idGene2:
                if idGene1 in self._mapNodes and idGene2 in self._mapNodes:
                    peso = DAO.getEdgeWeight(idGene1, idGene2)
                    if len(peso)>0 and peso is not None :
                        self._grafo.add_edge( self._mapNodes[idGene1], self._mapNodes[idGene2], weight=peso[0] )

        return self._grafo

    def getDetailsGraph(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getArchiOrdinatiCrescente(self):
        listaPeso = []
        for e in self._grafo.edges(data=True):
            listaPeso.append(( e[0], e[1], e[2]['weight']) )

        listaPeso.sort(key=lambda x: x[2])
        return listaPeso

    def getAnalisiGrafo(self):

        cc = nx.connected_components(self._grafo)
        ccSorted = sorted( cc, key=lambda x: len(x), reverse=True)
        # ccMaggiori=[]
        # for c in ccSorted:
        #      if len(c)>1:
        #          ccMaggiori.append( (c, len(c) ))

        return ccSorted

    #PUNTO 2
    def getPath(self):
        self._bestSol = []
        self._minConnesse = None

        for node in self._grafo.nodes:
            if node.Essential != "":
                parziale = [node]
                self._ricorsione(parziale, node)

        return self._bestSol, self._minConnesse

    def _ricorsione(self, parziale, source):

        #terminale
        if len(parziale) > len(self._bestSol):
            self._bestSol = copy.deepcopy(parziale)
            self._minConnesse = nx.number_connected_components(nx.subgraph(self._graph, parziale))

        elif len(parziale) == len(self._bestSol):
            if nx.number_connected_components(nx.subgraph(self._graph, parziale)) < self._minConnesse:
                self._bestSol = copy.deepcopy(parziale)
                self._minConnesse = nx.number_connected_components(nx.subgraph(self._graph, parziale))

        for n in self._graph.nodes:
            if n not in parziale:
                if n.GeneID > source.GeneID and n.Essential == source.Essential:
                    parziale.append(n)
                    self._ricorsione(parziale, n)
                    parziale.pop()

if __name__ == "__main__":
    m= Model()
    m.buildGraph("vacuole")
    print(m.getDetailsGraph())
    print(m.getAnalisiGrafo())
