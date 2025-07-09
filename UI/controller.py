import flet as ft
from UI.view import View
from model.modello import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillddLocalization(self):

        localization = self._model.getAllLocalization()
        for l in localization:
            self._view.dd_localization.options.append( ft.dropdown.Option(l) )

    def handle_graph(self, e):

        localization = self._view.dd_localization.value
        if localization == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, inserire una localization per continuare", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(localization)
        numNodi, numArchi = self._model.getDetailsGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append( ft.Text(f"Crato grafo con {numNodi} nodi e {numArchi} archi "))

        lista = self._model.getArchiOrdinatiCrescente()
        for l in lista:
            self._view.txt_result.controls.append(ft.Text(f"{l[0].GeneID} <-> {l[1].GeneID}: peso {l[2]}"))
        self._view.update_page()

    def analyze_graph(self, e):

        connesse = self._model.getAnalisiGrafo()
        self._view.txt_result.controls.append(ft.Text(f"Le componenti connesse sono:"))

        for c in connesse:
            if len(c) > 1:
                nodi = ""
                for n in list(c):
                    nodi += f"{n.GeneID}, "
                self._view.txt_result.controls.append(ft.Text(f"{nodi} | dimensione componente= {len(c)}"))
        self._view.update_page()


    def handle_path(self, e):

        self._view.txt_result.controls.clear()
        setNodi, compConnesse = self._model.getPath()

        self._view.txt_result.controls.append(ft.Text(f"Trovato set con dimensione {len(setNodi)}"))
        for p in setNodi:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))

        self._view.txt_result.controls.append(ft.Text(f"Numero componenti connesse: {compConnesse} "))
        self._view.update_page()

