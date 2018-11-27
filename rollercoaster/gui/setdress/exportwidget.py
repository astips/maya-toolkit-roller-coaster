# -*- coding: utf-8 -*-

import getpass
from QtSide import QtCore, QtGui, QtWidgets
from ..packages.utils import to_utf8
from ..packages.resource import Resource


class ExportOptionWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, _type=None, maya=None, preset=None):
        super(ExportOptionWidget, self).__init__(parent)

        self.travel_mode = None
        self.channelbox = False
        self.segment = False
        self.bake = False
        self.static = False

        self._parent = parent
        self._type = _type
        self.preset = preset
        self.maya = maya

        self.resource = Resource(None, self.preset.user['theme'])
        self.setup_ui()
        self.__connect()

    def setup_ui(self):
        self.setMinimumSize(QtCore.QSize(275, 0))
        self.vertical_layout_main = QtWidgets.QVBoxLayout(self)
        self.vertical_layout_main.setSpacing(4)
        self.vertical_layout_main.setContentsMargins(0, 0, 0, 2)

        self.horizontal_layout_title = QtWidgets.QHBoxLayout()
        self.button_type = QtWidgets.QPushButton(self)
        self.button_type.setFixedSize(36, 36)
        self.button_type.setIconSize(QtCore.QSize(36, 36))
        self.button_type.setFlat(True)
        self.horizontal_layout_title.addWidget(self.button_type)
        self.label_type = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)
        self.label_type.setFont(font)
        self.horizontal_layout_title.addWidget(self.label_type)
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout_title.addItem(spacer)
        self.vertical_layout_main.addLayout(self.horizontal_layout_title)
        self.line_main = QtWidgets.QFrame(self)
        self.line_main.setFrameShape(QtWidgets.QFrame.HLine)
        self.vertical_layout_main.addWidget(self.line_main)

        self.horizontal_layout_context = QtWidgets.QHBoxLayout()
        self.horizontal_layout_context.setContentsMargins(9, 0, 0, 0)
        self.label_context = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_context.setFont(font)
        self.label_context.setText('X-RIG Context')
        self.horizontal_layout_context.addWidget(self.label_context)
        self.combo_context = QtWidgets.QComboBox(self)
        self.combo_context.setMinimumSize(QtCore.QSize(75, 0))
        self.combo_context.setMaximumSize(QtCore.QSize(16777215, 25))
        self.combo_context.setFrame(False)
        self.horizontal_layout_context.addWidget(self.combo_context)
        self.vertical_layout_main.addLayout(self.horizontal_layout_context)
        self.line_xrig = QtWidgets.QFrame(self)
        self.line_xrig.setFrameShape(QtWidgets.QFrame.HLine)
        self.vertical_layout_main.addWidget(self.line_xrig)

        self.widget_info = QtWidgets.QWidget(self)
        self.vertical_layout_widget_info = QtWidgets.QVBoxLayout(self.widget_info)
        self.vertical_layout_widget_info.setContentsMargins(0, 0, 0, 0)
        self.form_layout_info = QtWidgets.QFormLayout()
        self.form_layout_info.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.form_layout_info.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.form_layout_info.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.form_layout_info.setContentsMargins(9, 6, -1, 4)
        self.form_layout_info.setHorizontalSpacing(25)
        self.form_layout_info.setVerticalSpacing(15)
        self.label_author = QtWidgets.QLabel(self.widget_info)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_author.setFont(font)
        self.label_author.setText('Author:')
        self.form_layout_info.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_author)
        self.label_author_value = QtWidgets.QLabel(self.widget_info)
        self.form_layout_info.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_author_value)
        self.label_frame = QtWidgets.QLabel(self.widget_info)
        self.label_frame.setFont(font)
        self.label_frame.setText('Frame Range:')
        self.form_layout_info.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_frame)
        self.label_frame_value = QtWidgets.QLabel(self.widget_info)
        self.form_layout_info.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_frame_value)
        self.label_namespace = QtWidgets.QLabel(self.widget_info)
        self.label_namespace.setFont(font)
        self.label_namespace.setText('Namespace:')
        self.form_layout_info.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_namespace)
        self.label_namespace_value = QtWidgets.QLabel(self.widget_info)
        self.form_layout_info.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_namespace_value)
        self.label_contains = QtWidgets.QLabel(self.widget_info)
        self.label_contains.setFont(font)
        self.label_contains.setText('Contains:')
        self.form_layout_info.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_contains)
        self.label_contains_value = QtWidgets.QLabel(self.widget_info)
        self.form_layout_info.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_contains_value)
        self.horizontal_layout_ctrl_tag = QtWidgets.QHBoxLayout()
        self.horizontal_layout_ctrl_tag.setSpacing(12)
        self.label_r_tag = QtWidgets.QLabel(self.widget_info)
        self.label_r_tag.setFont(font)
        self.label_r_tag.setText('R')
        self.label_r_tag.setStyleSheet("color: rgb(0, 50, 255);")
        self.horizontal_layout_ctrl_tag.addWidget(self.label_r_tag)
        self.label_m_tag = QtWidgets.QLabel(self.widget_info)
        self.label_m_tag.setFont(font)
        self.label_m_tag.setText('M')
        self.label_m_tag.setStyleSheet("color: rgb(150, 150, 0);")
        self.horizontal_layout_ctrl_tag.addWidget(self.label_m_tag)
        self.label_l_tag = QtWidgets.QLabel(self.widget_info)
        self.label_l_tag.setFont(font)
        self.label_l_tag.setText('L')
        self.label_l_tag.setStyleSheet("color: rgb(255, 0, 0);")
        self.horizontal_layout_ctrl_tag.addWidget(self.label_l_tag)
        self.form_layout_info.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.horizontal_layout_ctrl_tag)
        self.vertical_layout_widget_info.addLayout(self.form_layout_info)
        self.vertical_layout_main.addWidget(self.widget_info)

        self.widget_option = QtWidgets.QWidget(self)
        self.vertical_layout_group_option = QtWidgets.QVBoxLayout(self.widget_option)
        self.vertical_layout_group_option.setSpacing(6)
        self.vertical_layout_group_option.setContentsMargins(0, 0, 0, 0)

        self.group_travel = QtWidgets.QGroupBox(self.widget_option)
        self.group_travel.setTitle('')
        self.horizontal_layout_group_travel = QtWidgets.QHBoxLayout(self.group_travel)
        self.horizontal_layout_group_travel.setContentsMargins(-1, 12, -1, 12)
        self.radiobutton_selected = QtWidgets.QRadioButton(self.group_travel)
        self.radiobutton_selected.setMinimumSize(QtCore.QSize(110, 0))
        self.radiobutton_selected.setChecked(True)
        self.radiobutton_selected.setText('Selected')
        self.horizontal_layout_group_travel.addWidget(self.radiobutton_selected)
        self.radiobutton_recursive = QtWidgets.QRadioButton(self.group_travel)
        self.radiobutton_recursive.setText('Recursive')
        self.horizontal_layout_group_travel.addWidget(self.radiobutton_recursive)
        self.vertical_layout_group_option.addWidget(self.group_travel)

        self.group_frame = QtWidgets.QGroupBox(self.widget_option)
        self.group_frame.setTitle("")
        self.vertical_layout_group_frame = QtWidgets.QVBoxLayout(self.group_frame)
        self.vertical_layout_group_frame.setSpacing(12)
        self.vertical_layout_group_frame.setContentsMargins(-1, 12, -1, 12)
        self.horizontal_layout_time_a = QtWidgets.QHBoxLayout()
        self.radiobutton_all = QtWidgets.QRadioButton(self.group_frame)
        self.radiobutton_all.setMinimumSize(QtCore.QSize(110, 0))
        self.radiobutton_all.setChecked(True)
        self.radiobutton_all.setText('All Time')
        self.horizontal_layout_time_a.addWidget(self.radiobutton_all)
        self.radiobutton_slider = QtWidgets.QRadioButton(self.group_frame)
        self.radiobutton_slider.setText('Time Slider')
        self.horizontal_layout_time_a.addWidget(self.radiobutton_slider)
        self.vertical_layout_group_frame.addLayout(self.horizontal_layout_time_a)
        self.horizontal_layout_time_b = QtWidgets.QHBoxLayout()
        self.radiobutton_current = QtWidgets.QRadioButton(self.group_frame)
        self.radiobutton_current.setText('Current Frame')
        self.radiobutton_current.setMinimumSize(QtCore.QSize(110, 0))
        self.horizontal_layout_time_b.addWidget(self.radiobutton_current)
        self.vertical_layout_group_frame.addLayout(self.horizontal_layout_time_b)
        self.horizontal_layout_time_c = QtWidgets.QHBoxLayout()
        self.radiobutton_single = QtWidgets.QRadioButton(self.group_frame)
        self.radiobutton_single.setText('Single Frame')
        self.radiobutton_single.setMinimumSize(QtCore.QSize(110, 0))
        self.horizontal_layout_time_c.addWidget(self.radiobutton_single)
        self.radiobutton_range = QtWidgets.QRadioButton(self.group_frame)
        self.radiobutton_range.setText('Start / End')
        self.horizontal_layout_time_c.addWidget(self.radiobutton_range)
        self.vertical_layout_group_frame.addLayout(self.horizontal_layout_time_c)
        self.horizontal_layout_time_d = QtWidgets.QHBoxLayout()
        self.spinbox_start = QtWidgets.QSpinBox(self.group_frame)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.spinbox_start.sizePolicy().hasHeightForWidth())
        self.spinbox_start.setSizePolicy(size_policy)
        self.spinbox_start.setFocusPolicy(QtCore.Qt.TabFocus | QtCore.Qt.ClickFocus)
        self.spinbox_start.setFrame(True)
        self.spinbox_start.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinbox_start.setMinimum(-100000)
        self.spinbox_start.setMaximum(100000)
        self.spinbox_start.setEnabled(False)
        self.horizontal_layout_time_d.addWidget(self.spinbox_start)
        self.spinbox_end = QtWidgets.QSpinBox(self.group_frame)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.spinbox_end.sizePolicy().hasHeightForWidth())
        self.spinbox_end.setSizePolicy(size_policy)
        self.spinbox_end.setFocusPolicy(QtCore.Qt.TabFocus | QtCore.Qt.ClickFocus)
        self.spinbox_end.setFrame(True)
        self.spinbox_end.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinbox_end.setAccelerated(True)
        self.spinbox_end.setMinimum(-100000)
        self.spinbox_end.setMaximum(100000)
        self.spinbox_end.setEnabled(False)
        self.horizontal_layout_time_d.addWidget(self.spinbox_end)
        self.vertical_layout_group_frame.addLayout(self.horizontal_layout_time_d)
        self.vertical_layout_group_option.addWidget(self.group_frame)

        self.group_attr = QtWidgets.QGroupBox(self.widget_option)
        self.group_attr.setTitle("")
        self.horizontal_layout_group_attr = QtWidgets.QHBoxLayout(self.group_attr)
        self.horizontal_layout_group_attr.setSpacing(9)
        self.horizontal_layout_group_attr.setContentsMargins(-1, 12, -1, 12)
        self.radiobutton_keyable = QtWidgets.QRadioButton(self.group_attr)
        self.radiobutton_keyable.setText('All Keyable')
        self.radiobutton_keyable.setMinimumSize(QtCore.QSize(110, 0))
        self.radiobutton_keyable.setChecked(True)
        self.horizontal_layout_group_attr.addWidget(self.radiobutton_keyable)
        self.radiobutton_channelbox = QtWidgets.QRadioButton(self.group_attr)
        self.radiobutton_channelbox.setText('From Channel Box')
        self.horizontal_layout_group_attr.addWidget(self.radiobutton_channelbox)
        self.vertical_layout_group_option.addWidget(self.group_attr)

        self.group_include = QtWidgets.QGroupBox(self.widget_option)
        self.group_include.setTitle("")
        self.vertical_layout_group_include = QtWidgets.QVBoxLayout(self.group_include)
        self.vertical_layout_group_include.setSpacing(12)
        self.vertical_layout_group_include.setContentsMargins(-1, 12, -1, 12)
        self.check_static = QtWidgets.QCheckBox(self.group_include)
        self.check_static.setText('Static Values')
        self.check_static.setChecked(True)
        self.vertical_layout_group_include.addWidget(self.check_static)
        self.check_bake_constraint = QtWidgets.QCheckBox(self.group_include)
        self.check_bake_constraint.setText('Bake Constraints')
        self.vertical_layout_group_include.addWidget(self.check_bake_constraint)
        self.vertical_layout_group_option.addWidget(self.group_include)

        self.group_border = QtWidgets.QGroupBox(self.widget_option)
        self.group_border.setTitle("")
        self.horizontal_layout_group_border = QtWidgets.QHBoxLayout(self.group_border)
        self.horizontal_layout_group_border.setContentsMargins(-1, 12, -1, 12)
        self.radiobutton_segment = QtWidgets.QRadioButton(self.group_border)
        self.radiobutton_segment.setMinimumSize(QtCore.QSize(110, 0))
        self.radiobutton_segment.setText('Segment')
        self.radiobutton_segment.setEnabled(False)
        self.horizontal_layout_group_border.addWidget(self.radiobutton_segment)
        self.radiobutton_keys = QtWidgets.QRadioButton(self.group_border)
        self.radiobutton_keys.setText('Keys')
        self.radiobutton_keys.setChecked(True)
        self.horizontal_layout_group_border.addWidget(self.radiobutton_keys)
        self.vertical_layout_group_option.addWidget(self.group_border)

        self.vertical_layout_group_option.setStretch(0, 1)
        self.vertical_layout_group_option.setStretch(1, 3)
        self.vertical_layout_group_option.setStretch(2, 1)
        self.vertical_layout_group_option.setStretch(3, 2)
        self.vertical_layout_group_option.setStretch(4, 1)
        self.vertical_layout_main.addWidget(self.widget_option)

        self.horizontal_layout_comment = QtWidgets.QHBoxLayout()
        self.edit_comment = QtWidgets.QTextEdit(self)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.edit_comment.sizePolicy().hasHeightForWidth())
        self.edit_comment.setSizePolicy(size_policy)
        self.edit_comment.setFocusPolicy(QtCore.Qt.TabFocus | QtCore.Qt.ClickFocus)
        self.edit_comment.setMinimumSize(QtCore.QSize(0, 50))
        self.edit_comment.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.horizontal_layout_comment.addWidget(self.edit_comment)
        self.button_create_data = QtWidgets.QPushButton(self)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.button_create_data.sizePolicy().hasHeightForWidth())
        self.button_create_data.setSizePolicy(size_policy)
        self.button_create_data.setStyleSheet("background-color: rgb(255, 0, 0, 20);")
        self.button_create_data.setIconSize(QtCore.QSize(32, 32))
        self.button_create_data.setIcon(self.resource.icon('icon_get'))
        self.button_create_data.linkColor = 'red'
        self.horizontal_layout_comment.addWidget(self.button_create_data)
        self.horizontal_layout_comment.setStretch(0, 1)
        self.vertical_layout_main.addLayout(self.horizontal_layout_comment)

        if self._type == 'pose':
            self.button_type.setIcon(self.resource.icon('icon_pose'))
            self.label_type.setText('Pose')
            self.init_pose_options()
            self.set_start_end_when_all()
            self.update_ctrl()
        else:
            self.button_type.setIcon(self.resource.icon('icon_clip'))
            self.label_type.setText('Motion Clip')
            self.radiobutton_current.hide()
            self.widget_info.hide()

        self.label_author_value.setText(getpass.getuser())

    def __connect(self):
        self.radiobutton_recursive.toggled.connect(self.update_ctrl)
        self.radiobutton_recursive.toggled.connect(self.radiobutton_recursive_event)
        self.radiobutton_all.toggled.connect(self.set_start_end_when_all)
        self.radiobutton_all.toggled.connect(self.radiobutton_all_event)
        self.radiobutton_current.toggled.connect(self.radiobutton_current_event)
        self.radiobutton_single.toggled.connect(self.radiobutton_single_event)
        self.spinbox_start.valueChanged.connect(self.check_end_frame)
        self.radiobutton_range.toggled.connect(self.radiobutton_range_event)
        self.radiobutton_range.toggled.connect(self.check_end_frame)

    def radiobutton_recursive_event(self):
        self.check_static.setChecked(False)
        self.check_static.setEnabled(1 - self.radiobutton_recursive.isChecked())

    def radiobutton_all_event(self):
        self.radiobutton_keys.setChecked(self.radiobutton_all.isChecked())
        self.radiobutton_segment.setEnabled(1-self.radiobutton_all.isChecked())

    def radiobutton_current_event(self):
        self.radiobutton_segment.setEnabled(True)
        self.radiobutton_segment.setChecked(True)
        self.radiobutton_keys.setEnabled(False)

    def radiobutton_single_event(self):
        self.spinbox_start.setEnabled(self.radiobutton_single.isChecked())
        self.spinbox_end.setEnabled(False)
        self.radiobutton_segment.setEnabled(True)
        self.radiobutton_segment.setChecked(True)
        self.radiobutton_keys.setEnabled(False)

    def radiobutton_range_event(self):
        self.spinbox_start.setEnabled(self.radiobutton_range.isChecked())
        self.spinbox_end.setEnabled(self.radiobutton_range.isChecked())

    def check_end_frame(self):
        if not self.radiobutton_range.isChecked():
            return
        start_frame = self.spinbox_start.value()
        end_frame = self.spinbox_end.value()
        if end_frame < start_frame:
            self.spinbox_end.setValue(start_frame)

    def update_ctrl(self):
        # print 'update_ctrl'
        self.check_static.setChecked(False)
        self.check_static.setEnabled(1-self.radiobutton_recursive.isChecked())

        self.get_options()
        nodes = self.maya.engine._travel(mode=self.travel_mode, context=self.preset.user['context']) or []
        self.label_contains_value.setText(str(len(nodes)))
        lmr = self.maya.engine.ctrl_counter(nodes, context=self.preset.user['context'])
        if lmr[0]:
            self.label_l_tag.show()
        else:
            self.label_l_tag.hide()
        if lmr[1]:
            self.label_m_tag.show()
        else:
            self.label_m_tag.hide()
        if lmr[2]:
            self.label_r_tag.show()
        else:
            self.label_r_tag.hide()
        ns_str = ''
        namespaces = self.maya.engine._namespaces(nodes)
        if namespaces is None or not len(namespaces):
            self.label_namespace_value.setText('')
            return
        if len(namespaces) > 1:
            self.label_namespace_value.setStyleSheet("color: rgb(255, 0, 0, 255)")
        else:
            self.label_namespace_value.setStyleSheet("color: rgb(200, 200, 200, 255)")
        ns_str += '     '.join(namespaces)
        self.label_namespace_value.setText(ns_str)

    def update_current_frame(self):
        self.label_frame_value.setText(str(self.maya.frame.current()))

    def set_start_end_when_all(self):
        if not self.radiobutton_all.isChecked():
            return
        nodes = self.maya.engine._travel(
            mode='SELECTED' if self.radiobutton_selected.isChecked() else 'RECURSIVE',
            context=self.preset.user['context']
        )
        if nodes is None:
            st, et = self.maya.frame.slider
        else:
            st, et = self.maya.engine.get_frame_range_from_nodes(nodes)
        self.spinbox_start.setValue(st)
        self.spinbox_end.setValue(et)

    def get_frame_range(self):
        if self.radiobutton_all.isChecked():
            self.set_start_end_when_all()
            frame_range = (
                float(self.spinbox_start.value()), float(self.spinbox_end.value())
            )
        elif self.radiobutton_slider.isChecked():
            frame_range = self.maya.frame.slider
        elif self.radiobutton_single.isChecked():
            single_frame = self.spinbox_start.value()
            frame_range = (float(single_frame), float(single_frame))
        elif self.radiobutton_range.isChecked():
            frame_range = (
                float(self.spinbox_start.value()), float(self.spinbox_end.value())
            )
        else:
            current_frame = self.maya.frame.current()
            frame_range = (current_frame, current_frame)
        return frame_range

    def get_comment(self):
        return to_utf8(self.edit_comment.toPlainText())

    def get_options(self):
        if self.radiobutton_selected.isChecked():
            self.travel_mode = 'SELECTED'
        else:
            self.travel_mode = 'RECURSIVE'
        self.channelbox = self.radiobutton_channelbox.isChecked()
        self.bake = self.check_bake_constraint.isChecked()
        self.static = self.check_static.isChecked()
        self.segment = self.radiobutton_segment.isChecked()

    def init_pose_options(self):
        self.radiobutton_selected.setChecked(True)
        self.radiobutton_current.setChecked(True)
        self.radiobutton_segment.setChecked(True)

        self.group_frame.hide()
        self.group_border.hide()
        self.group_include.hide()
