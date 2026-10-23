# MoCapAnything V2 - One-Click Installer (PixelArtistry)

Runs the [MoCapAnything V2](https://github.com/phongdaot/MocapAnything) web demo locally on your own PC: **video in, animation out**, for 72 animal, creature and object characters (dragon, T-rex, raptor, spider, horse, elephant, crab ...), plus the **Dance Anything** tab that keeps the music.

Don't want to install anything? Try the free browser demo first: [huggingface.co/spaces/kehong/MoCapAnythingV2](https://huggingface.co/spaces/kehong/MoCapAnythingV2).

## Install

### Windows

1. On this page: **Code → Download ZIP**, and unzip it anywhere with ~20 GB free (a short path like `C:\AI\` is best).
2. Double-click `Install_MoCapAnything.bat`.
3. When it's done, double-click `Run_MoCapAnything.bat`. Your browser opens at http://127.0.0.1:7860 once the models are loaded (the first start takes a few minutes).

### Linux / macOS

```bash
./install.sh
./run.sh
```

### What the installer does

- Installs [uv](https://github.com/astral-sh/uv) if you don't have it, and creates its own Python 3.11 environment. Nothing touches your system Python or ComfyUI.
- Downloads the MoCapAnything repo (with git if you have it, otherwise as a ZIP).
- Installs PyTorch 2.9 with CUDA 12.8 on NVIDIA GPUs (RTX 30/40/50 series), otherwise the CPU build.
- Installs the demo packages.
- Pre-downloads the V2 weights, the official example videos and characters (~1.7 GB), and the helper models (DINOv2, BRIA RMBG-1.4, SAM 2.1), so the first start doesn't stall.
- Writes the `Run_MoCapAnything` launcher.
- Safe to re-run: the repo and the environment are reused, finished downloads are skipped.

**Requirements:** Windows 10/11 (or Linux/macOS), NVIDIA GPU recommended, ~20 GB free disk, internet for the first install.

## Using it

- **Mocap · Retarget tab:** pick an example or drop your own video, choose the target character, click Run.
- **Dance Anything tab:** drop a dance video with music, click the dancer, pick a character, click Run. The audio is put back on the result.
- **Downloads:** BVH, NPY and GLB, plus a side-by-side share clip. In Blender: File → Import → Motion Capture (.bvh), or import the GLB.

## Notes

- Without an NVIDIA GPU it runs on the CPU, which works but is slow. macOS always runs on the CPU.
- On Windows the optional Blender "photoreal" render is turned off (upstream uses a bash script for it). You still get the skeleton and 3D mesh preview and all the downloads.
- The demo only retargets onto its 72 built-in characters. Your own rigged character needs the separate custom-rig pipeline in the upstream repo (`examples/custom_rig/`), which needs Blender.
- `transformers` is pinned to 5.10.4 because the version upstream pins (5.10.0) was pulled from PyPI.

## License

> [!IMPORTANT]
> - **My files in this repo** (the installer scripts and this README): [MIT](LICENSE).
> - **MoCapAnything code and V2 weights:** MIT, by the [MoCapAnything authors](https://github.com/phongdaot/MocapAnything).
> - **BRIA RMBG-1.4** (background removal), **DINOv2**, **SAM 2** and the **example data** keep their own terms. The example data is for research use and its source footage keeps its original licences. Check them before commercial use. This is not legal advice.

## Credits

[MoCapAnything V2](https://animotionlab.github.io/MoCapAnythingV2/) ([paper](https://arxiv.org/abs/2604.28130)), SIGGRAPH Asia 2026. All credit for the model goes to its authors. This repo only makes it easier to install.

## PixelArtistry

- YouTube: [youtube.com/@PixelArtistry_](https://www.youtube.com/@PixelArtistry_)
- FutureFrames newsletter: [go.pixel-artistry.com/newsletter](https://go.pixel-artistry.com/newsletter)
