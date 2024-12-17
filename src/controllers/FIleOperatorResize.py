from PySide6.QtWidgets import QFileDialog, QMessageBox
import fitz, os, shutil
from src.utils.ResizeConfig import *
import fitz
class FileOperator:

    """
    A class for handling file operations, including uploading files, reading folders, and resizing PDF files.

    Methods:
        upload_files: Uploads selected files to a predefined folder.
        folder_reader: Reads the files in the upload folder and adds them to a list.
        resizeFiles: Resizes the selected files to a specified format and saves them.
    """

    def __init__(self, parent, test="TEST"):
        self.test = test
        self.upload_folder = "/home/galopin/Wa Its/src/data/PreResize"
        self.parent = parent
        self.pdf_files = []
        self.output_path = "/home/galopin/Wa Its/src/data/PostResize"
        self.widths_points = widths_points
        self.heights_points = heights_points
        self.custom_format = None

    def upload_files(self, parent):

        """ Function connected to the upload file button.
            This will upload files to desired folder by making a copy of the original """
        
        print(self.custom_format)
        file_paths, _ = QFileDialog.getOpenFileNames(parent, "Sélectionnez un fichier", "", ";Fichiers PDF (*.pdf)")
        if file_paths:
            try:
                """For each file_path selected by user, method will get its filename (base file name)
                   It will create a new path for the new file using the upload folder path + the file name
                   For example \folderX + fileX.join >> \FolderX\FileX
                   After having the new path and the file, we make sure the upload path exists, and we make a copy
                   of the desired file using shutil, passing the file and the later created path \FolderX\FileX """
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

        """Method to iterate trough predefined folder (Folder designated to be the upload folder)
           That gets all the file names on it, the is a control in the upload folder to only accept pdf files
           but here also we check for it once again."""

        for filename in os.listdir(self.upload_folder):    #The upload folder belongs to the file operator class
            if filename.endswith('.pdf'):                   #All we pass to the Resize widget (main widget) is the names of the files
                self.pdf_files.append(os.path.join(filename))  
                if filename not in parent_list:             #And a small check, to append only files that have not already been passed 
                    parent_list.append(filename)                #to main widget before.


    def resizeFilesA(self, format, files):
        """
        Resizes the provided PDF files to the specified format, scaling the pages while preserving the content.
        Method A. Will be called for basic formats [A4,A3,A2,A1,A0, 300x500]

        Args:
            format (str): The target format for resizing (e.g., "A4", "A3", etc.).
            files (dict): A dictionary containing filenames to resize. The dictionary keys are filenames.

        This method:
        - Opens each PDF file in the specified folder.
        - Calculates the required scaling factor based on the target format's dimensions.
        - Resizes the pages proportionally while preserving the aspect ratio.
        - Saves the resized PDFs with a new name.
        - Deletes the original PDF file after resizing.
        """
        for file_name in files.keys():
            file_path = os.path.join(self.upload_folder, file_name)
            if os.path.exists(file_path):
                doc = fitz.open(file_path)  # Open the original PDF
                new_doc = fitz.open()  # Create a new empty document
                for page in doc:  # Iterate through each page in the original document
                    current_rectangle = page.rect
                    # Calculate scale factors based on the target format's dimensions
                    scale_x = self.widths_points[format] / current_rectangle.width
                    scale_y = self.heights_points[format] / current_rectangle.height
                    scale = min(scale_x, scale_y)  # Use the smaller scale factor to preserve aspect ratio
                    matrix = fitz.Matrix(scale, scale)  # Create a transformation matrix for scaling
                    if current_rectangle.width > current_rectangle.height: #This means file is oriented in horizontal:
                        new_page = new_doc.new_page(width=self.heights_points[format], height=self.widths_points[format]) #We save it with inverted values, so it becomes horizontal also
                    else:
                        new_page = new_doc.new_page(width=self.widths_points[format], height=self.heights_points[format])
                    
                # Apply the transformation matrix to the page and add it to the new document
                new_page.show_pdf_page(new_page.rect, doc, page.number, matrix)
                # Save the resized PDF with the new format name
                new_doc.save(os.path.join(self.output_path, f"{file_name[:-4]}-Resize{format}.pdf"))
                new_doc.close()
                doc.close()
                os.remove(file_path)  # Remove the original file after resizing
            else:
                print(f"File not found: {file_path}")

    def ResizeFilesB(self,files,horizontal,custom_format):
        """
        Resizes the provided PDF files to the specified format, scaling the pages while preserving the content.
        Method B. Will be called for custom formats.
        Args:
            format (str): User input ex (620x1280).
            files (dict): A dictionary containing filenames to resize. The dictionary keys are filenames.

        This method:
        - Opens each PDF file in the specified folder.
        - Calculates the required scaling factor based on the target format's dimensions.
        - Resizes the pages proportionally while preserving the aspect ratio.
        - Saves the resized PDFs with a new name.
        - Deletes the original PDF file after resizing.
        """

        #This should take an input like 600 x 1280 and split it at X.
        #If it is horizontal then the max value is the width, so first check to be done is orientation
        #After having both orientation and widthxheight , simply resize as normal
        width = None
        heigth = None
        custom_format_values = custom_format.split("x")
        if custom_format_values[0] > custom_format_values[1]:
            heigth = int(custom_format_values[0]) * 2.83465
            width = int(custom_format_values[1]) * 2.83465
        else:
            heigth = int(custom_format_values[1]) * 2.83465
            width = int(custom_format_values[0]) * 2.83465
        print(custom_format_values)
        for file_name in files:
            file_path = os.path.join(self.upload_folder, file_name)
            if os.path.exists(file_path):
                doc = fitz.open(file_path)  # Open the original PDF
                new_doc = fitz.open()  # Create a new empty document
                for page in doc:  # Iterate through each page in the original document
                    current_rectangle = page.rect
                    # Calculate scale factors based on the target format's dimensions
                    scale_x = width / current_rectangle.width
                    scale_y = heigth / current_rectangle.height
                    scale = min(scale_x, scale_y)  # Use the smaller scale factor to preserve aspect ratio
                    matrix = fitz.Matrix(scale, scale)  # Create a transformation matrix for scaling
                    if horizontal: 
                        new_page = new_doc.new_page(width=heigth, height=width) 
                    else:
                        new_page = new_doc.new_page(width=width, height=heigth)
                # Apply the transformation matrix to the page and add it to the new document
                new_page.show_pdf_page(new_page.rect, doc, page.number, matrix)
                # Save the resized PDF with the new format name
                new_doc.save(os.path.join(self.output_path, f"{file_name[:-4]}-Resize{custom_format}.pdf"))
                new_doc.close()
                doc.close()
                os.remove(file_path)  # Remove the original file after resizing
            else:
                print(f"File not found: {file_path}")
    