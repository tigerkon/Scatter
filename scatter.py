from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import random


def maya_main_window():
    main_window = omui.MQtUtil_mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.explode = Explode()
        self.vertex = CreateVertex()
        self.setWindowTitle("Scatter")
        self.setMinimumWidth(500)
        self.setMinimumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 18px")
        self.scatter_layout = self._scatter_layout()
        self.vertex_layout = self.vert_place_ui()
        self.cnl_btn_layout = self.create_cancel_btn()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.scatter_layout)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.vertex_layout)
        self.main_lay.addLayout(self.cnl_btn_layout)
        self.setLayout(self.main_lay)

    def create_cancel_btn(self):
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.cancel_btn)
        return layout

    def scatter_header(self):
        self.scatter_scl_lvl = QtWidgets.QLabel("Scatter Y plane")
        self.scatter_scl_lvl.setStyleSheet("font: bold")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_scl_lvl, 0, 0)
        return layout

    def _scatter_layout(self):
        layout = self.scatter_header()
        self.scatter_dsbx_min = QtWidgets.QDoubleSpinBox()
        self.scatter_dsbx_min.setSuffix(" Scale Min")
        self.scatter_dsbx_min.setMinimumWidth(100)
        self.scatter_dsbx_min.setMinimum(1)
        self.scatter_rot_min = QtWidgets.QDoubleSpinBox()
        self.scatter_rot_min.setSuffix(" Rot Max")
        self.scatter_rot_min.setMinimumWidth(100)
        self.scatter_rot_min.setMaximum(360)
        self.scatter_dsbx_max = QtWidgets.QDoubleSpinBox()
        self.scatter_dsbx_max.setSuffix(" Scale Max")
        self.scatter_dsbx_max.setMinimumWidth(100)
        self.scatter_dsbx_max.setMinimum(1)
        self.scatter_amount = QtWidgets.QSpinBox()
        self.scatter_amount.setSuffix(" Amount")
        self.scatter_amount.setMinimumWidth(100)
        self.scatter_amount.setMinimum(1)
        self.scatter_seed = QtWidgets.QSpinBox()
        self.scatter_seed.setSuffix(" Enter 4 numbers")
        self.scatter_seed.setMinimumWidth(100)
        self.scatter_seed.setMinimum(1)
        self.scatter_seed.setMaximum(9999)
        self.scatter_y = QtWidgets.QDoubleSpinBox()
        self.scatter_y.setSuffix(" Y Height")
        self.scatter_y.setMinimumWidth(100)
        '''self.scatter_rot_max = QtWidgets.QDoubleSpinBox()
        self.scatter_rot_max.setSuffix(" Rot Max")
        self.scatter_rot_max.setMinimumWidth(100)
        self.scatter_rot_max.setMaximum(360)'''
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout.addWidget(self.scatter_dsbx_min, 1, 0)
        layout.addWidget(self.scatter_dsbx_max, 1, 1)
        layout.addWidget(self.scatter_rot_min, 1, 2)
        layout.addWidget(self.scatter_y, 1, 3)
        layout.addWidget(self.scatter_amount, 1, 4)
        layout.addWidget(self.scatter_seed, 1, 5)
        # layout.addWidget(self.scatter_rot_max, 1, 3)
        layout.addWidget(self.scatter_btn, 2, 2)
        return layout

    def vert_place_header(self):
        self.scatter_scl_lbl = QtWidgets.QLabel("Vertex Scatter")
        self.scatter_scl_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_scl_lbl, 0, 0)
        return layout

    def vert_place_ui(self):
        layout = self.vert_place_header()
        self.scatter_vert_header_lbl = QtWidgets.QLabel("Vertex Placement")
        self.scatter_vert_header_lbl.setStyleSheet("font: bold")
        self.vert_scl_min = QtWidgets.QDoubleSpinBox()
        self.vert_scl_min.setSuffix(" Scale Min")
        self.vert_scl_min.setMaximumWidth(100)
        self.vert_scl_min.setMinimum(1)
        self.vert_scl_max = QtWidgets.QDoubleSpinBox()
        self.vert_scl_max.setSuffix(" Scale Max")
        self.vert_scl_max.setMinimumWidth(100)
        self.vert_scl_max.setMinimum(1)
        self.vert_rot_min = QtWidgets.QDoubleSpinBox()
        self.vert_rot_min.setSuffix(" Rot Max")
        self.vert_rot_min.setMinimumWidth(100)
        self.vert_rot_min.setMinimum(0)
        self.vert_rot_min.setMaximum(360)
        '''self.vert_rot_max = QtWidgets.QDoubleSpinBox()
        self.vert_rot_max.setSuffix(" Rot Max")
        self.vert_rot_max.setMinimumWidth(100)
        self.vert_rot_max.setMinimum(0)
        self.vert_rot_max.setMaximum(360)'''
        self.normal_checkbox = QtWidgets.QCheckBox("normals")
        self.vert_btn = QtWidgets.QPushButton("Vert Placement")
        layout.addWidget(self.vert_scl_min, 1, 0)
        layout.addWidget(self.vert_scl_max, 1, 1)
        layout.addWidget(self.vert_rot_min, 1, 2)
        # layout.addWidget(self.vert_rot_max, 1, 3)
        layout.addWidget(self.normal_checkbox, 1, 3)
        layout.addWidget(self.vert_btn, 1, 4)
        return layout

    def create_connections(self):
        self.cancel_btn.clicked.connect(self.cancel)
        self.scatter_btn.clicked.connect(self.do_scatter)
        self.vert_btn.clicked.connect(self.vertex_plc)
        self.scatter_dsbx_min.valueChanged.connect(self.
                                                   set_dbsx_value_min)
        self.scatter_dsbx_max.valueChanged.connect(self.
                                                   set_dbsx_value_max)
        self.scatter_y.valueChanged.connect(self.set_y)
        self.scatter_rot_min.valueChanged.connect(self.set_dbsx_rot_min)
        self.scatter_amount.valueChanged.connect(self.set_amount)
        self.scatter_seed.valueChanged.connect(self.set_seed)
        # self.scatter_rot_max.valueChanged.connect(self.set_dbsx_rot_max)
        self.vert_scl_min.valueChanged.connect(self.set_vert_min)
        self.vert_scl_max.valueChanged.connect(self.set_vert_max)
        self.vert_rot_min.valueChanged.connect(self.set_rot_min)
        # self.vert_rot_max.valueChanged.connect(self.set_rot_max)
        self.normal_checkbox.stateChanged.connect(self.vert_normals)

    def set_dbsx_value_min(self):
        self.explode.scale_min = self.scatter_dsbx_min.value()

    def set_dbsx_value_max(self):
        self.explode.scale_max = self.scatter_dsbx_max.value()

    def set_dbsx_rot_min(self):
        self.explode.rotation_min = self.scatter_rot_min.value()

    def set_y(self):
        self.explode.y_pos = self.scatter_y.value()

    def set_amount(self):
        self.explode.number_obj = self.scatter_amount.value()

    def set_seed(self):
        self.explode.seed_num = self.scatter_seed.value()

    '''def set_dbsx_rot_max(self):
        self.explode.rotation_max = self.scatter_dsbx_max.value()'''

    def set_vert_min(self):
        self.vertex.scale_min = self.vert_scl_min.value()

    def set_vert_max(self):
        self.vertex.scale_max = self.vert_scl_max.value()

    def set_rot_min(self):
        self.vertex.rotation_min = self.vert_rot_min.value()

    '''def set_rot_max(self):
        self.vertex.rotation_max = self.vert_rot_max.value()'''

    def vert_normals(self):
        if self.normal_checkbox.isChecked():
            self.vertex.normal = True
        else:
            self.vertex.normal = False
        print(self.vertex.normal)

    @QtCore.Slot()
    def vertex_plc(self):
        self.set_vert_min()
        self.set_vert_max()
        self.set_rot_min()
        # self.set_rot_max()
        self.vert_normals()
        self.vertex.Vertex_Inst()

    @QtCore.Slot()
    def do_scatter(self):
        self.set_dbsx_value_min()
        self.set_dbsx_value_max()
        self.set_dbsx_rot_min()
        # self.set_dbsx_rot_max()
        self.set_y()
        self.set_amount()
        self.set_seed()
        self.explode.scatter_shot()

    @QtCore.Slot()
    def cancel(self):
        self.close()


class CreateVertex(object):
    def __init__(self):
        self.rotation_min = 0
        # self.rotation_max = 360
        self.scale_min = 1
        self.scale_max = 2
        self.normal = False

    def Vertex_Inst(self):
        random.seed(1534)
        print(self.normal)
        result = cmds.ls(orderedSelection=True)
        vertex_name = cmds.filterExpand(expand=True, selectionMask=31)
        inst_obj = result[0]
        instance_group_name = cmds.group(empty=True, name=inst_obj +
                                                          '_instance_grp#')
        cmds.xform(instance_group_name, centerPivots=True)
        if cmds.objectType(inst_obj) == 'transform':
            for vertex in vertex_name:
                instance_result = cmds.instance(inst_obj, name=inst_obj + "_instance#")
                cmds.parent(instance_result, instance_group_name)
                self.random_rotation(instance_result)
                self.random_scaling(instance_result)
                if self.normal:
                    print("normals")
                    cmds.normalConstraint(vertex_name, inst_obj, aimVector=[0, 1, 0])
                    x_ver, y_ver, z_ver = cmds.pointPosition(vertex)
                    cmds.move(x_ver, y_ver, z_ver)
                else:
                    print("not normals")
                    x_ver, y_ver, z_ver = cmds.pointPosition(vertex)
                    cmds.move(x_ver, y_ver, z_ver)
        else:
            print "ERROR"

        # cmds.hide(inst_obj)

    def random_rotation(self, instance_result):
        x_rot = random.uniform(0, self.rotation_min)
        y_rot = random.uniform(0, self.rotation_min)
        z_rot = random.uniform(0, self.rotation_min)
        cmds.rotate(x_rot, y_rot, z_rot, instance_result)

    def random_scaling(self, instance_result):
        min_value = self.scale_min
        max_value = self.scale_max
        print max_value
        scaling_factor = random.uniform(min_value, max_value)
        cmds.scale(scaling_factor, scaling_factor,
                   scaling_factor, instance_result)


class Explode(object):
    def __init__(self):
        self.rotation_min = 0
        # self.rotation_max = 360
        self.scale_min = 1
        self.scale_max = 2
        self.y_pos = 0
        self.number_obj = 1
        self.seed_num = 1234

    def scatter_shot(self):
        random.seed(self.seed_num)
        result = cmds.ls(orderedSelection=True)

        inst_obj = result[0]
        instance_group_name = cmds.group(empty=True, name=inst_obj +
                                                          '_instance_grp#')
        for i in range(0, self.number_obj):
            instance_result = cmds.instance(inst_obj, name=inst_obj + "_instance#")
            cmds.parent(instance_result, instance_group_name)
            self.random_movement(instance_result)
            self.random_rotation(instance_result)
            self.random_scaling(instance_result)

        # cmds.hide(inst_obj)
        cmds.xform(instance_group_name, centerPivots=True)

    def random_movement(self, instance_result):
        x = random.uniform(-10, 10)
        y = self.y_pos
        z = random.uniform(-10, 10)
        cmds.move(x, y, z, instance_result)

    def random_rotation(self, instance_result):
        x_rot = random.uniform(0, self.rotation_min)
        y_rot = random.uniform(0, self.rotation_min)
        z_rot = random.uniform(0, self.rotation_min)
        cmds.rotate(x_rot, y_rot, z_rot, instance_result)

    def random_scaling(self, instance_result):
        min_value = self.scale_min
        max_value = self.scale_max
        print min_value
        print max_value
        scaling_factor = random.uniform(min_value, max_value)
        cmds.scale(scaling_factor, scaling_factor,
                   scaling_factor, instance_result)
