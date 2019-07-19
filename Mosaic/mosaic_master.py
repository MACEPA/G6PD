from FlowCytometryTools import FCMeasurement
from Mosaic.make_table import model_table
from Mosaic.calc_bright_cells import prep_fcs, calc_bright_cells

test = FCMeasurement(ID='', datafile='{}/1.fcs'.format(fcs_dir))
channels = test.channels

table = model_table()

data = prep_fcs(fcs)