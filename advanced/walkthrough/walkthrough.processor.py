## Copyright (C) LIMSI-CNRS (2014)
##
## contributor(s) : Jorge Gascon, Damien Touraine, David Poirier-Quinot,
## Laurent Pointal, Julian Adenauer, 
## 
## This software is a computer program whose purpose is to distribute
## blender to render on Virtual Reality device systems.
## 
## This software is governed by the CeCILL  license under French law and
## abiding by the rules of distribution of free software.  You can  use, 
## modify and/ or redistribute the software under the terms of the CeCILL
## license as circulated by CEA, CNRS and INRIA at the following URL
## "http://www.cecill.info". 
## 
## As a counterpart to the access to the source code and  rights to copy,
## modify and redistribute granted by the license, users are provided only
## with a limited warranty  and the software's author,  the holder of the
## economic rights,  and the successive licensors  have only  limited
## liability. 
## 
## In this respect, the user's attention is drawn to the risks associated
## with loading,  using,  modifying and/or developing or reproducing the
## software by the user in light of its specific status of free software,
## that may mean  that it is complicated to manipulate,  and  that  also
## therefore means  that it is reserved for developers  and  experienced
## professionals having in-depth computer knowledge. Users are therefore
## encouraged to load and test the software's suitability as regards their
## requirements in conditions enabling the security of their systems and/or 
## data to be ensured and,  more generally, to use and operate it in the 
## same conditions as regards security. 
## 
## The fact that you are presently reading this means that you have had
## knowledge of the CeCILL license and that you accept its terms.
## 

import blendervr
import os

blendervr.processor.appendProcessor(os.path.join(blendervr.tools.getRootPath(), 'samples', 'processors.py'))

if blendervr.is_virtual_environment():
    import bge
    import math
    import mathutils
    import copy

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent, head_navigator = True)

            if hasattr(self, '_navigator'):
                self._navigator.setPositionFactors(1, 20.0, 1.0)

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

                self._car = bge.logic.getCurrentScene().objects.get("carro_preto")
                self._movement = mathutils.Vector([0, 0, 0])
                self._rotation = mathutils.Vector([0, 0, 0])

        def buttons(self, info):
            if (info['button'] == 0) and (info['state'] == 1):
                self._navigator.update(self._navigator.CALIBRATE, self._user)
            if (info['button'] == 1) and (info['state'] == 1):
                self._navigator.update(self._navigator.TOGGLE, self._user)
            if (info['button'] == 2) and (info['state'] == 1):
                self.reset(info['users'])
            if (info['button'] == 3) and (info['state'] == 1):
                self.BlenderVR.quit("because user asked !")

        def run(self):
            self._car.applyMovement(self._movement, True)
            self._car.applyRotation(self._rotation, True)

        def rum_a(self, info):
            MOVE = 0.1 #speed
            ROT = math.radians(1)
            car = bge.logic.getCurrentScene().objects.get("carro_preto")
            if info['channel'][1] < 0.2:
                self._movement = mathutils.Vector([0, MOVE, 0])
            elif info['channel'][1] > 0.8:
                self._movement = mathutils.Vector([0, -MOVE, 0])
            else:
                self._movement = mathutils.Vector([0, 0, 0])

            if info['channel'][0] < 0.2:
                self._rotation = mathutils.Vector([0, 0, ROT])
            elif info['channel'][0] > 0.8:
                self._rotation = mathutils.Vector([0, 0, -ROT])
            else:
                self._rotation = mathutils.Vector([0, 0, 0])

elif blendervr.is_creating_loader():

    import bpy
    
    class Processor(blendervr.processor.getProcessor()):

        def __init__(self, creator):
            super(Processor, self).__init__(creator)

elif blendervr.is_console():

    class Processor(blendervr.processor.getProcessor()):

        def __init__(self, console):
            ui_path = os.path.join(blendervr.tools.getModulePath(), 'designer', 'walkthrough.ui')
            super(Processor, self).__init__(console, ui_path, head_navigator = True)

            if hasattr(self, '_navigator'):
                self._navigator.registerWidget(self._ui.HC_Nav)

        def useLoader(self):
            return True
