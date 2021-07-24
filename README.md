# ignition-auto-trace
A python script that will automatically add trace loggers to any ignition project

The script will take any script with pre-existing functions like so:
```
def myFunction(param1, param2, param3, **param4):
  return foo
  
def mySecondFunction(example="TEST"):
  return example
```

and automatically add everything necessary to handle trace logging throughout.

```
logger = system.util.getLogger("my

def myFunction(param1, param2, **args):
  logger.trace("Folder.Script.myFunction(param1=%s, param2=%s, args=%s)" % (param1, param2, args))
  return foo
  
def mySecondFunction(example="TEST"):
  logger.trace("Folder.Script.mySecondFunction(example=%s)" % (example))
  return example
```
