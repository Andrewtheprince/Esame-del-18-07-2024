import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def fillDD(self):
        nCromosomi = self._model.getNCromosomi()
        for n in nCromosomi:
            self._view.dd_min_ch.options.append(ft.dropdown.Option(n))
            self._view.dd_max_ch.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def handle_graph(self, e):
        nMin = self._view.dd_min_ch.value
        nMax = self._view.dd_max_ch.value
        if nMin > nMax:
            self._view.create_alert("Devi inserire un valore più piccolo in nMin confronto a nMax!")
            return
        self._model.buildGraph(nMin, nMax)
        nodi, archi = self._model.getGraphDetails()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Creato grafo con {nodi} nodi e {archi} archi!"))
        top5 = self._model.getTop5Nodes()
        self._view.txt_result1.controls.append(ft.Text(""))
        self._view.txt_result1.controls.append(ft.Text("I 5 nodi con il maggior numero di archi uscenti sono:"))
        for i in range(5):
            nodo = top5[i]
            self._view.txt_result1.controls.append(ft.Text(f"{nodo[0]} | num.archi uscenti: {nodo[1]} | peso tot.: {nodo[2]}"))
        self._view.update_page()

    def handle_dettagli(self, e):
        pass


    def handle_path(self, e):
        pass