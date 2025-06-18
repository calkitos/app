import PySimpleGUI as sg
from pathlib import Path
from get_data import analyze_pdfs
from make_dataset import create_csvs


class GUI:
    def run():
        layout = [
            [sg.Text("Selecciona el folder que contiene los PDFs a analizar:")],
            [sg.Input(key="-INPUT_FOLDER-"), sg.FolderBrowse()],
            [sg.Text("Selecciona el folder que recibirá los archivos resultantes:")],
            [sg.Input(key="-OUTPUT_FOLDER-"), sg.FolderBrowse()],
            [sg.Button("Comenzar"), sg.Button("SALIR")],
            [sg.Text("¡ATENCIÓN!: Si los archivos ya existen en el folder de destino, serán remplazados.")]
        ]

        window = sg.Window("Analizador de PDFs para Karen", layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "SALIR":
                break
            if event == "Comenzar":
                # print("Selected file:", values["-INPUT_FOLDER-"])
                analyze_pdfs(Path(values["-INPUT_FOLDER-"]),Path(values["-OUTPUT_FOLDER-"]))
                create_csvs(Path(values["-OUTPUT_FOLDER-"]))

                sg.popup(f"""
                Proceso concluido con éxito.
                -Se han creado archivos auxiliares en la carpeta {values["-OUTPUT_FOLDER-"]}/raw.
                -Se han creado archivos csv en {values["-OUTPUT_FOLDER-"]}
                """, title="Proceso finalizado")
        window.close()


def main():
    my_gui = GUI
    my_gui.run()


if __name__=="__main__":
    main()
