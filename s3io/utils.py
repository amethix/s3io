import sys

def printStuff(msg, arg):
    """ Print msg+perc to stdout and flush 
    msg = "Converting control data %d%%"
    """
    sys.stdout.write('\r')
    sys.stdout.write(msg % (arg))
    sys.stdout.flush()

