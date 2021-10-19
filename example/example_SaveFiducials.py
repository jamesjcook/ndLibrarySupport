# load a fiducial file from memory 
slicer.util.loadMarkupsFiducialList("/path/to/list/F.fcsv")

#programatically add points
slicer.modules.markups.logic().AddFiducial(1.0, -2.0, 3.3)

"C:\Users\hmm56\Documents\F.mrk.json"