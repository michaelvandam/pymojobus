from cpm import CPM
from prm import PRM
from rdm import RDM
from anes import ANES
from default import DefaultDevice

deviceTypes = {"DEFAULT":DefaultDevice,
                "RDM":RDM,
                "CPM":CPM,
                "PRM":PRM,
                "ANES":ANES}