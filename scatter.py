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
        self.setWindowTitle("Scatter")
        self.setMinimumWidth(500)
        self.setMinimumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        lMinR = QtWidgets.QLabel("Min Rotation", self)
        oMinR = QtWidgets.QLineEdit(self)
        lMaxR = QtWidgets.QLabel("Max Rotation", self)
        oMaxR = QtWidgets.QLineEdit(self)
        lMinS = QtWidgets.QLabel("Min Scale", self)
        oMinS = QtWidgets.QLineEdit(self)
        lMasS = QtWidgets.QLabel("Max Scale", self)
        oMaxS = QtWidgets.QLineEdit(self)
        submit = QtWidgets.QPushButton("Submit", self)


def scatterObjects():
    # random.seed(1234)
    result = cmds.ls(orderedSelection=True)
    print result
    transform_name = result[0]
    print transform_name
    vertex_names = cmds.filterExpand(expand=True, selectionMask=31)
    print vertex_names
    instance_group_name = cmds.group(empty=True,
                                     name=transform_name + '_instance_grp#')

    for vertex in vertex_names:
        print vertex
        instance_result = cmds.instance(transform_name, name=transform_name + '_instance#')
        cmds.parent(instance_result, instance_group_name)
        position = cmds.pointPosition(vertex)
        print position
        cmds.move(position[0], position[1], position[2], instance_result)

        xRot = random.uniform(0, 360)
        yRot = random.uniform(0, 360)
        zRot = random.uniform(0, 360)
        cmds.rotate(xRot, yRot, zRot, instance_result)

        scalingFactor = random.uniform(0.3, 2)
        cmds.scale(scalingFactor, scalingFactor, scalingFactor, instance_result)

    cmds.hide(transform_name)
    cmds.xform(instance_group_name, centerPivots=True)
