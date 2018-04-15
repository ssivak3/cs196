from music21 import*
#convert to Xml
musicxml.m21ToXml.typeToMusicXMLType('longa')
musicxml.m21ToXml.typeToMusicXMLType('quarter')
#Translate a music21 Note into an object ready to be parsed.
n = note.Note('c3')
n.quarterLength = 3
GEX = musicxml.m21ToXml.GeneralObjectExporter()
sc = GEX.fromGeneralNote(n)
sc.show('t')
# chord
ch = chord.Chord()
ch.quarterLength = 2
b = pitch.Pitch('A-2')
c = pitch.Pitch('D3')
d = pitch.Pitch('E4')
e = [b, c, d]
ch.pitches = e
MEX = musicxml.m21ToXml.MeasureExporter()
mxNoteList = MEX.chordToXml(ch)
MEX.dump(mxNoteList[0])
# clif
gc = clef.GClef()
MEX = musicxml.m21ToXml.MeasureExporter()
mxc = MEX.clefToXml(gc)
MEX.dump(mxc)
# coda direction
c = repeat.Coda()
MEX = musicxml.m21ToXml.MeasureExporter()
mxCodaDir = MEX.codaToXml(c)
MEX.dump(mxCodaDir)
# duration
d = duration.Duration(1.5)
MEX = musicxml.m21ToXml.MeasureExporter()
MEX.currentDivisions = 10
mxDuration = MEX.durationXml(d)
MEX.dump(mxDuration)
# nested tag
ppp = dynamics.Dynamic('ppp')
ppp.style.relativeY = -10
MEX = musicxml.m21ToXml.MeasureExporter()
mxDirection = MEX.dynamicToXml(ppp)
MEX.dump(mxDirection)