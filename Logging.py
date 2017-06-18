import sys
import time

DO_TRACE = False


def tracefunc(frame, event, arg, indent=[0]):
	if event == "call" and DO_TRACE:
		indent[0] += 2
		logline(str("-" * indent[0] + "> call to: " + frame.f_code.co_name))
	elif event == "return" and DO_TRACE:
		logline(str("<" + "-" * indent[0] + " exit of: " + frame.f_code.co_name))
		indent[0] -= 2
	elif event == 'exception':
		co = frame.f_code
		func_name = co.co_name
		line_no = frame.f_lineno
		filename = co.co_filename
		exc_type, exc_value, exc_traceback = arg
		logline(str('=> Exception: %s "%s" on line %s of %s' % (exc_type.__name__, exc_value, line_no, func_name)))
	return tracefunc


def startlogging():
	clearlog()
	sys.settrace(tracefunc)


def logline(msg):
	f = open(getlogfilename(), 'a')
	f.write(msg+"\n")
	f.close()


def clearlog():
	f = open(getlogfilename(), 'w')
	f.write(str(time.strftime("%Y-%m-%d %H:%M")) + "\n\n")
	f.close()


def getlogfilename():
	return __file__.replace('.pyc', '.log').replace('Logging.py', 'Log.log')
