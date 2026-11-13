# Akatsuki 14.02 + HEN184 - HTTP 404 host fix

**Status: experimental; this fixes missing-asset startup errors only, not console stability.**

## Why the last Lite build produced HTTP 404
The Lite ZIP excluded the official HEN binary. Its `serve.bat`, `14.02 Jailbreak.bat`, and `serve.sh` could start a host without first running `prepare_hen184.py`. The browser then requested `/hen1402_184.bin` and received 404. An *older still-running server* on the same port could produce the same symptom.

## Fixed
- All Windows launchers route through the verified startup script.
- `server.py` refuses to start unless the official release asset exists and matches its **size, SHA-256, and raw payload signature**; the server itself can attempt the download if started directly.
- `serve.sh` uses the guarded, authenticated Python server.
- If port 8000 is occupied, an explicit message tells you how to switch ports.
- Downloads are verified before saving and are never accepted on a hash mismatch.

## Run on Windows
1. **Close previous Akatsuki / Afterglow server windows**, otherwise your PS4 might talk to an old server.
2. Extract the entire ZIP. Run `START_HEN_1402_EXPERIMENTAL.bat`.
3. If automatic download succeeds, the script prints `[PASS]` and starts the server. Use **only the new PS4 URL printed** by that window.
4. If GitHub is blocked, the script **will not start a server**. Open the official release page below on your Windows PC. Under *Assets*, download `hen.bin`, rename it to `hen1402_184.bin`, and place it **in the same folder as `server.py` and `prepare_hen184.py`**. Run the BAT again.
5. If port 8000 is occupied, run this at Command Prompt in the extracted folder: `START_HEN_1402_EXPERIMENTAL.bat 8765`, and use its printed URL.
6. **Don't run the exploit if the console hasn't been backed up.** The 14.02 Akatsuki kernel-stage patches are still unverified and could cause another freeze.

## Official release
https://github.com/Scene-Collective/ps4-hen/releases/tag/pre-release-main-184

Expected asset name: `hen.bin` (rename locally to `hen1402_184.bin`)

Expected size: **501152 bytes**

Expected SHA-256: `44af7f94709355bc5c7b9cef78e83d83583d04be6b151d5f4eec683d4163fffb`

Do not use the `hen.bin` from your original Akatsuki archive (500448 bytes). It is a different build.

## What this build does NOT fix
- The unverified 14.02 WebKit and kernel patch offsets.
- Potential incompatibilities or freezes when the PS4 payload executes.
- PSN access or authentication.

The Lite archive does **not** bundle the official HEN184 executable; it only fetches/verifies it on the PC. It cannot be considered an already-tested 14.02 jailbreak.
