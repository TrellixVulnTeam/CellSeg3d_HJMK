import os
import warnings

import napari
import numpy as np
import pims
import skimage.io as io
from qtpy import QtGui
from qtpy.QtWidgets import QCheckBox
from qtpy.QtWidgets import QLabel
from qtpy.QtWidgets import QLayout
from qtpy.QtWidgets import QLineEdit
from qtpy.QtWidgets import QSizePolicy
from qtpy.QtWidgets import QVBoxLayout

from napari_cellseg_annotator import utils
from napari_cellseg_annotator import interface as ui
from napari_cellseg_annotator.launch_review import launch_review
from napari_cellseg_annotator.plugin_base import BasePlugin

warnings.formatwarning = utils.format_Warning


global_launched_before = False


class Reviewer(BasePlugin):
    """A plugin for selecting volumes and labels file and launching the review process.
    Inherits from : :doc:`plugin_base`"""

    def __init__(self, viewer: "napari.viewer.Viewer"):
        """Creates a Reviewer plugin with several buttons :

        * Open file prompt to select volumes directory

        * Open file prompt to select labels directory

        * A dropdown menu with a choice of png or tif filetypes

        * A checkbox if you want to create a new status csv for the dataset

        * A button to launch the review process (see :doc:`launch_review`)
        """

        super().__init__(viewer)

        # self._viewer = viewer

        self.textbox = QLineEdit(self)
        self.textbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.checkBox = QCheckBox("Create new dataset ?")
        self.checkBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btn_start = ui.make_button(
            "Start reviewing", self.run_review, self
        )

        self.lbl_mod = QLabel("Model name", self)

        self.warn_label = QLabel(
            "WARNING : You already have a review session running.\n"
            "Launching another will close the current one,\n"
            " make sure to save your work beforehand"
        )
        pal = self.warn_label.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
        self.warn_label.setPalette(pal)

        self.build()

    def build(self):
        """Build buttons in a layout and add them to the napari Viewer"""

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 1, 11)
        vbox.setSizeConstraint(QLayout.SetFixedSize)

        global global_launched_before
        if global_launched_before:
            vbox.addWidget(self.warn_label)
            warnings.warn(
                "You already have a review session running.\n"
                "Launching another will close the current one,\n"
                " make sure to save your work beforehand"
            )

        ui.add_blank(self, vbox)
        ###########################
        data_group_w, data_group_l = ui.make_group("Data")

        data_group_l.addWidget(
            ui.combine_blocks(self.filetype_choice, self.file_handling_box), alignment = ui.LEFT_AL
        )
        self.filetype_choice.setVisible(False)

        data_group_l.addWidget(
            ui.combine_blocks(self.btn_image, self.lbl_image)
        )

        data_group_l.addWidget(
            ui.combine_blocks(self.btn_label, self.lbl_label)
        )

        data_group_w.setLayout(data_group_l)
        vbox.addWidget(data_group_w)
        ###########################
        ui.add_blank(self, vbox)
        ###########################
        # vbox.addWidget(self.lblft2)
        csv_param_w, csv_param_l = ui.make_group("CSV parameters")

        csv_param_l.addWidget(
            ui.combine_blocks(
                self.textbox,
                self.lbl_mod,
                horizontal=False,
                l=5,
                t=5,
                r=5,
                b=5,
            )
        )
        csv_param_l.addWidget(self.checkBox)

        csv_param_w.setLayout(csv_param_l)
        vbox.addWidget(csv_param_w)
        ###########################
        ui.add_blank(self, vbox)
        ###########################

        vbox.addWidget(self.btn_start)
        vbox.addWidget(self.btn_close)

        ui.make_scrollable(
            contained_layout=vbox,
            containing_widget=self,
            min_wh=[185, 200],
            base_wh=[190, 600],
        )
        # self.show()
        # self._viewer.window.add_dock_widget(self, name="Reviewer", area="right")

    def run_review(self):

        """Launches review process by loading the files from the chosen folders,
        and adds several widgets to the napari Viewer.
        If the review process has been launched once before,
        closes the window entirely and launches the review process in a fresh window.

        TODO:

        * Save work done before leaving

        See :doc:`launch_review`

        Returns:
            napari.viewer.Viewer: self.viewer
        """

        self.filetype = self.filetype_choice.currentText()
        self.as_folder = self.file_handling_box.isChecked()

        #################################
        #################################
        #################################
        # TODO test remove later
        if utils.ENABLE_TEST_MODE():
            if self.as_folder:
                self.image_path = "C:/Users/Cyril/Desktop/Proj_bachelor/data/visual_png/sample"
                self.label_path = "C:/Users/Cyril/Desktop/Proj_bachelor/data/visual_png/sample_labels"
            else:
                self.image_path = "C:/Users/Cyril/Desktop/Proj_bachelor/data/visual_tif/volumes/images.tif"
                self.label_path = "C:/Users/Cyril/Desktop/Proj_bachelor/data/visual_tif/labels/testing_im.tif"
        #################################
        #################################
        #################################

        images = utils.load_images(
            self.image_path, self.filetype, self.as_folder
        )
        if (
            self.label_path == ""
        ):  # saves empty images of the same size as original images
            if self.as_folder:
                labels = np.zeros_like(images.compute())  # dask to numpy
            self.label_path = os.path.join(
                os.path.dirname(self.image_path), self.textbox.text()
            )
            os.makedirs(self.label_path, exist_ok=True)

            for i in range(len(labels)):
                io.imsave(
                    os.path.join(
                        self.label_path, str(i).zfill(4) + self.filetype
                    ),
                    labels[i],
                )
        else:
            labels = utils.load_saved_masks(
                self.label_path,
                self.filetype,
                self.as_folder,
            )
        try:
            labels_raw = utils.load_raw_masks(
                self.label_path + "_raw", self.filetype
            )
        except pims.UnknownFormatError:
            labels_raw = None
        except FileNotFoundError:
            # TODO : might not work, test with predi labels later
            labels_raw = None

        global global_launched_before
        if global_launched_before:
            new_viewer = napari.Viewer()
            view1 = launch_review(
                new_viewer,
                images,
                labels,
                labels_raw,
                self.label_path,
                self.textbox.text(),
                self.checkBox.isChecked(),
                self.filetype,
                self.as_folder,
            )
            warnings.warn(
                "Opening several loader sessions in one window is not supported; opening in new window"
            )
            self._viewer.close()
        else:
            viewer = self._viewer
            print("new sess")
            view1 = launch_review(
                viewer,
                images,
                labels,
                labels_raw,
                self.label_path,
                self.textbox.text(),
                self.checkBox.isChecked(),
                self.filetype,
                self.as_folder,
            )
            self.close()

            global_launched_before = True

        return view1

    def close(self):
        """Close widget and remove it from window.
        Sets the check for an active session to false, so that if the user closes manually and doesn't launch the review,
        the active session warning does not display and a new viewer is not opened when launching for the first time.
        """
        global global_launched_before  # if user closes window rather than launching review, does not count as active session
        if global_launched_before:
            global_launched_before = False
        # print("close req")
        try:
            self._viewer.window.remove_dock_widget(self)
        except LookupError:
            return
