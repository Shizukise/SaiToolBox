from PySide6.QtWidgets import QFileDialog, QMessageBox
import fitz
import os


class FileOperator:
    def __init__(self, parent, test="TEST"):
        self.test = test
        self.upload_folder = "/home/galopin/Wa Its/src/data/PreResize"
        self.parent = parent
        self.pdf_files = []
        self.output_path = "/home/galopin/Wa Its/src/data/PostResize"
        self.widths_points = {
                        "A4": 595.28,
                        "A3": 841.89,
                        "A2": 1190.55,
                        "A1": 1683.78,
                        "A0": 2383.78
                        }
        self.heights_points = {
                        "A4": 841.89,
                        "A3": 1190.55,
                        "A2": 1683.78,
                        "A1": 2383.78,
                        "A0": 3370.79
                        }



    def upload_files(self, parent):
        """ Function connected to the upload file button. """
        file_paths, _ = QFileDialog.getOpenFileNames(parent, "Sélectionnez un fichier", "", ";Fichiers PDF (*.pdf)")
        if file_paths:
            try:
                for file_path in file_paths:
                    file_name = os.path.basename(file_path)
                    destination_path = os.path.join(self.upload_folder, file_name)
                    # Ensure the upload folder exists
                    os.makedirs(self.upload_folder, exist_ok=True)
                    shutil.copy(file_path, destination_path)
                QMessageBox.information(parent, "Téléversement réussi", f"Le fichier a été téléversé.")
            except Exception as e:
                QMessageBox.critical(parent, "Exception", f"{str(e)}")
        else:
            QMessageBox.warning(parent, "Aucun fichier sélectionné", "Veuillez sélectionner un fichier à téléverseur.")

    def folder_reader(self, parent_list):
        for filename in os.listdir(self.upload_folder):
            if filename.endswith('.pdf'):
                self.pdf_files.append(os.path.join(filename))
                if filename not in parent_list:
                    parent_list.append(filename)

    def resizeFiles(self, format, files):
        for file_name in files.keys():
            file_path = os.path.join(self.upload_folder, file_name)
            if os.path.exists(file_path):
                doc = fitz.open(file_path)
                new_doc = fitz.open()
                for page in doc:
                    current_rectangle = page.rect
                    scale_x = self.widths_points[format] / current_rectangle.width
                    scale_y = self.heights_points[format] / current_rectangle.height
                    scale = min(scale_x, scale_y)
                    matrix = fitz.Matrix(scale, scale)
                    new_page = new_doc.new_page(width=self.widths_points[format], height=self.heights_points[format])
                    new_page.show_pdf_page(new_page.rect, doc, page.number, matrix)
                new_doc.save(os.path.join(self.output_path, f"{file_name[:-4]}-Resize{format}.pdf"))
                new_doc.close()
                doc.close()

            else:
                print(f"File not found: {file_path}")