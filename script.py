import os
import re

myProjectPath = "Insert Ignition Directory Here"
myProjectName = "MyProject"

scriptPath = '%s/projects/%s/ignition/script-python' % (myProjectPath, myProjectName)


def checkIfFunction(line):
    return line.startswith('def ')    

def getTabs(line):
    return ''.join(["\t" for tab in range(line.rstrip().count('\t'))])

def verifyTabInsteadOfSpace(line):
    if line.startswith("    "):
        return line.replace("    ", "\t")

    return line

def getScriptPath(line, subdir):
    return subdir.replace(scriptPath, '').replace('/', '.')[1:]

def createFunctionPath(line, subdir):
    functionName = re.search('def (.*)\(', line).group(1)
    scriptFolder = getScriptPath(line, subdir)

    return "%s.%s" % (scriptFolder, functionName)

def getParameterArray(line):
    parameterString = parameterString = re.search('\((.*)\):', line).group(1)
    parameterArray = [param.split('=')[0].replace("\n", "").replace('\t', '').replace('*', '').strip() for param in parameterString.split(',')]
    if parameterArray == ['']:
        parameterArray = []

    return parameterArray

def createParameters(line):
    parameterArray = getParameterArray(line)
    parameterFormatString = ', '.join([param + "=%s" for param in parameterArray])
    parameterFormatParameters = ', '.join(parameterArray)
    return '%s)" %% (%s)' % (parameterFormatString, parameterFormatParameters)

def checkForParameters(line):
    parameterArray = getParameterArray(line)
    return len(parameterArray) > 0

def buildLogger(line, subdir):
    function = createFunctionPath(line, subdir)
    parameters = createParameters(line)

    if checkForParameters(line):
        logger = 'logger.trace("%s(%s)\n' % (function, parameters)
    else:
        logger = 'logger.trace("%s()")\n' % function

    return logger


for subdir, dirs, files in os.walk(scriptPath):
    for fileName in files:
        if fileName.endswith('.py'):
            filePath = os.path.join(subdir, fileName)

            with open(filePath, "r") as file:
                lastRowIsFunction = False
                logger = None

                data = file.readlines()

                for index, line in enumerate(data):
                    line = verifyTabInsteadOfSpace(line)

                    # Check for the logger existing, if not then create it!
                    if index == 0:
                        logger = getScriptPath(line, subdir)
                        data[index] = 'logger = system.util.getLogger("%s")\n' % logger
                        
                    # Verify we dont get duplicate loggers for no reason
                    elif line == data[0]:
                        data[index] = "\n"

                    elif checkIfFunction(line):
                        logger = buildLogger(line, subdir)
                        defTabs = getTabs(line)
                        lastRowIsFunction = True

                    elif lastRowIsFunction:
                        # Replace a line if its already a logger
                        if 'logger.trace' in line:
                            data[index] = defTabs + "\t" + logger

                        # Add a new line if no logger is present
                        else:
                            data.insert(index, defTabs + "\t" + logger)     

                        lastRowIsFunction = False
                        defTabs = None
                        logger = None    
                    else:
                        data[index] = line

            with open(filePath, 'w') as file:
                file.writelines(data)
