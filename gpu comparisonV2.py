import json
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit , QHBoxLayout , QPushButton, QTableWidget, QTableWidgetItem
import sys
import os

def loadJson(JsonPath):
    if not os.path.exists(JsonPath):
        print(f"File not found: {JsonPath}, creating a new one.")
        default_data = []
        with open(JsonPath, 'w', encoding='utf-8') as json_file:
            json.dump(default_data, json_file, indent=4)
        return default_data
    with open(JsonPath, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def writeJson(jsonData,jsonPath):
    if not os.path.exists(jsonPath):
        os.makedirs(os.path.dirname(jsonPath), exist_ok=True)
    with open(jsonPath, "w", encoding="utf-8") as f:
            json.dump(jsonData, f, indent=4, ensure_ascii=False)
    print(f"json file written at {jsonPath}")

benchmarkBlenderData = loadJson("benchmarkBlender.json")
gpusResultData = loadJson("gpusResult.json")
gpus = benchmarkBlenderData["body"]
gpus = sorted(benchmarkBlenderData["body"], key=lambda x: x[0].lower(), reverse=True)
gpusResult = []
# constructors = []
# model=[]
# fullnames = []
# for gpu in gpus:
#     split = gpu[0].split(" ")
#     constructorName = split[0]
#     constructors.append(constructorName)
#     modelName = " ".join(split[1:])
#     model.append(modelName)
#     fullname = gpu[0]
#     fullnames.append(fullname)
# constructors = list(set(constructors))

class GPUScoreViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPU Benchmark Viewer")
        
        self.dropdown = QComboBox()
        self.importButton = QPushButton()
        self.importButton.setText("Import")
        self.exportButton = QPushButton()
        self.exportButton.setText("export")
        self.addButton = QPushButton()
        self.addButton.setText("add")

        self.dropdown.addItems([gpu[0] for gpu in gpus])
        self.dropdown.currentIndexChanged.connect(self.update_label)
        # self.dropdownConstructor = QComboBox()
        # self.dropdownConstructor.addItems([modelname for modelname in model])
        self.priceLineEdit = QLineEdit()
        self.priceLineEdit.setPlaceholderText("Enter GPU price")
        self.priceLineEdit.textChanged.connect(self.update_label)
        self.linkLineEdit = QLineEdit()
        self.linkLineEdit.setPlaceholderText("Enter GPU link")
        self.priceLineEdit.setPlaceholderText("Enter GPU price")
        self.label = QLabel("Select a GPU to see its score")
        self.labelResutlt = QLabel("Select a GPU to see its score")

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.importButton)
        # buttonLayout.addWidget(self.exportButton)
        buttonLayout.addWidget(self.addButton)

        layoutDropdown = QHBoxLayout()
        layoutDropdown.addWidget(self.dropdown)
        # layoutDropdown.addWidget(self.dropdownConstructor)


        self.layout = QVBoxLayout()
        self.layout.addLayout(layoutDropdown)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.priceLineEdit)
        self.layout.addWidget(self.labelResutlt)
        self.layout.addWidget(self.linkLineEdit)
        self.layout.addLayout(buttonLayout)
        self.setLayout(self.layout)
        self.update_label()  # Show the first GPU's score initially

        self.importButton.clicked.connect(self.importData)
        # self.exportButton.clicked.connect(self.exportData)
        self.addButton.clicked.connect(self.addEntry)
        
    def createTable(self):
        gpusResultData = loadJson("gpusResult.json")
        
        if hasattr(self, "table"):
            self.table.setRowCount(0)
        else:
            self.table = QTableWidget()
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["ratio","Name", "Score", "Price", "Link"])
            self.layout.addWidget(self.table)

        self.table.setRowCount(len(gpusResultData))
        for row, entry in enumerate(gpusResultData):
            self.table.setItem(row, 0, QTableWidgetItem(entry.get("ratio", "")))
            self.table.setItem(row, 1, QTableWidgetItem(entry.get("name", "")))
            self.table.setItem(row, 2, QTableWidgetItem(str(entry.get("score", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(entry.get("price", "")))
            self.table.setItem(row, 4, QTableWidgetItem(entry.get("link", "")))

    def importData(self):
        # fill this function with a code that import a json file and update the gpus list
        pass
    
    def addEntry(self):
        name = self.dropdown.currentText()
        try:
            score = next(gpu[1] for gpu in gpus if gpu[0] == name)
        except StopIteration:
            score = 0  # fallback
        ratio = self.labelResutlt.text()
        price = self.priceLineEdit.text()
        link = self.linkLineEdit.text()
        new_entry = {
            'ratio':ratio, 
            'name':name, 
            'score':score, 
            'price':price, 
            'link':link
            }
        gpusResultData = loadJson("gpusResult.json")
        gpusResultData.append(new_entry)
        writeJson(gpusResultData,"gpusResult.json")
        self.createTable()

    def update_label(self):
        index = self.dropdown.currentIndex()
        price = self.priceLineEdit.text()
        gpu_name, score, _ = gpus[index]
        self.label.setText(f"{gpu_name}: Median Score: {score}")
        result = score / float(price) if price else 0
        self.labelResutlt.setText(f"point per euro ={result}")
        

# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = GPUScoreViewer()
    viewer.show()
    sys.exit(app.exec_())
