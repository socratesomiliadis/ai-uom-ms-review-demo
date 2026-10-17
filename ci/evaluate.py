"""Educational evaluator. Execute trusted tooling; overlay one candidate source file."""
from pathlib import Path
import argparse, subprocess, shutil, sys, json, time, os, xml.etree.ElementTree as ET

p=argparse.ArgumentParser()
p.add_argument('--candidate',required=True)
p.add_argument('--trusted',required=True)
p.add_argument('--mode',choices=['legacy','acceptance'],default='acceptance')
p.add_argument('--out',default='reports')
a=p.parse_args()
candidate=Path(a.candidate).resolve(); trusted=Path(a.trusted).resolve(); out=Path(a.out).resolve()
out.mkdir(parents=True,exist_ok=True)
# Each execution uses a fresh directory; no recursive deletion of user paths.
import tempfile
run=Path(tempfile.mkdtemp(prefix='eval-',dir=out))
for item in ['pom.xml','mvnw','mvnw.cmd','.mvn','src']:
    src=trusted/item; dst=run/item
    if src.is_dir(): shutil.copytree(src,dst)
    else: shutil.copy2(src,dst)
source=Path('src/main/java/edu/ai/PriceCalculator.java')
shutil.copy2(candidate/source,run/source)
if a.mode == 'acceptance':
    shutil.copytree(trusted/'evaluation/src/test/java',run/'src/test/java',dirs_exist_ok=True)
if sys.platform == 'win32': command=['cmd','/d','/c','mvnw.cmd','-B','-ntp','test']
else:
    (run/'mvnw').chmod(0o755)
    command=['./mvnw','-B','-ntp','test']
started=time.monotonic()
try:
    result=subprocess.run(command,cwd=run,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',timeout=300)
    returncode=result.returncode; log=result.stdout
except subprocess.TimeoutExpired as e:
    returncode=124; log='TIMEOUT: evaluation exceeded 300 seconds.\n'+str(e.stdout or '')
(out/'build.log').write_text(log,encoding='utf-8')
junit=out/'junit'; junit.mkdir(exist_ok=True)
for stale in junit.glob('TEST-*.xml'): stale.unlink()
counts=dict(tests=0,failures=0,errors=0,skipped=0)
failures=[]
for report in (run/'target/surefire-reports').glob('TEST-*.xml'):
    shutil.copy2(report,junit/report.name)
    tree=ET.parse(report).getroot()
    for k in counts: counts[k]+=int(tree.attrib.get(k,0))
    for case in tree.findall('testcase'):
        for kind in ['failure','error']:
            f=case.find(kind)
            if f is not None: failures.append(dict(test=case.attrib.get('name'),kind=kind,message=f.attrib.get('message','')))
passed=returncode==0 and counts['tests']>0 and not any(counts[k] for k in ['failures','errors','skipped'])
report=dict(mode=a.mode,status='PASS' if passed else 'FAIL',seconds=round(time.monotonic()-started,3),exit_code=returncode,**counts,failed_checks=failures)
for label,path in [('tested_checkout_sha',candidate),('trusted_policy_sha',trusted)]:
    try: report[label]=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError: report[label]=None
report['pr_head_sha']=os.environ.get('PR_HEAD_SHA')
report['source_sha256']=__import__('hashlib').sha256((candidate/source).read_bytes()).hexdigest()
(out/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if not passed: print('Read '+str(out/'build.log')+' for compiler errors or test failures.')
sys.exit(0 if passed else 1)
