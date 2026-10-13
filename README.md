# VSFilterMod r5.3.1 Vmoe

VSFilterMod r5.3.1 with the Vmoe subtitle tags from computerfan's
`r5.2.7-beta` ported to the current Masaiki codebase.

The exact upstream commits, feature provenance, adapted files, and validation
status are recorded in [`PORTING.md`](PORTING.md).

## Vmoe tags

- `\ortho0` / `\ortho1` — perspective or orthographic projection
- `\xblur` / `\yblur` — animatable directional blur
- `\fshp` — animatable horizontal spacing
- `\blend` — additional color composition modes

The accepted textual blend modes are `over`, `add`, `sub`, `mult`, `scr` and
`diff`.

Tag documentation: [New tags in Vmoe mod](https://github.com/computerfan/VSFilterMod/wiki/New-Tags#new-tags-in-vmoe-mod)

## Building on Windows

Requirements:

- Visual Studio with Desktop development with C++
- MFC for the latest x64/x86 build tools
- Windows 10 SDK
- an installed MSVC toolset compatible with the selected Visual Studio

Run one of the included scripts:

```bat
build_x64.bat
build_x86.bat
build_all.bat
```

The scripts detect `v145`, `v143`, or `v142` from the active MSVC tools. An
explicit toolset can be supplied when more than one is installed:

```bat
build_x64.bat v143
build_all.bat v145
```

The `VSFILTERMOD_TOOLSET` environment variable is also accepted when no
argument is provided.

The resulting files are copied to:

```text
dist\x64\VSFilterMod.dll
dist\x86\VSFilterMod.dll
```

The scripts locate Visual Studio automatically and use the `Release (MOD)`
configuration. A Portuguese guide is available in
[`README_PT-BR.md`](README_PT-BR.md).

Confirmed environments are Visual Studio 2026 with `v145` locally and Visual
Studio 2022 with `v143` in GitHub Actions. The project files retain the upstream
`v142` setting, but that toolset has not been validated for this port. The CI
workflow remains fixed to `v143` for reproducibility.

Compiler warnings inherited from the legacy codebase are expected. The build
is considered successful only when the final DLL exists. Locally compiled DLLs
are not digitally signed.

To build both architectures and create a ZIP with a SHA-256 checksum, run:

```powershell
.\package_release.ps1 -Version r5.3.1-Vmoe.1
```

Use `-Toolset v143` or `-Toolset v145` to select an installed toolset. The
package is written to the dedicated `release-output` directory by default.

## VapourSynth usage

```text
vsfm.TextSubMod(clip clip, string file[, int charset=1, float fps=-1.0, string vfr='', int accurate=0])
vsfm.VobSub(clip clip, string file)
```

- `clip`: YUV420P8, YUV420P10, YUV420P16 and RGB24 are supported.
- `accurate`: set to `1` for accurate 10/16-bit rendering (slower), or `0`
  for the default mode.

The VapourSynth interface targets the API 4 (R55 and newer, required since
R80); the namespace `vsfm`, the functions and their arguments are unchanged.
A wheel for Windows x64 is attached to the GitHub releases:

```text
pip install vapoursynth_vsfiltermod-<version>-py3-none-win_amd64.whl
```

It puts `VSFilterMod.dll` into `site-packages/vapoursynth/plugins`, where
VapourSynth autoloads it. `tests/test_vsfiltermod.py` checks the formats, the
Vmoe tags and the errors against an installed wheel or a given DLL.

## MPC-BE

1. Register the matching DLL with `regsvr32.exe VSFilterMod.dll` using an
   elevated command prompt.
2. In MPC-BE, select `VSFilter/xy-VSFilter` as the subtitle renderer.

## Base projects and credits

- [Masaiki/VSFilterMod r5.3.1](https://github.com/Masaiki/VSFilterMod/tree/effb5a7a5e1aa34dc8023cd03e66acc7f6527bc1) — source base
- [computerfan/VSFilterMod r5.2.7-beta](https://github.com/computerfan/VSFilterMod/releases/tag/r5.2.7-beta) — Vmoe features
- [sorayuki/VSFilterMod](https://github.com/sorayuki/VSFilterMod)
- [teplofizik/VSFilterMod](https://github.com/teplofizik/vsfiltermod)

This repository preserves the original source notices and is distributed under
the GNU General Public License. See [`LICENSE`](LICENSE).
