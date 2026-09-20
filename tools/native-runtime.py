"""Prepare the hash-pinned SDK and execute one fresh native operation session."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]

def prepare(jar):
 pin=json.loads((ROOT/'docs/toolchain.json').read_text())['engine']['sha256']
 if hashlib.sha256(jar.read_bytes()).hexdigest()!=pin:raise ValueError('Unqualified engine')
 lib=ROOT/'.cache/native/lib';lib.mkdir(parents=True,exist_ok=True)
 members=[]
 with zipfile.ZipFile(jar) as archive:
  for name in sorted(archive.namelist()):
   if name.startswith('BOOT-INF/lib/') and name.endswith('.jar'):
    target=lib/Path(name).name;data=archive.read(name)
    if not target.exists() or target.read_bytes()!=data:target.write_bytes(data)
    members.append(str(target))
 # Explicit verified members prevent unrelated cache jars entering the classpath.
 classes=ROOT/'.cache/native/classes';classes.mkdir(parents=True,exist_ok=True)
 cp=os.pathsep.join(members)
 subprocess.run(['javac','-cp',cp,'-d',str(classes),str(ROOT/'tools/java/SteadiNative.java')],check=True)
 return os.pathsep.join([str(classes),cp])

def execute(cp,inputs):
 if Path(inputs[-1]).exists():raise ValueError('Output directory must not exist; choose a fresh invocation path')
 return subprocess.run(['java','-Duser.timezone=UTC','-cp',cp,'SteadiNative',*map(str,inputs)],capture_output=True,text=True,encoding='utf-8',timeout=120)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--jar',required=True,type=Path);parser.add_argument('inputs',nargs=6);args=parser.parse_args()
 cp=prepare(args.jar);run=execute(cp,args.inputs);print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
