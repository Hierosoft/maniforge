from __future__ import print_function
from __future__ import division
import logging
import sys

if sys.version_info.major >= 3:
    from logging import getLogger
else:
    # Python 2
    from hierosoft.logging2 import getLogger

from maniforge.gcodefollower import GCodeFollower

logger = getLogger(__name__)


def usage():
    # print(CLI_HELP)
    print(GCodeFollower.getDocumentation())
    GCodeFollower.printSettingsDocumentation()
    print("")


class GCodeFollowerArgParser():
    '''
    The run arguments are parsed here in case you want to change them
    via the GUI. They are parsed once and for all to avoid late parsing
    as long as you only make one instance of this class!

    '''
    def __init__(self):
        '''
        This uses sys.argv! See usage for documentation.
        '''
        global verbosity
        self.verbose = False if verbosity < 1 else True
        self.temperatures = None
        self.template_gcode_path = None
        self.help = False
        seqArgs = []

        for argI in range(1, len(sys.argv)):
            arg = sys.argv[argI]
            if arg == "--verbose":
                self.verbose = True
                logger.setLevel(logging.INFO)
                logger.info("* Verbose mode is enabled.")
            elif arg == "--debug":
                self.verbose = True
                logger.setLevel(logging.DEBUG)
            elif arg == "--help":
                self.help = True
            elif arg.startswith("--"):
                raise ValueError("The argument {} is invalid."
                                 "".format(arg))
            else:
                seqArgs.append(arg)

        if (len(seqArgs) == 1) or (len(seqArgs) == 3):
            self.template_gcode_path = seqArgs[0]
        if len(seqArgs) == 3:
            self.temperatures = [seqArgs[1], seqArgs[2]]
        elif len(seqArgs) == 2:
            self.temperatures = [seqArgs[0], seqArgs[1]]
        if len(seqArgs) > 3:
            usage()
            raise ValueError("Error: There were too many arguments.")

        if self.verbose:
            print("seqArgs: {}".format(seqArgs))
            print("template_gcode_path: {}".format(self.template_gcode_path))
            print("temperatures: {}".format(self.temperatures))
