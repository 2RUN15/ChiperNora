from PyQt6.QtWidgets import QFileDialog

#Dosya Seçme
def chose_file(self):
    file_path,_ = QFileDialog.getOpenFileName(
        self,
        "Choose File",
        "",
        "TXT Files (*.txt);;MD Files (*.md);;ALL Files (*.*)"
    )
    
    if file_path:
        return file_path

#Klasör Seçme
def chose_folder(self):
    folder_path = QFileDialog.getExistingDirectory(self,"Choose Folder")
    
    if folder_path:
        return folder_path
