import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        a = self._view.ddA.value
        b = self._view.ddB.value
        self._model.buildGraph(a, b)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text("Grafo creato:"))
        n,a = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi:{n}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi:{a}"))
        self._view.update_page()

    def handle_dettagli(self, e):
        loc = self._view.ddDettagli.value
        nodes = self._model.getNodesOfLocation(loc)
        self._view.txt_result1.controls.append(ft.Text(f"Geni con location {loc}:"))
        for n in nodes:
            self._view.txt_result1.controls.append(ft.Text(f"{n}"))

        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDDs(self):
        values = self._model.getChromosomeVals()
        self._view.ddA.options = list(map(lambda x: ft.dropdown.Option(x), values))
        self._view.ddB.options = list(map(lambda x: ft.dropdown.Option(x), values))

    def fillDDLocalization(self):
        values = self._model.getLocalization()
        self._view.ddDettagli.options = list(map(lambda x: ft.dropdown.Option(x), values))
