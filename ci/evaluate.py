"""Evaluate a complete candidate project against an independent acceptance contract."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,time
import xml.etree.ElementTree as ET

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--candidate',required=True)
parser.add_argument('--trusted',required=True)
parser.add_argument('--mode',choices=['legacy','acceptance'],default='acceptance')
parser.add_argument('--out',default='reports')
args=parser.parse_args()
candidate=Path(args.candidate).resolve();trusted=Path(args.trusted).resolve();out=Path(args.out).resolve()
out.mkdir(parents=True,exist_ok=True)
run=Path(tempfile.mkdtemp(prefix='eval-',dir=out))
# These are generated/runtime directories, not editable project paths.
generated={'.git','target','node_modules','reports','.eval-work','__pycache__'}
def ignore(directory,names):
    return [name for name in names if name in generated or (Path(directory)/name).resolve().is_relative_to(out)]
shutil.copytree(candidate,run,dirs_exist_ok=True,ignore=ignore)
# Candidate source, resources, build and tests stay together. The two harness
# suites are supplied independently from the agreed contract for this run.
test_root=run/'src/test/java'
if args.mode=='acceptance':
    shutil.copytree(trusted/'src/test/java',test_root,dirs_exist_ok=True)
    shutil.copytree(trusted/'evaluation/src/test/java',test_root,dirs_exist_ok=True)
required=json.loads((trusted/'evaluation/required-tests.json').read_text(encoding='utf-8'))
required={tuple(case) for case in required[args.mode]}
files={path.relative_to(candidate).as_posix():hashlib.sha256(path.read_bytes()).hexdigest()
       for path in sorted(candidate.rglob('*')) if path.is_file()
       and not any(part in generated for part in path.relative_to(candidate).parts)
       and not path.resolve().is_relative_to(out)}
project_hash=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
started=time.monotonic()
command=['cmd','/d','/c','mvnw.cmd','-B','-ntp','clean','test'] if sys.platform=='win32' else ['./mvnw','-B','-ntp','clean','test']
try:
    if sys.platform!='win32':(run/'mvnw').chmod(0o755)
    result=subprocess.run(command,cwd=run,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',timeout=300)
    returncode=result.returncode;log=result.stdout
except subprocess.TimeoutExpired:
    returncode=124;log='TIMEOUT: evaluation exceeded 300 seconds.\n'
except OSError as error:
    returncode=1;log='Could not build the complete candidate project: '+str(error)+'\n'
(out/'build.log').write_text(log,encoding='utf-8')
junit=out/'junit';junit.mkdir(exist_ok=True)
for stale in junit.glob('TEST-*.xml'):stale.unlink()
counts=dict(tests=0,failures=0,errors=0,skipped=0)
failures=[];executed=set()
for index,path in enumerate(sorted(run.rglob('TEST-*.xml'))):
    if not path.parent.name.endswith('reports'):continue
    shutil.copy2(path,junit/f'{index:03d}-{path.name}')
    for case in ET.parse(path).getroot().iter('testcase'):
        counts['tests']+=1
        identity=(case.attrib.get('classname',''),case.attrib.get('name',''))
        executed.add(identity)
        for kind in ['failure','error','skipped']:
            detail=case.find(kind)
            if detail is not None:
                counts[{'failure':'failures','error':'errors','skipped':'skipped'}[kind]]+=1
                failures.append(dict(test=identity[1],kind=kind,message=detail.attrib.get('message','')))
missing=sorted(required-executed)
passed=returncode==0 and not missing and counts['tests']>0 and not any(counts[k] for k in ['failures','errors','skipped'])
report=dict(mode=args.mode,status='PASS' if passed else 'FAIL',seconds=round(time.monotonic()-started,3),exit_code=returncode,**counts,failed_checks=failures,
            required_tests=len(required),required_tests_observed=len(required&executed),missing_required_tests=[dict(classname=c,name=n) for c,n in missing],
            project_sha256=project_hash,candidate_file_sha256=files)
for label,path in [('tested_checkout_sha',candidate),('trusted_policy_sha',trusted)]:
    try:
        top=Path(subprocess.check_output(['git','-C',str(path),'rev-parse','--show-toplevel'],text=True,stderr=subprocess.DEVNULL).strip()).resolve()
        report[label]=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip() if top==path else None
    except subprocess.CalledProcessError:report[label]=None
report['pr_head_sha']=os.environ.get('PR_HEAD_SHA')
report['source_sha256']=files.get('src/main/java/edu/ai/PriceCalculator.java')
(out/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='candidate_file_sha256'},ensure_ascii=False,indent=2))
if not passed:print('Read '+str(out/'build.log')+' and missing_required_tests for build or contract failures.')
sys.exit(0 if passed else 1)
