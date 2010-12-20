from cpm import CPM
from prm import PRM
from rdm import RDM
from fdm import FDM
from anes import ANES
from default import DefaultDevice

deviceTypes = {"DEFAULT":DefaultDevice,
                "RDM":RDM,
                "CPM":CPM,
                "PRM":PRM,
                "FDM":FDM,
                "ANES":ANES}