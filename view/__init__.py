from deviceviews.cpmview import CPMView
from deviceviews.rdmview import RDMView
from deviceviews.prmview import PRMView
from deviceviews.anesview import ANESView

deviceViewTypes = { "RDM":RDMView,
                "CPM":CPMView,
                "PRM":PRMView,
                "ANES":ANESView}