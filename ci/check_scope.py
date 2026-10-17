"""Reject candidate changes outside the lab contract. Not a security boundary."""
import subprocess,sys
from pathlib import PurePosixPath
candidate,base=sys.argv[1:3]
changes=subprocess.check_output(['git','-C',candidate,'diff','--name-only','-z',base,'HEAD'],text=True).split('\0')
bad=[]
for name in filter(None,changes):
    allowed=(name=='src/main/java/edu/ai/PriceCalculator.java'
             or (name.startswith('submissions/') and name.endswith('.md'))
             or (name.startswith('src/test/java/') and name.endswith('.java')))
    if not allowed: bad.append(name)
if bad: print('OUT OF SCOPE: '+', '.join(bad)); sys.exit(1)
print('Scope PASS')
