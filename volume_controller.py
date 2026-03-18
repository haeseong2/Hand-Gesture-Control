import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class VolumeController:
    def __init__(self):

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        volRange = self.volume.GetVolumeRange()

        self.minVol = volRange[0]
        self.maxVol = volRange[1]

    def set_volume(self, percent):

        vol = np.interp(percent,[0,100],[self.minVol,self.maxVol])

        self.volume.SetMasterVolumeLevel(vol,None)