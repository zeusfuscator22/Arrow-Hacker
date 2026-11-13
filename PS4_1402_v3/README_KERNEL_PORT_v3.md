# Akatsuki 14.02 - Clean Kernel Port v3 (EXPERIMENTAL)

**Goal:** Attempt to start official Scene-Collective HEN184 through Akatsuki on PS4 14.02.
**Status:** built and statically verified, NOT tested on a PS4. A full system freeze is still possible.

## What new files changed

The user-supplied `14.02 Webkit Code Execution.zip` contains four ELF binaries. These are **firmware reference images**, NOT .js payloads or files that can be swapped into a PS4 browser page. None is copied over the console's firmware.

- `1402k.elf`: supplied 14.02 kernel image, used to derive 15 patch RVAs and pristine bytes. The previous Akatsuki kernel ELF has 15 already-patched sites and cannot serve as a clean baseline.
- `libSceLibcInternal.sprx`: all 14 expected code gadget signatures validate, so their known offsets are unchanged.
- `libSceNKWebKit.sprx`: byte-for-byte identical to user's earlier 14.00 browser engine. This does not establish independent 14.02 provenance.
- `libkernel_web.sprx`: small update vs user's earlier library; runtime thread entry previously resolved to libkernel+0x194d0. Module is used for offline comparison, not reloaded into PS4.

## Code changes

1. Replaces 15 legacy 14.00 kernel patch RVAs with firmware-14.02 candidates matched to the new unmodified ELF. The changes include `memcpy` `0x2BD85D` => `0x2BDB5D` and `dlsym` offsets shifted +0x220.
2. Removes the heuristic scan that could relocate a patch to the first nearby `0x75` (the new `memcpy` branch is `0x76`).
3. Adds **fail-closed 15-site byte verification** after opening the kernel interface, before the 15 writes: if any address has neither its expected original instruction bytes nor the known replacement bytes, the patch pass is refused.
4. Removes the unverified runtime debug-menu/RCMgr kernel modifications (they aren't required for starting HEN).
5. Retains the Windows HEN184 downloader, its SHA256 checks, manual-launch behavior, and no-store web serving.
6. Ships no large ELF firmware images; the 14.02 reference values and their hashes are in `14.02_REFERENCE_MANIFEST.json`.

## Run

1. Completely close ALL earlier Akatsuki host windows to free port 8000.
2. Extract this ZIP (do not run BAT from inside ZIP). Run `START_HEN_1402_EXPERIMENTAL.bat`.
3. It downloads/verifies official 14.02 HEN184 automatically. Wait for `[PASS]` and follow **only the newly printed PS4 URL**.
4. The console may freeze; no successful HEN start is guaranteed. Do not run this on a console with data you cannot restore.
5. If you still have `14.02 Webkit Code Execution.zip`, place it beside `AUDIT_1402_REFERENCE.bat` and use that optional batch file to check fingerprints and the patch table **offline**. It never connects to the console.

## Boundaries

- A 14.02 kernel ELF and matching gadget signatures do not prove Akatsuki's earlier kernel exploit, bootstrap, or native HEN initialization are valid on a retail 14.02 PS4.
- The patch site labels come from the 14.00 upstream patch list and were relocated using neighboring code/14.02 baseline bytes. No hardware validation. In particular, some unconditional-jump replacements change control flow and may conflict with HEN184's internal patching.
- The 14.02 module origin is not independently authenticated. Do not describe this as a stable jailbreak.
- The original kernel stage performs code execution and other writes before the new 15-site guard runs; the guard is **not** a blanket guarantee against kernel freezes.
- This does not enable PSN login or online play.

## Official HEN184

https://github.com/Scene-Collective/ps4-hen/releases/tag/pre-release-main-184

Expected `hen.bin` size: 501152; SHA256: `44af7f94709355bc5c7b9cef78e83d83583d04be6b151d5f4eec683d4163fffb`.
