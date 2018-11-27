# -*- coding: utf-8 -*-

import os
import math
from functools import partial
from QtSide import QtCore, QtGui, QtWidgets
from ..packages.resource import Resource
from ..packages.widgets.labels import ImageSequenceLabel
from ..packages.utils import natural_sort, to_utf8


class LoadWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, machine=None, maya=None, preset=None):
        super(LoadWidget, self).__init__(parent)

        self._parent = parent
        self.machine = machine
        self.undo = maya.undo
        self.preset = preset

        self.animation = None
        self.resource = Resource(None, self.preset.user['theme'])
        self.on_play = False
        self.info = None
        self.item = None

        # options
        self.travel_mode = None
        self.apply_mode = None
        self._scale = 1.0
        self._frames = None

        self.setup_ui()
        self.__connect()

    def setup_ui(self):
        self.setMinimumSize(QtCore.QSize(200, 0))
        self.setMaximumSize(QtCore.QSize(500, 16777215))
        self.vertical_layout_main = QtWidgets.QVBoxLayout(self)
        self.vertical_layout_main.setSpacing(6)
        self.vertical_layout_main.setContentsMargins(2, 4, 6, 4)

        self.horizontal_layout_type = QtWidgets.QHBoxLayout()
        self.button_type = QtWidgets.QPushButton(self)
        self.button_type.setMinimumSize(QtCore.QSize(25, 25))
        self.button_type.setMaximumSize(QtCore.QSize(25, 25))
        self.button_type.setIconSize(QtCore.QSize(25, 25))
        self.button_type.setFlat(True)
        self.horizontal_layout_type.addWidget(self.button_type)
        self.label_type = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_type.setFont(font)
        self.horizontal_layout_type.addWidget(self.label_type)
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout_type.addItem(spacer)
        self.vertical_layout_main.addLayout(self.horizontal_layout_type)

        self.frame_preview = QtWidgets.QFrame(self)
        self.frame_preview.setBaseSize(QtCore.QSize(200, 80))
        self.frame_preview.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_preview.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_preview.setFixedHeight(self.frame_preview.width() * 4 / 5)
        self.frame_preview.setStyleSheet("background-color: rgb(10, 10, 10, 75)")
        self.vertical_layout_frame_preview = QtWidgets.QVBoxLayout(self.frame_preview)
        self.vertical_layout_frame_preview.setContentsMargins(4, 4, 4, 4)
        self.label_sequence = ImageSequenceLabel(
            self.frame_preview, fps=self.preset.user['editor']['fps'], timer=self.preset.user['editor']['interval']
        )
        self.vertical_layout_frame_preview.addWidget(self.label_sequence)
        self.button_play = QtWidgets.QPushButton(self.frame_preview)
        self.button_play.setIconSize(QtCore.QSize(32, 32))
        self.button_play.setIcon(self.resource.icon('icon_playitem'))
        self.button_play.setFlat(True)
        self.button_play.setMouseTracking(False)
        self.button_play.setStyleSheet("border-radius: 15px;background-color: rgb(10, 10, 10, 0)")

        self.button_switch = QtWidgets.QPushButton(self.frame_preview)
        self.button_switch.setIconSize(QtCore.QSize(30, 30))
        self.button_switch.setIcon(self.resource.icon('icon_arrow_right_item'))
        self.button_switch.setFlat(True)
        self.button_switch.setMouseTracking(False)
        self.button_switch.setStyleSheet("border-radius: 15px;background-color: rgb(10, 10, 10, 0)")
        self.vertical_layout_main.addWidget(self.frame_preview)

        self.form_layout_info = QtWidgets.QFormLayout()
        self.form_layout_info.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.form_layout_info.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.form_layout_info.setContentsMargins(8, 2, 4, 2)
        self.form_layout_info.setHorizontalSpacing(9)
        self.form_layout_info.setVerticalSpacing(8)
        self.label_author = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_author.setFont(font)
        self.label_author.setText('Author:')
        self.form_layout_info.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_author)
        self.label_author_value = QtWidgets.QLabel(self)
        self.form_layout_info.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_author_value)
        self.label_date = QtWidgets.QLabel(self)
        self.label_date.setFont(font)
        self.label_date.setText('Created Date:')
        self.form_layout_info.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_date)
        self.label_date_value = QtWidgets.QLabel(self)
        self.form_layout_info.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_date_value)
        self.label_namespace = QtWidgets.QLabel(self)
        self.label_namespace.setFont(font)
        self.label_namespace.setText('Namespace:')
        self.form_layout_info.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_namespace)
        self.label_namespace_value = QtWidgets.QLabel(self)
        self.form_layout_info.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_namespace_value)
        self.label_range = QtWidgets.QLabel(self)
        self.label_range.setFont(font)
        self.label_range.setText('Frame Range:')
        self.form_layout_info.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_range)
        self.label_range_value = QtWidgets.QLabel(self)
        self.form_layout_info.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_range_value)
        self.label_contains = QtWidgets.QLabel(self)
        self.label_contains.setFont(font)
        self.label_contains.setText('Contains:')
        self.form_layout_info.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_contains)
        self.label_contains_value = QtWidgets.QLabel(self)
        self.form_layout_info.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_contains_value)
        self.label_comment = QtWidgets.QLabel(self)
        self.label_comment.setFont(font)
        self.label_comment.setText('Comment:')
        self.form_layout_info.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_comment)
        self.label_comment_value = QtWidgets.QLabel(self)
        self.form_layout_info.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.label_comment_value)
        self.vertical_layout_main.addLayout(self.form_layout_info)

        self.widget_clip = QtWidgets.QGroupBox(self)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setPointSize(11)
        font.setBold(True)
        self.widget_clip.setFont(font)
        self.widget_clip.setTitle('Motion Clip Options')
        self.vertical_layout_widget_clip = QtWidgets.QVBoxLayout(self.widget_clip)
        self.vertical_layout_widget_clip.setSpacing(6)
        self.vertical_layout_widget_clip.setContentsMargins(4, 12, 4, 4)
        self.horizontal_layout_controls = QtWidgets.QHBoxLayout()
        self.label_controls = QtWidgets.QLabel(self.widget_clip)
        self.label_controls.setText('Controls')
        self.horizontal_layout_controls.addWidget(self.label_controls)
        self.vertical_layout_widget_clip.addLayout(self.horizontal_layout_controls)
        self.widget_apply_to = QtWidgets.QWidget(self.widget_clip)
        self.horizontal_layout_apply_to = QtWidgets.QHBoxLayout(self.widget_apply_to)
        self.horizontal_layout_apply_to.setContentsMargins(20, 0, 0, 0)
        self.radiobutton_selected = QtWidgets.QRadioButton(self.widget_apply_to)
        self.radiobutton_selected.setChecked(True)
        self.radiobutton_selected.setText('Selected')
        self.horizontal_layout_apply_to.addWidget(self.radiobutton_selected)
        self.radiobutton_recursive = QtWidgets.QRadioButton(self.widget_apply_to)
        self.radiobutton_recursive.setText('Recursive')
        self.horizontal_layout_apply_to.addWidget(self.radiobutton_recursive)
        self.vertical_layout_widget_clip.addWidget(self.widget_apply_to)

        self.horizontal_layout_frames = QtWidgets.QHBoxLayout()
        self.label_frames = QtWidgets.QLabel(self.widget_clip)
        self.label_frames.setText('Frames')
        self.horizontal_layout_frames.addWidget(self.label_frames)
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout_frames.addItem(spacer)
        self.vertical_layout_widget_clip.addLayout(self.horizontal_layout_frames)
        self.widget_frames = QtWidgets.QWidget(self.widget_clip)
        self.vertical_layout_widget_frames = QtWidgets.QVBoxLayout(self.widget_frames)
        self.vertical_layout_widget_frames.setContentsMargins(20, 0, 0, 0)
        self.horizontal_layout_frames_a = QtWidgets.QHBoxLayout()
        self.radiobutton_from_data_frame = QtWidgets.QRadioButton(self.widget_frames)
        self.radiobutton_from_data_frame.setChecked(True)
        self.radiobutton_from_data_frame.setText('From Data')
        self.horizontal_layout_frames_a.addWidget(self.radiobutton_from_data_frame)
        self.radiobutton_current_frame = QtWidgets.QRadioButton(self.widget_frames)
        self.radiobutton_current_frame.setText('Current Frame')
        self.horizontal_layout_frames_a.addWidget(self.radiobutton_current_frame)
        self.vertical_layout_widget_frames.addLayout(self.horizontal_layout_frames_a)
        self.horizontal_layout_frames_b = QtWidgets.QHBoxLayout()
        self.radiobutton_start_end = QtWidgets.QRadioButton(self.widget_frames)
        self.radiobutton_start_end.setText('Start / End')
        self.horizontal_layout_frames_b.addWidget(self.radiobutton_start_end)
        self.spinbox_start = QtWidgets.QSpinBox(self.widget_frames)
        self.spinbox_start.setEnabled(False)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.spinbox_start.sizePolicy().hasHeightForWidth())
        self.spinbox_start.setSizePolicy(size_policy)
        self.spinbox_start.setFrame(False)
        self.spinbox_start.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinbox_start.setKeyboardTracking(False)
        self.spinbox_start.setMinimum(-10000)
        self.spinbox_start.setMaximum(10000)
        self.horizontal_layout_frames_b.addWidget(self.spinbox_start)
        self.spinbox_end = QtWidgets.QSpinBox(self.widget_frames)
        self.spinbox_end.setEnabled(False)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.spinbox_end.sizePolicy().hasHeightForWidth())
        self.spinbox_end.setSizePolicy(size_policy)
        self.spinbox_end.setFrame(False)
        self.spinbox_end.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinbox_end.setKeyboardTracking(False)
        self.spinbox_end.setMinimum(-10000)
        self.spinbox_end.setMaximum(10000)
        self.horizontal_layout_frames_b.addWidget(self.spinbox_end)
        self.vertical_layout_widget_frames.addLayout(self.horizontal_layout_frames_b)
        self.vertical_layout_widget_clip.addWidget(self.widget_frames)

        self.horizontal_layout_mode = QtWidgets.QHBoxLayout()
        self.label_mode = QtWidgets.QLabel(self.widget_clip)
        self.label_mode.setText('Mode')
        self.horizontal_layout_mode.addWidget(self.label_mode)
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout_mode.addItem(spacer)
        self.vertical_layout_widget_clip.addLayout(self.horizontal_layout_mode)
        self.widget_mode = QtWidgets.QWidget(self.widget_clip)
        self.vertical_layout_widget_mode = QtWidgets.QVBoxLayout(self.widget_mode)
        self.vertical_layout_widget_mode.setContentsMargins(20, 0, 0, 0)
        self.vertical_layout_widget_mode.setSpacing(9)
        self.horizontal_layout_mode_a = QtWidgets.QHBoxLayout()
        self.horizontal_layout_mode_a.setSpacing(5)
        self.radiobutton_replace_all = QtWidgets.QRadioButton(self.widget_mode)
        self.radiobutton_replace_all.setText('Replace All')
        self.radiobutton_replace_all.setChecked(True)
        self.horizontal_layout_mode_a.addWidget(self.radiobutton_replace_all)
        self.radiobutton_insert = QtWidgets.QRadioButton(self.widget_mode)
        self.radiobutton_insert.setText('Insert')
        self.horizontal_layout_mode_a.addWidget(self.radiobutton_insert)
        self.vertical_layout_widget_mode.addLayout(self.horizontal_layout_mode_a)
        self.horizontal_layout_mode_b = QtWidgets.QHBoxLayout()
        self.horizontal_layout_mode_b.setSpacing(5)
        self.radiobutton_replace_range = QtWidgets.QRadioButton(self.widget_mode)
        self.radiobutton_replace_range.setText('Replace Range')
        self.horizontal_layout_mode_b.addWidget(self.radiobutton_replace_range)
        self.radiobutton_merge = QtWidgets.QRadioButton(self.widget_mode)
        self.radiobutton_merge.setText('Merge')
        self.horizontal_layout_mode_b.addWidget(self.radiobutton_merge)
        self.vertical_layout_widget_mode.addLayout(self.horizontal_layout_mode_b)
        self.vertical_layout_widget_clip.addWidget(self.widget_mode)

        self.horizontal_layout_scale = QtWidgets.QHBoxLayout()
        self.horizontal_layout_scale.setContentsMargins(0, -1, -1, -1)
        self.checkbox_scale = QtWidgets.QCheckBox(self.widget_clip)
        self.checkbox_scale.setText('Scale')
        self.checkbox_scale.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.horizontal_layout_scale.addWidget(self.checkbox_scale)
        self.spinbox_scale = QtWidgets.QDoubleSpinBox(self.widget_clip)
        self.spinbox_scale.setEnabled(False)
        self.spinbox_scale.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.spinbox_scale.setFrame(False)
        self.spinbox_scale.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinbox_scale.setMinimum(0.01)
        self.spinbox_scale.setMaximum(10.0)
        self.spinbox_scale.setSingleStep(0.1)
        self.spinbox_scale.setProperty("value", 1.0)
        self.horizontal_layout_scale.addWidget(self.spinbox_scale)
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout_scale.addItem(spacer)
        self.vertical_layout_widget_clip.addLayout(self.horizontal_layout_scale)

        self.horizontal_layout_help_image = QtWidgets.QHBoxLayout()
        self.checkbox_help_image = QtWidgets.QCheckBox(self.widget_clip)
        self.checkbox_help_image.setText('Help Image')
        self.checkbox_help_image.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.horizontal_layout_help_image.addWidget(self.checkbox_help_image)
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout_help_image.addItem(spacer)
        self.vertical_layout_widget_clip.addLayout(self.horizontal_layout_help_image)
        self.vertical_layout_widget_help_image = QtWidgets.QVBoxLayout()
        self.vertical_layout_widget_help_image.setContentsMargins(20, 0, 0, 0)
        self.label_help_image = QtWidgets.QLabel(self)
        self.label_help_image.setPixmap(self.resource.pixmap('replaceCompletely'))
        self.label_help_image.setFixedHeight(0)
        self.vertical_layout_widget_help_image.addWidget(self.label_help_image)
        self.vertical_layout_widget_clip.addLayout(self.vertical_layout_widget_help_image)

        self.vertical_layout_main.addWidget(self.widget_clip)

        self.widget_pose = QtWidgets.QGroupBox(self)
        self.widget_pose.setFont(font)
        self.widget_pose.setTitle('Pose Options')
        self.vertical_layout_widget_pose = QtWidgets.QVBoxLayout(self.widget_pose)
        self.vertical_layout_widget_pose.setSpacing(6)
        self.vertical_layout_widget_pose.setContentsMargins(4, 12, 4, 4)

        self.horizontal_layout_blend_title = QtWidgets.QHBoxLayout()
        self.label_blend = QtWidgets.QLabel(self.widget_pose)
        self.label_blend.setText('Blend')
        self.horizontal_layout_blend_title.addWidget(self.label_blend)
        self.vertical_layout_widget_pose.addLayout(self.horizontal_layout_blend_title)

        self.horizontal_layout_blend = QtWidgets.QHBoxLayout()
        self.horizontal_layout_blend.setContentsMargins(20, 0, 0, 0)
        self.slider_blend = QtWidgets.QSlider(self.widget_pose)
        self.slider_blend.setMaximum(100)
        self.slider_blend.setProperty("value", 100)
        self.slider_blend.setOrientation(QtCore.Qt.Horizontal)
        self.slider_blend.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider_blend.setTickInterval(10)
        self.horizontal_layout_blend.addWidget(self.slider_blend)
        self.spinbox_blend = QtWidgets.QSpinBox(self.widget_pose)
        self.spinbox_blend.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.spinbox_blend.setFrame(False)
        self.spinbox_blend.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinbox_blend.setMaximum(100)
        self.spinbox_blend.setProperty("value", 100)
        self.horizontal_layout_blend.addWidget(self.spinbox_blend)
        self.vertical_layout_widget_pose.addLayout(self.horizontal_layout_blend)

        self.vertical_layout_main.addWidget(self.widget_pose)

        self.horizontal_layout_buttons = QtWidgets.QHBoxLayout()
        self.button_apply = QtWidgets.QPushButton(self)
        self.button_apply.setFont(font)
        self.button_apply.setText('Apply')
        self.button_apply.setAutoDefault(False)
        self.button_apply.setIcon(self.resource.icon('icon_paint'))
        self.button_apply.setStyleSheet("background-color: rgb(10, 10, 10, 75)")
        self.horizontal_layout_buttons.addWidget(self.button_apply)
        self.button_edit = QtWidgets.QPushButton(self)
        self.button_edit.setFont(font)
        self.button_edit.setText('Edit')
        self.button_edit.setAutoDefault(False)
        self.button_edit.setIcon(self.resource.icon('icon_edit'))
        self.button_edit.setStyleSheet("background-color: rgb(10, 10, 10, 75)")
        self.horizontal_layout_buttons.addWidget(self.button_edit)
        self.button_edit.hide()
        self.vertical_layout_main.addLayout(self.horizontal_layout_buttons)
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vertical_layout_main.addItem(spacer)
        self.hide()

    def __connect(self):
        self.frame_preview.resizeEvent = self.preview_resize_event
        self.label_sequence.enterEvent = self.seq_enter_event
        self.spinbox_start.wheelEvent = self.ignore_wheel_event
        self.spinbox_end.wheelEvent = self.ignore_wheel_event
        self.spinbox_scale.wheelEvent = self.ignore_wheel_event
        self.button_play.clicked.connect(self.play)
        self.button_switch.clicked.connect(self.switch_snapshots)
        self.checkbox_scale.clicked.connect(self.set_scale)
        self.checkbox_help_image.toggled.connect(self.toggle_help_image)
        self.radiobutton_replace_all.toggled.connect(self.switch_help_image)
        self.radiobutton_replace_range.toggled.connect(self.switch_help_image)
        self.radiobutton_insert.toggled.connect(self.switch_help_image)
        self.radiobutton_merge.toggled.connect(self.switch_help_image)
        self.slider_blend.valueChanged.connect(self.spinbox_blend.setValue)
        self.spinbox_blend.valueChanged.connect(self.slider_blend.setValue)
        self.radiobutton_start_end.toggled.connect(self.toggle_start_end_eidt)
        self.radiobutton_start_end.toggled.connect(self.check_end_frame)
        self.spinbox_start.valueChanged.connect(self.check_end_frame)
        self.spinbox_end.valueChanged.connect(self.check_end_frame)
        self.radiobutton_current_frame.toggled.connect(self.toggle_current_frame)
        self.button_apply.clicked.connect(self.apply)
        self.button_edit.clicked.connect(self.edit)

    def build(self, item):
        self.item = item
        if item.linkType == 'pose':
            self.button_type.setIcon(self.resource.icon('icon_pose'))
            self.label_type.setText('Pose')
            self.button_play.hide()
            self.widget_pose.show()
            self.widget_clip.hide()
        else:
            self.button_type.setIcon(self.resource.icon('icon_clip'))
            self.label_type.setText('Motion Clip')
            self.on_play = False
            self.label_sequence._image_sequence.pause()
            self.button_play.setIcon(self.resource.icon('icon_playitem'))
            self.button_play.show()
            self.widget_pose.hide()
            self.widget_clip.show()
        self.label_sequence.linkCurrentSnapshot = self.item.linkCurrentSnapshot
        self.label_sequence._stop()
        self.label_sequence.set_dir(item.linkWidget.image_dir)
        if item.linkWidget.image_dir is None or not os.path.exists(item.linkWidget.image_dir):
            self.label_sequence.setPixmap(self.resource.pixmap(self.preset.tool['template']['image']))
        self.fill_info()

    def fill_info(self):
        data_file = os.path.join(self.item.linkPath, self.preset.tool['const']['datafile'])
        if not os.path.exists(data_file):
            self._parent.listwidget.warning('Data file lost !')
            self.hide()
            return
        self.info = self.machine.parse(data_file, info=True)
        self.label_author_value.setText(self.info['artist'])
        self.label_date_value.setText(self.info['date'])
        self.label_namespace_value.setText(self.info['namespace'] if len(self.info['namespace']) else 'None')
        self.label_range_value.setText(' - '.join([str(e) for e in self.info['frames']]))
        self.label_contains_value.setText(str(self.info['count']))
        self.label_comment_value.setText(self.info['comment'])
        self.label_comment_value.setToolTip(self.info['comment'])

    def switch_snapshots(self):
        if not self.item.linkSnapshots:
            return
        self.label_sequence.linkCurrentSnapshot += 1
        current = int(math.fmod(self.label_sequence.linkCurrentSnapshot, len(self.item.linkSnapshots)))
        image_dir = os.path.join(
            self.item.linkPath, self.preset.tool['const']['snapshot'], self.item.linkSnapshots[current]
        )
        images = [image for image in os.listdir(image_dir) if image.endswith(self.preset.tool['const']['compress'])]
        if len(images):
            natural_sort(images)
            pixmap_image = QtGui.QPixmap(os.path.join(image_dir, images[0]))
        else:
            pixmap_image = self.resource.pixmap(self.preset.tool['template']['image'])
        self.label_sequence.setPixmap(pixmap_image)
        self.label_sequence.set_dir(image_dir)
        self.label_sequence.set_current_frame(0)

    def set_scale(self):
        self.spinbox_scale.setEnabled(self.checkbox_scale.isChecked())
        if not self.checkbox_scale.isChecked():
            self.spinbox_scale.setValue(1.0)

    def get_scale(self):
        self._scale = float(self.spinbox_scale.text())

    def get_blend_percent(self):
        return self.spinbox_blend.value()

    def toggle_start_end_eidt(self):
        if self.radiobutton_replace_all.isChecked():
            self.radiobutton_replace_range.setChecked(True)
        self.radiobutton_replace_all.setEnabled(1 - self.radiobutton_start_end.isChecked())
        self.spinbox_start.setEnabled(self.radiobutton_start_end.isChecked())
        self.spinbox_end.setEnabled(self.radiobutton_start_end.isChecked())

    def check_end_frame(self):
        if self.radiobutton_start_end.isChecked():
            sf = self.spinbox_start.value()
            ef = self.spinbox_end.value()
            if ef < sf:
                self.spinbox_end.setValue(sf)

    def toggle_current_frame(self):
        self.radiobutton_replace_range.setEnabled(1 - self.radiobutton_current_frame.isChecked())
        self.radiobutton_replace_all.setEnabled(1 - self.radiobutton_current_frame.isChecked())
        if self.radiobutton_replace_range.isChecked() or self.radiobutton_replace_all.isChecked():
            self.radiobutton_insert.setChecked(True)

    def switch_help_image(self):
        if self.radiobutton_replace_all.isChecked():
            self.label_help_image.setPixmap(self.resource.pixmap('replaceCompletely'))
        if self.radiobutton_replace_range.isChecked():
            self.label_help_image.setPixmap(self.resource.pixmap('replace'))
        if self.radiobutton_insert.isChecked():
            self.label_help_image.setPixmap(self.resource.pixmap('insert'))
        if self.radiobutton_merge.isChecked():
            self.label_help_image.setPixmap(self.resource.pixmap('merge'))

    def toggle_help_image(self):
        # def set_help_image_height(height):
        #     self.label_help_image.setFixedHeight(height)
        x, y, _, _ = self.label_help_image.geometry().getCoords()
        self.animation = QtCore.QPropertyAnimation(self.label_help_image, 'maximumHeight')
        self.animation.setDuration(150)
        if self.checkbox_help_image.isChecked():
            self.animation.setStartValue(0)
            self.animation.setEndValue(150)
        else:
            self.animation.setStartValue(self.label_help_image.height())
            self.animation.setEndValue(0)
        # self.animation.valueChanged.connect(set_help_image_height)
        self.animation.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def preview_resize_event(self, event):
        event.accept()
        self.frame_preview.setFixedHeight(self.frame_preview.width() * 4 / 5)
        self.button_play.setGeometry(
            self.frame_preview.width() - 38, self.frame_preview.height() - 40, 32, 32
        )
        self.button_switch.setGeometry(self.frame_preview.width() - 30, 6, 28, 28)

    def seq_enter_event(self, event):
        event.ignore()

    def ignore_wheel_event(self, event):
        event.ignore()

    def play(self):
        self.label_sequence._image_sequence.switch()
        self.on_play = bool(1 - self.on_play)
        if self.on_play:
            self.button_play.setIcon(self.resource.icon('icon_pauseitem'))
        else:
            self.button_play.setIcon(self.resource.icon('icon_playitem'))

    def get_clip_modes(self):
        if self.radiobutton_selected.isChecked():
            self.travel_mode = 'SELECTED'
        else:
            self.travel_mode = 'RECURSIVE'

        if self.radiobutton_replace_all.isChecked():
            self.apply_mode = 'replace-entire'
        elif self.radiobutton_replace_range.isChecked():
            self.apply_mode = 'replace-range'
        elif self.radiobutton_insert.isChecked():
            self.apply_mode = 'insert'
        elif self.radiobutton_merge.isChecked():
            self.apply_mode = 'merge'
        else:
            pass

    def get_frames(self):
        if self.radiobutton_from_data_frame.isChecked():
            frame_range = self.info['frames']
        elif self.radiobutton_current_frame.isChecked():
            _offset = self.maya.frame().current() - self.machine.frames[0]
            frame_range = [self.maya.frame().current(), self.machine.frames[1] + _offset]
        elif self.radiobutton_start_end.isChecked():
            # self.spinbox_start.setValue(int(self.spinbox_start.text()))
            frame_range = [int(self.spinbox_start.text()), int(self.spinbox_end.text())]
        else:
            frame_range = None
        return frame_range

    def apply_pose(self):
        pose_options = self._parent._options
        self.machine._calculate(
            method=pose_options[0], channelBox=pose_options[2], namespace=None, mode=pose_options[1][0],
            modify=pose_options[1][1], file=os.path.join(self._item.linkPath, self.preset.tool['const']['datafile'])
        )
        self.machine.blending(percent=self.get_blend_percent())

    def apply_clip(self):
        self.get_clip_modes()
        self.get_frames()
        self.machine.animate(
            frameRange=self._get_frames(), method=self._method, mode=self._mode,
            namespace=None, channelBox=False, scale=self._scale,
            file=os.path.join(self._item.linkPath, self.preset.tool['const']['datafile'])
        )

    def apply(self):
        if self.item.linkType == 'pose':
            self.undo.open_chunk()
            try:
                self.apply_pose()
            except Exception as e:
                self._parent.listwidget.warning(e)
            finally:
                self.undo.close_chunk()
        else:
            self.apply_clip()

    def edit(self):
        def do_edit():
            comment = to_utf8(text_edit.text())
            datafile = os.path.join(self.item.linkPath, self.preset.tool['const']['datafile'])
            title = self.machine.parse(file=file, title=True)
            data = self.machine.parse(file=file, title=False)
            self.machine.write(datafile, comment=comment, data=data, namespace=title['namespace'])
            edit_dialog.close()

        edit_dialog = QtWidgets.QDialog(self)
        edit_dialog.setWindowTitle('Edit Comment.')
        layout_main = QtWidgets.QVBoxLayout(edit_dialog)
        layout_main.setContentsMargins(4, 4, 4, 4)
        layout_main.setSpacing(4)

        label = QtWidgets.QLabel(edit_dialog)
        label.setText('Can only edit the data comment for now.')

        text_edit = QtWidgets.QTextEdit(edit_dialog)
        text_edit.setFrameShape(QtWidgets.QFrame.NoFrame)

        button_cancel = QtWidgets.QPushButton(edit_dialog)
        button_cancel.setText('Cancel')
        button_ok = QtWidgets.QPushButton(edit_dialog)
        button_ok.setText('Ok')

        layout_buttons = QtWidgets.QHBoxLayout(edit_dialog)
        layout_buttons.addWidget(button_cancel)
        layout_buttons.addWidget(button_ok)

        layout_main.addWidget(label)
        layout_main.addWidget(text_edit)
        layout_main.addLayout(layout_buttons)
        edit_dialog.setLayout(layout_main)

        button_cancel.clicked.connect(edit_dialog.close)
        button_ok.clicked.connect(partial(do_edit, edit_dialog))

        edit_dialog.exec_()
