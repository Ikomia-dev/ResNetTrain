from ikomia import utils, core, dataprocess
import ResNetTrain_process as processMod

# PyQt GUI framework
from PyQt5.QtWidgets import *


# --------------------
# - Class which implements widget associated with the process
# - Inherits core.CProtocolTaskWidget from Ikomia API
# --------------------
class ResNetTrainWidget(core.CProtocolTaskWidget):

    def __init__(self, param, parent):
        core.CProtocolTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = processMod.ResNetTrainParam()
        else:
            self.parameters = param

        # Create layout : QGridLayout by default
        self.grid_layout = QGridLayout()
        self.combo_model = utils.append_combo(self.grid_layout, "Model name")
        self.combo_model.addItem("resnet18")
        self.combo_model.addItem("resnet34")
        self.combo_model.addItem("resnet50")
        self.combo_model.addItem("resnet101")
        self.combo_model.addItem("resnet152")

        self.spin_workers = utils.append_spin(self.grid_layout, label="Data loader workers", value=self.parameters.num_workers, min=0, max=8, step=2)
        self.spin_batch = utils.append_spin(self.grid_layout, label="Batch size", value=self.parameters.batch_size,
                                           min=1, max=1024, step=1)
        self.spin_epoch = utils.append_spin(self.grid_layout, label="Epochs", value=self.parameters.epochs, min=1)
        self.spin_classes = utils.append_spin(self.grid_layout, label="Classes", value=self.parameters.classes, min=1)
        self.spin_size = utils.append_spin(self.grid_layout, label="Input size", value=self.parameters.input_size)
        self.check_pretrained = utils.append_check(self.grid_layout, label="Pre-trained model",
                                                  checked=self.parameters.use_pretrained)
        self.check_features = utils.append_check(self.grid_layout, label="Feature Extract mode",
                                                checked=self.parameters.feature_extract)

        label_model_format = QLabel("Model format")
        row = self.grid_layout.rowCount()
        self.grid_layout.addWidget(label_model_format, row, 0)
        self.check_pth = QCheckBox("pth")
        self.check_pth.setChecked(self.parameters.export_pth)
        self.grid_layout.addWidget(self.check_pth, row, 1)
        self.check_onnx = QCheckBox("onnx")
        self.check_onnx.setChecked(self.parameters.export_onnx)
        self.grid_layout.addWidget(self.check_onnx, row+1, 1)

        self.browse_folder = utils.append_browse_file(self.grid_layout, label="Output folder",
                                                      path=self.parameters.output_folder,
                                                      tooltip="Select output folder",
                                                      mode=QFileDialog.Directory)

        # PyQt -> Qt wrapping
        layout_ptr = utils.PyQtToQt(self.grid_layout)

        # Set widget layout
        self.setLayout(layout_ptr)

    def onApply(self):
        # Apply button clicked slot
        # Get parameters from widget
        self.parameters.num_workers = self.spin_workers.value()
        self.parameters.model_name = self.combo_model.currentText()
        self.parameters.batch_size = self.spin_batch.value()
        self.parameters.epochs = self.spin_epoch.value()
        self.parameters.classes = self.spin_classes.value()
        self.parameters.input_size = self.spin_size.value()
        self.parameters.use_pretrained = self.check_pretrained.isChecked()
        self.parameters.feature_extract = self.check_features.isChecked()
        self.parameters.export_pth = self.check_pth.isChecked()
        self.parameters.export_onnx = self.check_onnx.isChecked()
        self.parameters.output_folder = self.browse_folder.path

        # Send signal to launch the process
        self.emitApply(self.parameters)


# --------------------
# - Factory class to build process widget object
# - Inherits dataprocess.CWidgetFactory from Ikomia API
# --------------------
class ResNetTrainWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "ResNet Train"

    def create(self, param):
        # Create widget object
        return ResNetTrainWidget(param, None)
