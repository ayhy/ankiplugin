# -*- coding: utf-8 -*-

from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
#from aqt.utils import shortcut, showInfo #debug

directions = [
(1, Qt.CTRL + Qt.Key_Tab),
(-1, Qt.CTRL + Qt.SHIFT + Qt.Key_Tab),
]

def jumpBlankField(editor, direction):

    candidateField=editor.currentField
    if direction < 0:
        backward_fields=reversed(editor.note.fields[:editor.currentField])
        candidateField -= next((diff_num for diff_num, text in enumerate(backward_fields) if text), editor.currentField -1)
        #when all previous fields are blank, go back to start

        candidateField += direction
        #showInfo("Backward Move: to field %d" % candidateField) #debug

    else:
        forward_fields=editor.note.fields[editor.currentField+1:]
        candidateField += next((diff_num for diff_num, text in enumerate(forward_fields) if text), len(forward_fields) -1)
        #when all following fields are blank, go forward to end

        candidateField += direction
        #showInfo("Forward Move: to field %d" % candidateField)  #debug

        candidateField = max(0, candidateField)
        candidateField = min(len(editor.note.fields), candidateField)

    editor.web.eval("focusField(%d);" % candidateField)
    editor.currentField=candidateField

def onSetupButtons(editor):
    # add shortcut to access jumpBlank
    for code, key in directions:
        s = QShortcut(QKeySequence(key), editor.parentWindow)
        s.connect(s, SIGNAL("activated()"),
                  lambda c=code: jumpBlankField(editor, c))

addHook("setupEditorButtons", onSetupButtons)
