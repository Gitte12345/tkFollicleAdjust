# tkFollicleAdjust.py

import maya.cmds as cmds
import maya.mel as mel
from functools import partial 

folAttributes = ['overrideDynamics', 'stiffness', 'damp', 'clumpWidth', 'clumpWidthMult','densityMult', 'curlMult']



def cShrinkWin(windowToClose, *args):
	cmds.window(windowToClose, e=1, h=20)
	cmds.window(windowToClose, e=1, w=300)


def tkSetAllFolAttrib(*args):
	for attrib in folAttributes:
		tkSetFolAttrib(attrib)


def tkDefaultAllFolAttrib(*args):
	myFol = tkGetFollices()
	hs = cmds.listConnections(myFol[0], sh=1, type='hairSystem')[0]
	cmds.floatField('stiffness', v=1, e=1)

	value = cmds.getAttr(hs + '.damp')
	cmds.floatField('damp', v=value, e=1)

	value = cmds.getAttr(hs + '.clumpWidth')
	cmds.floatField('clumpWidth', v=value, e=1)

	cmds.floatField('clumpWidthMult', v=1, e=1)
	cmds.floatField('densityMult', v=1, e=1)
	cmds.floatField('curlMult', v=1, e=1)

	tkSetAllFolAttrib()





def tkSetFolAttrib(attrib, *args):
	myFol = tkGetFollices()
	if attrib != 'overrideDynamics':
		value = cmds.floatField(attrib, v=1, q=1)
	else:
		value = cmds.checkBox(attrib, v=1, q=1)

	for fol in myFol:
		cmds.setAttr(fol[0] + '.' + attrib, value)


def tkGetAllFolAttrib(*args):
	for attrib in folAttributes:
		tkGetFolAttrib(attrib)


def tkGetFolAttrib(attrib, *args):
	myFol = tkGetFollices()

	value = cmds.getAttr(myFol[0][0] + '.' + attrib)
	if attrib != 'overrideDynamics':
		cmds.floatField(attrib, v=value, e=1)
	else:
		cmds.checkBox(attrib, v=value, e=1)



def tkGetFollices(*args):
	myCrv = []
	myFol = []
	curSel = cmds.ls(sl=1, l=1)
	for sel in curSel:
		if cmds.objectType(sel, isType='nurbsCurve'):
			myCrv.append(sel)
		else:
			shapes = cmds.listRelatives(sel, s=1, type='nurbsCurve')
			if shapes:
				myCrv.append(shapes)

	for crv in myCrv:
		fol = cmds.listConnections(crv, sh=1, t='follicle')
		if fol:
			myFol.append(fol)

	return myFol





def tkFollicleAdjustUI(*args):
	ver = 0.1
	colSilverDark 		= [0.08, 0.09, 0.10];
	colSilverMid 		= [0.23, 0.23, 0.23];
	colSilverLight 		= [0.39, 0.46, 0.50];
	colRed 		 		= [0.46, 0.39, 0.39];
	colGreen	 		= [0.39, 0.46, 0.39];
	windowStartHeight = 50
	windowStartWidth = 450
	bh1 = 22
	if (cmds.window('win_tkFollicleAdjust', exists=1)):
		cmds.deleteUI('win_tkFollicleAdjust')
	myWindow = cmds.window('win_tkFollicleAdjust', t=('tkFollicleAdjust ' + str(ver)), s=1)

	cmds.columnLayout(adj=1, bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]))
	cmds.frameLayout('flFollicleAttributes', l='Follicle Attributes', bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]), cll=1, cl=0, cc=partial(cShrinkWin, "win_tkFollicleAdjust"))

	cmds.rowColumnLayout(bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]), nc=4, cw=[(1, 60), (2, 180), (3, 60), (4, 60)])


	cmds.button(l='Read All', h=bh1, c=partial(tkGetAllFolAttrib), bgc=(colGreen[0], colGreen[1], colGreen[2]))
	cmds.text(' ')
	cmds.button(l='Default', h=bh1, c=partial(tkDefaultAllFolAttrib))
	cmds.button(l='Set All', h=bh1, c=partial(tkSetAllFolAttrib), bgc=(colRed[0], colRed[1], colRed[2]))

	cmds.setParent('..')
	cmds.separator(bgc=(colSilverDark[0], colSilverDark[1], colSilverDark[2]))
	cmds.rowColumnLayout(bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]), nc=4, cw=[(1, 60), (2, 180), (3, 60), (4, 60)])

	cmds.button(l='Read', h=bh1, c=partial(tkGetFolAttrib, 'overrideDynamics'), bgc=(colGreen[0], colGreen[1], colGreen[2]))
	cmds.textField('overrideDynamics', tx = 'overrideDynamics', ed=0)
	cmds.checkBox('overrideDynamics', l='on')
	cmds.button(l='Set Values', h=bh1, c=partial(tkSetFolAttrib, 'overrideDynamics'), bgc=(colRed[0], colRed[1], colRed[2]))


	cmds.button(l='Read', h=bh1, c=partial(tkGetFolAttrib, 'stiffness'), bgc=(colGreen[0], colGreen[1], colGreen[2]))
	cmds.textField('stiffness', tx = 'stiffness', ed=0)
	cmds.floatField('stiffness', min=0, max=1, h=bh1, ed=1, bgc=(0, 0, 0))
	cmds.button(l='Set Values', h=bh1, c=partial(tkSetFolAttrib, 'stiffness'), bgc=(colRed[0], colRed[1], colRed[2]))

	cmds.button(l='Read', h=bh1, c=partial(tkGetFolAttrib, 'damp'), bgc=(colGreen[0], colGreen[1], colGreen[2]))
	cmds.textField('damp', tx = 'damp', ed=0)
	cmds.floatField('damp', min=0, h=bh1, ed=1, bgc=(0, 0, 0))
	cmds.button(l='Set Values', h=bh1, c=partial(tkSetFolAttrib, 'damp'), bgc=(colRed[0], colRed[1], colRed[2]))

	cmds.button(l='Read', h=bh1, c=partial(tkGetFolAttrib, 'clumpWidth'), bgc=(colGreen[0], colGreen[1], colGreen[2]))
	cmds.textField('clumpWidth', tx = 'clumpWidth', ed=0)
	cmds.floatField('clumpWidth', h=bh1, ed=1, bgc=(0, 0, 0))
	cmds.button(l='Set Values', h=bh1, c=partial(tkSetFolAttrib, 'clumpWidth'), bgc=(colRed[0], colRed[1], colRed[2]))

	cmds.button(l='Read', h=bh1, c=partial(tkGetFolAttrib, 'clumpWidthMult'), bgc=(colGreen[0], colGreen[1], colGreen[2]))
	cmds.textField('clumpWidthMult', tx = 'clumpWidthMult', ed=0)
	cmds.floatField('clumpWidthMult', h=bh1, ed=1, bgc=(0, 0, 0))
	cmds.button(l='Set Values', h=bh1, c=partial(tkSetFolAttrib, 'clumpWidthMult'), bgc=(colRed[0], colRed[1], colRed[2]))

	cmds.button(l='Read', h=bh1, c=partial(tkGetFolAttrib, 'densityMult'), bgc=(colGreen[0], colGreen[1], colGreen[2]))
	cmds.textField('densityMult', tx = 'densityMult', ed=0)
	cmds.floatField('densityMult', h=bh1, ed=1, bgc=(0, 0, 0))
	cmds.button(l='Set Values', h=bh1, c=partial(tkSetFolAttrib, 'densityMult'), bgc=(colRed[0], colRed[1], colRed[2]))

	cmds.button(l='Read', h=bh1, c=partial(tkGetFolAttrib, 'curlMult'), bgc=(colGreen[0], colGreen[1], colGreen[2]))
	cmds.textField('curlMult', tx = 'curlMult', ed=0)
	cmds.floatField('curlMult', h=bh1, ed=1, bgc=(0, 0, 0))
	cmds.button(l='Set Values', h=bh1, c=partial(tkSetFolAttrib, 'curlMult'), bgc=(colRed[0], colRed[1], colRed[2]))

	cmds.setParent('..')


	cmds.showWindow(myWindow)

tkFollicleAdjustUI()