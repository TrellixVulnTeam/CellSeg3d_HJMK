# napari-cellseg3d: a napari plug-in for 3d deep learning models for cell segmentation


<img src="docs/res/logo/logo_diag.png" title="cellseg3d" alt="cellseg3d logo" width="250" align="right" vspace = "80"/>

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://www.gnu.org/licenses/mit(https://github.com/AdaptiveMotorControlLab/CellSeg3d/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-cellseg3d.svg?color=green)](https://pypi.org/project/napari-cellseg3d)
[![Python Version](https://img.shields.io/pypi/pyversions/CellSeg3d.svg?color=green)](https://python.org)
[![tests](https://github.com/AdaptiveMotorControlLab/CellSeg3d/workflows/tests/badge.svg)](https://github.com/AdaptiveMotorControlLab/CellSeg3d/actions)
[![codecov](https://codecov.io/gh/AdaptiveMotorControlLab/napari-cellseg3d/branch/main/graph/badge.svg)](https://codecov.io/gh/AdaptiveMotorControlLab/CellSeg3d)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-cellseg3d)](https://napari-hub.org/plugins/CellSeg3d)


A napari plugin for 3D cell segmentation: training, inference, and data review. In particular, this project was developed for analysis of mesoSPIM-acquired (cleared tissue + lightsheet) datasets.

**Pre-Alpha version, please expect bugs and issues. Reporting them on the Github repository would help us a lot!**

----------------------------------

## Installation

You can install `napari-cellseg-3d` via [pip] (pypi-test placeholder):  

    pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ napari-cellseg3d==0.0.3

## Documentation

Available on the [Github pages website](https://adaptivemotorcontrollab.github.io/cellseg3d-docs/)

Source files can be found at https://AdaptiveMotorControlLab.github.io/cellseg3d-docs

You can also generate docs by running ``make html`` in the docs folder.

## Usage

To use the plugin, please run:
```
napari
```
Then go into Plugins > napari-cellseg-3d, and choose which tool to use.

- **Review**: This module allows you to review your labels, from predictions or manual labeling, and correct them if needed. It then saves the status of each file in a csv, for easier monitoring.
- **Inference**: This module allows you to use pre-trained segmentation algorithms on volumes to automatically label cells and compute statistics.
- **Train**:  This module allows you to train segmentation algorithms from labeled volumes.
- **Utilities**: This module allows you to perform several actions like cropping your volumes and labels dynamically, by selecting a fixed size volume and moving it around the image; computing prediction scores from ground truth and predicition labels; or converting labels from instance to segmentation and the opposite. 


## Requirements
**Python >= 3.8 required**

Requires manual installation of **pytorch** and **MONAI**.

For Pytorch, please see [PyTorch's website for installation instructions].
A CUDA-capable GPU is not needed but very strongly recommended, especially for training.

If you get errors from MONAI regarding missing readers, please see [MONAI's optional dependencies] page for instructions on getting the readers required by your images.


## Issues

If you encounter any problems, please [file an issue] along with a detailed description.


## Testing 

To run tests locally: 

- Locally : run ``pytest`` in the plugin folder
- Locally with coverage : In the plugin folder, run ``coverage run --source=src -m pytest`` then ``coverage.xml`` to generate a .xml coverage file.
- With tox : run ``tox`` in the plugin folder (will simulate tests with several python and OS configs, requires substantial storage space)

## Contributing

Contributions are very welcome. 

Please ensure the coverage at least stays the same before you submit a pull request.

For local installation from Github cloning, please run:

```
pip install -e .
```

## License

Distributed under the terms of the [MIT] license.

"napari-cellseg-3d" is free and open source software.


[file an issue]: https://github.com/AdaptiveMotorControlLab/CellSeg3d/issues
[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/

[PyTorch's website for installation instructions]: https://pytorch.org/get-started/locally/
[MONAI's optional dependencies]: https://docs.monai.io/en/stable/installation.html#installing-the-recommended-dependencies

## Acknowledgements 

This plugin was developed by Cyril Achard & Maxime Vidal.

This work was funded, in part, from the Wyss Center to the Adaptive Motor Control Lab.


## Plugin base
This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/plugins/stable/index.html
-->
