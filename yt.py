#!/usr/bin/python

import sys, getopt, os

possibleScripts = "Possible scripts:" + \
        "\n\tnew-proj" + \
        "\n\ttranscode-proj"

usageStrs = {
    "yt": "Usage: yt [-h | --help] <script> <scriptopts>\n" + possibleScripts,
    "new-proj": "Usage: yt new-proj " + \
            "[-h | --help] " + \
            "{-n <projName> | --projName=<projName>} " + \
            "[-v | --verbose] " + \
            "[-r <videoRootDir> | --videoRootDir=<videoRootDir> ] " + \
            "\n\nExplanation of arguments:" + \
            "\n\t-h | --help:\n\t\tPrint the help string and exit" + \
            "\n\t-n <projName> | --projName=<projName>:\n\t\tThe name of the new project. Mandatory argument." + \
            "\n\t-v | --verbose:\n\t\tPrints debug output during script execution" + \
            "\n\t-r <videoRootDir> | --videoRootDir=<videoRootDir>:\n\t\t" + \
            "Sets the YouTube video root directory. Default: ~/Videos/YouTube/sources/" + \
            "\n\nThe new-proj script will create the common folder " + \
            "structure at the root directory with the provided project name",
    "transcode-proj": "Usage: yt transcode-proj " + \
            "[-h | --help] " + \
            "{-n <projName> | --projName=<projName>} " + \
            "[-v | --verbose] " + \
            "[-r <videoRootDir> | --videoRootDir=<videoRootDir> ] " + \
            "[-m | --mock ] " + \
            "\n\nExplanation of arguments:" + \
            "\n\t-h | --help:\n\t\tPrint the help string and exit" + \
            "\n\t-n <projName> | --projName=<projName>:\n\t\t" + \
            "The name of the project for which to transcode source footage. Mandatory argument." + \
            "\n\t-v | --verbose:\n\t\tPrints debug output during script execution" + \
            "\n\t-r <videoRootDir> | --videoRootDir=<videoRootDir>:\n\t\t" + \
            "Sets the YouTube video root directory. Default: ~/Videos/YouTube/sources/" + \
            "\n\t-m | --mock:\n\t\tPrints out the transcode command without actuall running it" + \
            "\n\nThe transcode-proj script will transcode all the files in the " + \
            "projName/video/ folder.",
}

errStrs = {
    "noScriptName": "Error: did not provide script name.\nPossible options:" + possibleScripts,
    "notImplErr": "Error: calling an unimplemented function",
    "whichScriptUnrecognizedArg": "Error: Unrecognized argument to yt.\n" + usageStrs[ "yt" ],
    "getoptFailure": "Error: getopt failed in the parseOpt function! Error message:",
    "new-projNoProj": "Error: project name not provided to the new-proj script!",
    "new-projProjExists": "Error: project with this name already exists!",
}

class BaseScript( object ):
    cfg = {
        "projName": "",
        "videoRootDir": "~/Videos/YouTube/sources/",
        "verbose": False,
    }
    short_opt = "hn:r:v"
    long_opt = [ "help", "projName=", "videoRootDir=", "verbose" ]

    def __init__( self ):
        # Not much in the default case
        pass

    def parseOpts( self, scriptArgs ):
        print( errStrs[ "notImplErr" ] )
        sys.exit( 1 )

    def execScript( self ):
        print( errStrs[ "notImplErr" ] )
        sys.exit( 1 )


class NewProjScript( BaseScript ):
    def __init__( self ):
        # Not much in this case either, since the default cfg and opts apply.
        pass

    def parseOpts( self, scriptArgs ):
        try:
            opts, args = getopt.getopt(
                    scriptArgs, self.short_opt, self.long_opt )
        except getopt.GetoptError as err:
            print( errStrs[ "getoptFailure" ] )
            print( err )
            print( usageStrs[ "new-proj" ] )
            sys.exit( 1 )

        for opt, arg in opts:
            if opt in ( "-h", "--help" ):
                print( usageStrs[ "new-proj" ] )
                sys.exit()
            elif opt in ( "-n", "--projName" ):
                self.cfg[ "projName" ] = arg
            elif opt in ( "-r", "--videoRootDir" ):
                self.cfg[ "videoRootDir" ] = arg
            elif opt in ( "-v", "--verbose" ):
                self.cfg[ "verbose" ] = True
        
        if self.cfg[ "projName" ] == "":
            print( errStrs[ "new-projNoProj" ] )
            print( usageStrs[ "new-proj" ] )
            sys.exit( 1 )
            

    def execScript( self ):
        if self.cfg[ "verbose" ]:
            print( "Executing new-proj script with config: ", self.cfg )
        
        projPath = os.path.join( 
                self.cfg[ "videoRootDir" ], self.cfg[ "projName" ] )

        if self.cfg[ "verbose" ]:
            print( "About to make project path: ", projPath )

        try:
            os.makedirs( projPath )
        except FileExistsError:
            print( errStrs[ "new-projProjExists" ] )
            print( "Failed path: ", projPath )
            sys.exit( 1 )

        for subFolder in [ "audio", "photo", "video" ]:
            projSubPath = os.path.join( projPath, subFolder )
            if self.cfg[ "verbose" ]:
                print( "About to make project sub-path: ", projSubPath )
            os.makedirs( projSubPath )

        if self.cfg[ "verbose" ]:
            print( "Finished making the folder structure for the new project!" )



class TranscodeProjScript( BaseScript ):
    def __init__( self ):
        # In this case, need to add some extra getopt and cfg parameters.
        self.short_opt += "m"
        self.long_opt.append( "mock" )
        self.cfg[ "mock" ] = False

    def parseOpts( self, scriptArgs ):
        # TODO: Implement the opt parser
        pass

    def execScript( self ):
        # TODO: Implement the script
        pass


def whichScript( argv ):
    if len( argv ) == 0:
        print( errStrs[ "noScriptName" ] )
        sys.exit( 1 )
    elif argv[ 0 ] == "-h" or argv[ 0 ] == "--help":
        print( usageStrs[ "yt" ] )
        sys.exit()
    elif argv[ 0 ] == "new-proj":
        return NewProjScript()
    elif argv[ 0 ] == "transcode-proj":
        return TranscodeProjScript()
    else:
        print( errStrs[ "whichScriptUnrecognizedArg" ] )
        sys.exit( 1 )


def main( argv ):
    script = whichScript( argv )
    script.parseOpts( argv[ 1 : ] )
    script.execScript()

if __name__ == "__main__":
    main( sys.argv[ 1 : ] )
