# maya-toolkit-roller-coaster
Maya(2015-2018) toolkit used to save/load pose or animation clip.

### DEPENDENCY
- **QtSide** https://github.com/astips/QtSide
- **Mirror Plane** https://github.com/astips/maya-plugin-mirror-plane

### INSTALLATION
1. Download the latest release and unzip the folder where you want to live.
2. Copy folder "rollercoaster" to %USERPROFILE%\Documents\maya\scripts

### USAGE
Tip: You need to value the _**QT_SIDE_BINDING**_ env var before running the toolkit if you 
did not set/export this var when maya launched.
```python
import os
os.environ['QT_SIDE_BINDING'] = 'pyside'  # Maya2016: pyside, Maya2017+: pyside2
```
```python
# startup editor
from rollercoaster.main import run_editor
run_editor()


# startup pose creator
from rollercoaster.main import run_creator
run_creator('pose')


# startup clip creator
from rollercoaster.main import run_creator
run_creator('clip')
```
### PRESET > rollercoaster/presets.json
```json
{
    "manager": ["astips", "root"],
    "official": {
        "path": ""
    },
    "user": {
        "path": ""
    },
    "context": ["basic"],
    "theme": ["black", "light-black", "grey", "light-grey"],
    "const": {
        "datafile": "data.xml",
        "snapshot": "snapshot",
        "compress": "jpg",
        "additive": ".ADDITIVE"
    },
    "template": {"image": "icon_park"},
    "email": "animator.well@gmail.com"
}
```
- "manager" -- define super users of this toolkit (who can manager the **Official Tab**)
- "context" -- x-rig context names configured by user
- "email" -- your license register email used to auth professional version license

### XRIG Context Option > rollercoaster/core/mutils/option
Because of the diversity of rigging files, **rollercoaster** tool allow users config their own
xrig contexts.

for example : an open source rig file named 'kayla'

```python
from .base import XRigBase

class XRigKayla(XRigBase):
    CONTEXT_NAME = 'kayla'
    CTRL_TAG = ['_CON']

    LT_CTRL_TAG = ['L_']
    LT_CTRL_FORMAT = ['L_*']

    MD_CTRL_TAG = ['M_']
    MD_CTRL_FORMAT = ['M_*']

    RT_CTRL_TAG = ['R_']
    RT_CTRL_FORMAT = ['R_*']

    IK_CTRL_TAG = ['_ik']
    FK_CTRL_TAG = ['_fk']

    IK_FLIP_ATTR = []
    MD_FLIP_ATTR = []
    FACE_FLIP_ATTR = []
```

### SHORTCUTS
- Alt + Q
- Alt + W
- Alt + E
- Alt + R
- Alt + (1, 2, 3, 4)
- Ctrl + Tab
- Ctrl + C
- Ctrl + X
- Ctrl + V
- Ctrl + Z
- Ctrl + MMouse(Click/Scroll)
- `
- Space
- Esc