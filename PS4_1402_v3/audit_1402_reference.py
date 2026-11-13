#!/usr/bin/env python3
"""Offline PS4 14.02 firmware reference fingerprint and patch-byte audit."""
import hashlib, json, sys, zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
MAN=json.loads((BASE/'14.02_REFERENCE_MANIFEST.json').read_text(encoding='utf-8'))
source=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/MAN['reference_archive']
if not source.is_file():
    print('[FAIL] Could not find:', source)
    print('Place the original 14.02 Webkit Code Execution.zip beside this script or supply its full path.')
    raise SystemExit(1)
failures=[]
with zipfile.ZipFile(source) as archive:
    for filename, expected in MAN['reference_files'].items():
        names=[x for x in archive.namelist() if x.rsplit('/',1)[-1]==filename]
        if len(names)!=1:
            print('[FAIL]',filename,'missing or duplicated');failures.append(filename);continue
        data=archive.read(names[0]);digest=hashlib.sha256(data).hexdigest()
        good=len(data)==expected['bytes'] and digest==expected['sha256']
        print('[PASS]' if good else '[FAIL]',filename, 'size=',len(data),'sha256=',digest)
        if not good:failures.append(filename)
        if filename!='1402k.elf':continue
        for p in MAN['sites']:
            o=int(p['rva'],16);exp=bytes.fromhex(p['expected_unmodified'])
            if data[o:o+len(exp)]!=exp:
                failures.append(p['name']); print('  [FAIL]',p['name'],p['rva'],'expected',exp.hex(),'got',data[o:o+len(exp)].hex())
        print('  Patch reference sites:',len(MAN['sites']),'checked')
print('RESULT:', 'PASS: user-supplied ELF files match port reference' if not failures else 'FAIL: input mismatch; do not treat it as the audited firmware build')
raise SystemExit(1 if failures else 0)
