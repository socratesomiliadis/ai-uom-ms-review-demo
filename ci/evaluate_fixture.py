"""Compose a complete candidate from a teaching source fixture, then evaluate it."""
from pathlib import Path
import argparse,shutil,subprocess,sys,tempfile
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--fixture',required=True)
parser.add_argument('--trusted',required=True)
parser.add_argument('--out',required=True)
parser.add_argument('--mode',choices=['legacy','acceptance'],default='acceptance')
args=parser.parse_args()
trusted=Path(args.trusted).resolve();out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
candidate=Path(tempfile.mkdtemp(prefix='fixture-',dir=out))
ignore=shutil.ignore_patterns('.git','target','reports','.eval-work','__pycache__')
shutil.copytree(trusted,candidate,dirs_exist_ok=True,ignore=ignore)
shutil.copytree(Path(args.fixture).resolve(),candidate,dirs_exist_ok=True,ignore=ignore)
result=subprocess.run([sys.executable,str(trusted/'ci/evaluate.py'),'--candidate',str(candidate),'--trusted',str(trusted),'--mode',args.mode,'--out',str(out/'evaluation')])
sys.exit(result.returncode)
