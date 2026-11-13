#!/usr/bin/env python3
"""Fetch and verify the official PS4-HEN main-184 file before serving anything.

This script NEVER executes HEN or the PS4 exploit. An existing invalid file is
left untouched (not used), and a failed download is never installed.
"""
import hashlib
import os
from pathlib import Path
import sys
import urllib.request

OFFICIAL_RELEASE = 'https://github.com/Scene-Collective/ps4-hen/releases/tag/pre-release-main-184'
OFFICIAL_ASSET = 'https://github.com/Scene-Collective/ps4-hen/releases/download/pre-release-main-184/hen.bin'
EXPECTED_SHA256 = '44af7f94709355bc5c7b9cef78e83d83583d04be6b151d5f4eec683d4163fffb'
EXPECTED_SIZE = 501152
DEST = Path(__file__).resolve().parent / 'hen1402_184.bin'

def validate(data):
    return len(data) == EXPECTED_SIZE and hashlib.sha256(data).hexdigest() == EXPECTED_SHA256 and data[:1] == b'\xe9'

def explain_manual_download():
    print('')
    print('MANUAL FIX (on the Windows PC):')
    print('  1. Open: ' + OFFICIAL_RELEASE)
    print('  2. Under Assets download hen.bin (from release pre-release-main-184).')
    print('  3. Rename it to hen1402_184.bin and put it here:')
    print('     ' + str(DEST))
    print('  4. Re-run START_HEN_1402_EXPERIMENTAL.bat.')
    print('  Expected size: 501152 bytes')
    print('  Expected SHA-256: ' + EXPECTED_SHA256)
    print('  Do NOT use the older hen.bin included in previous Akatsuki ZIPs.')
    print('')

def ensure_hen184(allow_download=True):
    if DEST.is_file():
        raw=DEST.read_bytes()
        if validate(raw):
            print('[PASS] Official 14.02 HEN184 verified on disk: ' + DEST.name)
            return True
        print('[FAIL] Found hen1402_184.bin, but its size, SHA-256 or format is incorrect.')
        print('  Found size: ' + str(len(raw)))
        print('  Found SHA-256: ' + hashlib.sha256(raw).hexdigest())
        explain_manual_download()
        return False
    print('[INFO] hen1402_184.bin is missing; the Lite ZIP intentionally does not contain it.')
    if not allow_download or os.environ.get('AKATSUKI_SKIP_DOWNLOAD') == '1':
        explain_manual_download()
        return False
    print('[INFO] Downloading the official HEN184 asset from GitHub...')
    try:
        req=urllib.request.Request(OFFICIAL_ASSET,headers={
            'User-Agent':'Mozilla/5.0 (compatible; AkatsukiHEN184-VerifiedAsset/2.0)',
            'Accept':'application/octet-stream',
        })
        with urllib.request.urlopen(req,timeout=30) as response:
            raw=response.read(EXPECTED_SIZE+1)
    except Exception as exc:
        print('[FAIL] Official GitHub download failed: ' + str(exc))
        explain_manual_download()
        return False
    if not validate(raw):
        print('[FAIL] Download did NOT match the official HEN184 digest. File was NOT saved.')
        print('  Downloaded size: '+str(len(raw)))
        print('  Downloaded SHA-256: '+hashlib.sha256(raw).hexdigest())
        explain_manual_download()
        return False
    temp=DEST.with_name('hen1402_184.bin.tmp')
    try:
        temp.write_bytes(raw)
        temp.replace(DEST)
    finally:
        if temp.exists(): temp.unlink()
    print('[PASS] Downloaded, installed and SHA-256 verified '+str(DEST))
    return True

if __name__=='__main__':
    sys.exit(0 if ensure_hen184() else 2)
