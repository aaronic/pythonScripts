from omega_autoweb import *

def find1stEFA(robot):
    try:
        robot.switchFrame('qdniframe')
        robot.switchFrame('BlockTitle_2000')
        FATitle = robot.getText('text','TLY: EFA')
        if 'TLY: EFA' in FATitle:
            return True
        else:
            return False
    except Exception as err:
        print(str(err))
        return False
    finally:
        robot.switchBack()
        robot.switchBack()

def find2ndEFA(robot):
    try:
        robot.switchFrame('qdniframe')
        robot.switchFrame('BlockTitle_20000')
        FATitle = robot.getText('text','TLY: 2nd level EFA')
        if 'TLY: 2nd level EFA' in FATitle:
            return True
        else:
            return False
    except Exception as err:
        print(str(err))
        return False
    finally:
        robot.switchBack()
        robot.switchBack()

def get1stEFAComment(robot):
    try:
        robot.switchFrame('qdniframe')
        robot.switchFrame('Frame_2000')
        comment = robot.getFirstElement('xpath','//*[@id="F2420"]')
        if comment is not None:
            return comment.text
    except Exception as err:
        print(str(err))
        return False
    finally:
        robot.switchBack()
        robot.switchBack()

def get2ndEFAComment(robot):
    try:
        robot.switchFrame('qdniframe')
        robot.switchFrame('Frame_20000')
        comment = robot.getFirstElement('xpath','//*[@id="F2841"]')
        if comment is not None:
            return comment.text
    except Exception as err:
        print(str(err))
        return False
    finally:
        robot.switchBack()
        robot.switchBack()
SQs = [
'SQ01353611',
'SQ01353611',
'SQ01355312',
'SQ01355508',
'SQ01355616',
'SQ01355761',
'SQ01355761',
'SQ01355987',
'SQ01355858',
'SQ01355671',
'SQ01355674',
'SQ01356042',
'SQ01356042',
'SQ01356042',
'SQ01356042',
'SQ01356042',
'SQ01356603',
'SQ01356603',
'SQ01356954',
'SQ01357662',
'SQ01357662',
'SQ01357662',
'SQ01357662',
'SQ01357662',
'SQ01357111',
'SQ01357995',
'SQ01357995',
'SQ01357995',
'SQ01357995',
'SQ01357995',
'SQ01357995',
'SQ01357995',
'SQ01357995',
'SQ01357939',
'SQ01357939',
'SQ01357936',
'SQ01357994',
'SQ01357956',
'SQ01358059',
'SQ01359295',
'SQ01359308',
'SQ01359303',
'SQ01359303',
]
url = 'http://cvppasip02/SPAS/QDN/iFrameIndex.aspx?SQNum=SQ01346557&id=309'
robot = webRobot()
for SQ in SQs:
    url = 'http://cvppasip02/SPAS/QDN/iFrameIndex.aspx?SQNum='+SQ+'&id=309'
    robot.loadPage(url)
    if find1stEFA(robot):
        print(get1stEFAComment(robot))
    elif find2ndEFA(robot):
        print(get2ndEFAComment(robot))
robot.shutDown()
