import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.Log import setup_logger, trackFunction
import os
from src.View.components.BaseView import BaseView
import pathlib

logger = setup_logger(loggerName="DataFrameComponent")


class DataFrameComponent(tk.Frame):
    def __init__(self, parent: tk.Tk, df: pd.DataFrame = None, fileName: str = None):
        super().__init__(parent)
        self._pd = df
        self.optionFrame: tk.Frame = None
        self._parent = parent
        self._tree: ttk.Treeview = None
        self.fileName = pathlib.Path(fileName)

        if self.pd is None:
            self.loadDataFrame()

        self._createComponent()
        self._createButtons()

    def _createComponent(self):
        columns = list(self.pd.columns)
        self._tree = ttk.Treeview(self, columns=columns, show="headings")

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center")

        for index, row in self.pd.iterrows():
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            self.tree.insert(
                "", "end", values=row.tolist(),
                tags=(tag,)
            )

        v_scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(
            self, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=v_scrollbar.set,
                            xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=1, column=0, sticky=tk.NSEW)
        v_scrollbar.grid(row=1, column=1, sticky=tk.NS)
        h_scrollbar.grid(row=2, column=0, sticky=tk.EW)

        self.grid_rowconfigure(1, weight=1, minsize=200)
        self.grid_columnconfigure(0, weight=1)

        self.tree.tag_configure("oddrow", background="#ffffff")
        self.tree.tag_configure("evenrow", background="#f2faff")

    def _createButtons(self):
        """Método para crear el Frame con los botones encima del DataFrame"""
        self.optionFrame = tk.Frame(self)
        self.optionFrame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        # Botón para cargar otro archivo
        loadButton = tk.Button(
            self.optionFrame, text="Cargar archivo", command=self.loadFile)
        loadButton.pack(side=tk.LEFT, padx=10)

        exportButton = tk.Button(
            self.optionFrame, text="Exportar archivo", command=self.exportFile)
        exportButton.pack(side=tk.LEFT, padx=10)

    def loadDataFrame(self):
        if self.fileName is None:
            error = "No se ha proporcionado ningún archivo para acceder."
            logger.error(error)
            raise ValueError(error)

        if not self.fileName.is_file():
            error = f"No es posible acceder al archivo {self.fileName}."
            logger.error(error)
            self._pd = pd.DataFrame()
            messagebox.showwarning(
                "Atención",
                f"No es posible acceder al archivo {self.fileName}.\n"
                f"Por favor, inserte el archivo"
            )

            return

        self._pd = pd.read_excel(self.fileName)

    def loadFile(self):
        newFilePath = filedialog.askopenfilename(
            title="Selecciona el archivo de las CURP",
            initialdir="~",
            filetypes=(("Archivos de Excel", "*.xlsx"),)
        )
        newFilePath = pathlib.Path(newFilePath)

        if newFilePath.is_file():

            self.fileName = newFilePath
            self.loadDataFrame()

            self.pd.to_excel(self.fileName, index=False)
            self._createComponent()

    def exportFile(self):

        defaultFileName = self.fileName.name
        newFilePath = filedialog.asksaveasfilename(
            title="Guardar archivo como",
            defaultextension=".xlsx",
            filetypes=(
                ("Archivos de Excel", "*.xlsx"),
                ("Todos los archivos", "*.*")
            ),
            initialfile=defaultFileName
        )

        newFilePath = pathlib.Path(newFilePath)

        if newFilePath.is_dir():
            self.pd.to_excel(newFilePath, index=False)
            messagebox.showinfo("Archivo exportado ",
                                f"Archivo guardado en {newFilePath}")

    def clearData(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    @property
    def pd(self):
        return self._pd

    @property
    def tree(self):
        return self._tree


if __name__ == "__main__":
    from src.Config import Config

    fileName = Config.getPath("Files", "lists_dir") / \
        "TEST" / "Lista Alumnos 2-A.xlsx"
    base = BaseView()
    component = DataFrameComponent(base.root, fileName=fileName)
    component.pack(fill=tk.BOTH, expand=True)

    base.show()
