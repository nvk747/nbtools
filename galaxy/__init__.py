"""
Galaxy extension for Jupyterlab via nbtools

A framework for creating user-friendly widgets and tools in Jupyter Notebook.
"""


# Import nbtools functionality
from .jupyter_extensions import (GalaxyMagic, load_ipython_extension, load_jupyter_server_extension, _jupyter_server_extension_paths, _jupyter_nbextension_paths)
from .widgets import build_ui,UIBuilder as GalaxyUIBuilder, UIOutput as GalaxyUIOutput, open
from .manager import NBTool, list, modified, register, unregister, tool
from .r_support import r_build_ui
from .remote_widgets import GalaxyAuthWidget, GalaxyTaskWidget, GalaxyJobWidget, session, register_session, get_session, display
from .local_widgets import GalaxyModuleWidget

__author__ = 'Thorin Tabor'
__copyright__ = 'Copyright 2016-2020, Regents of the University of California & Broad Institute'
__version__ = '20.05.1'
__status__ = 'Beta'
__license__ = 'BSD'


