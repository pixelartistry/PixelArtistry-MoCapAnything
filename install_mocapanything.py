#!/usr/bin/env python3
"""
MoCapAnything V2 - one-click local installer (PixelArtistry)

What it does
  1. Downloads the MoCapAnything repo (no git needed)
  2. Creates an isolated Python 3.11 environment with uv
  3. Installs PyTorch (CUDA 12.8 for NVIDIA RTX 30/40/50, CPU otherwise) + the demo dependencies
  4. Pre-downloads the model weights and the official example data from Hugging Face
  5. Writes a "Run MoCapAnything" launcher next to this script

Upstream project: https://github.com/phongdaot/MocapAnything  (code + V2 weights: MIT)
Run it via "Install_MoCapAnything.bat" (Windows) or "install.sh" (Linux/macOS).
Only uses the Python standard library, so it runs before anything else is installed.
"""
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.join(ROOT, "MocapAnything")
VENV = os.path.join(REPO_DIR, ".venv")
REPO_GIT = "https://github.com/phongdaot/MocapAnything.git"
REPO_ZIP = "https://github.com/phongdaot/MocapAnything/archive/refs/heads/main.zip"
PYTHON_VERSION = "3.11"
IS_WIN = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"

TORCH = ["torch==2.9.0", "torchvision==0.24.0"]
# Minimal demo stack (from the repo's RUN.md quick start) + what demo/app.py imports.
DEPS = [
    "numpy==1.26.4", "opencv-python==4.11.0.86", "pillow", "matplotlib", "scipy",
    "scikit-image", "trimesh==4.9.0", "roma==1.5.4", "pyyaml", "tqdm",
    "huggingface_hub", "hf_xet", "transformers==5.10.4", "diffusers==0.38.0",
    "safetensors", "accelerate", "gradio", "imageio", "imageio-ffmpeg", "pygltflib",
]


def step(msg):
    print(f"\n=== {msg} ===", flush=True)


def run(cmd, **kw):
    print("  > " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, **kw)


def find_uv():
    uv = shutil.which("uv")
    if uv:
        return uv
    home = os.path.expanduser("~")
    for p in (os.path.join(home, ".local", "bin", "uv.exe" if IS_WIN else "uv"),
              os.path.join(home, ".cargo", "bin", "uv.exe" if IS_WIN else "uv")):
        if os.path.exists(p):
            return p
    sys.exit("uv not found. Start the installer through Install_MoCapAnything.bat / install.sh.")


def has_nvidia():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
                             capture_output=True, text=True, timeout=20)
        if out.returncode == 0 and out.stdout.strip():
            print("  GPU: " + out.stdout.strip().splitlines()[0])
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return False


def venv_python():
    return os.path.join(VENV, "Scripts", "python.exe") if IS_WIN else os.path.join(VENV, "bin", "python")


def download_repo():
    if os.path.exists(os.path.join(REPO_DIR, "demo", "app.py")):
        print("  Repo already there - skipping download.")
        return
    if shutil.which("git"):  # git available -> clone (easy to update later with "git pull")
        run(["git", "clone", "--depth", "1", REPO_GIT, REPO_DIR])
        return
    zip_path = os.path.join(ROOT, "mocapanything_main.zip")
    print(f"  Downloading {REPO_ZIP}")
    urllib.request.urlretrieve(REPO_ZIP, zip_path)
    with zipfile.ZipFile(zip_path) as z:
        top = z.namelist()[0].split("/")[0]  # e.g. MocapAnything-main
        z.extractall(ROOT)
    os.replace(os.path.join(ROOT, top), REPO_DIR)
    os.remove(zip_path)


def install_env(uv):
    if not os.path.exists(venv_python()):
        run([uv, "venv", "--python", PYTHON_VERSION, VENV])
    py = ["--python", venv_python()]
    if IS_MAC:
        run([uv, "pip", "install", *py, *TORCH])
        print("  Note: on a Mac the demo runs on CPU and will be slow.")
    elif has_nvidia():
        run([uv, "pip", "install", *py, *TORCH,
             "--index-url", "https://download.pytorch.org/whl/cu128"])
    else:
        print("  No NVIDIA GPU found - installing the CPU build (works, but slow).")
        run([uv, "pip", "install", *py, *TORCH,
             "--index-url", "https://download.pytorch.org/whl/cpu"])
    run([uv, "pip", "install", *py, *DEPS])


def download_models():
    code = (
        "from huggingface_hub import snapshot_download\n"
        "print('  weights -> checkpoints/')\n"
        "snapshot_download('kehong/MoCapAnythingV2-weights', local_dir='checkpoints')\n"
        "print('  example videos + characters -> demo/data/ (about 1.7 GB)')\n"
        "snapshot_download('kehong/MoCapAnythingV2-data-sample', repo_type='dataset', local_dir='demo/data')\n"
        "# helper models the app would otherwise fetch on first launch (into the HF cache)\n"
        "for rid in ('facebook/dinov2-large', 'briaai/RMBG-1.4', 'facebook/sam2.1-hiera-base-plus'):\n"
        "    try:\n"
        "        print('  ' + rid); snapshot_download(rid)\n"
        "    except Exception as e:\n"
        "        print(f'  ! could not pre-download {rid} ({e.__class__.__name__}) - the app retries on first start')\n"
    )
    run([venv_python(), "-c", code], cwd=REPO_DIR)


def write_launchers():
    launcher = os.path.join(ROOT, "run_mocapanything.py")
    with open(launcher, "w", encoding="utf-8") as f:
        f.write(LAUNCHER_PY)
    if IS_WIN:
        with open(os.path.join(ROOT, "Run_MoCapAnything.bat"), "w", encoding="utf-8") as f:
            f.write('@echo off\r\ncd /d "%~dp0"\r\n'
                    '"MocapAnything\\.venv\\Scripts\\python.exe" run_mocapanything.py\r\npause\r\n')
    else:
        p = os.path.join(ROOT, "run.sh")
        with open(p, "w", encoding="utf-8") as f:
            f.write('#!/usr/bin/env bash\ncd "$(dirname "$0")"\n'
                    'MocapAnything/.venv/bin/python run_mocapanything.py\n')
        os.chmod(p, 0o755)


LAUNCHER_PY = r'''#!/usr/bin/env python3
"""Starts the MoCapAnything V2 web demo locally and opens it in the browser."""
import os, platform, subprocess, sys, threading, time, urllib.request, webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(ROOT, "MocapAnything")
PORT = os.environ.get("GRADIO_SERVER_PORT", "7860")
URL = f"http://127.0.0.1:{PORT}"

env = dict(os.environ)
env["PYTHONPATH"] = REPO + os.pathsep + os.path.join(REPO, "TripoSG")
env["APP_HOST"] = "127.0.0.1"
env["GRADIO_SERVER_PORT"] = PORT
env["PYTHONUTF8"] = "1"            # emoji in the UI/logs on Windows consoles
env["PYTHONIOENCODING"] = "utf-8"
env["GRADIO_ANALYTICS_ENABLED"] = "False"
if platform.system() == "Windows":
    # The optional Blender render uses a bash wrapper that can't run on Windows.
    # Hide Blender so the demo uses its built-in render (skeleton + mesh preview).
    env.pop("BLENDER_BIN", None)
    env["PATH"] = os.pathsep.join(p for p in env.get("PATH", "").split(os.pathsep)
                                  if "blender" not in p.lower())

def open_when_ready():
    for _ in range(900):            # first start loads models, give it up to 15 min
        try:
            urllib.request.urlopen(URL, timeout=2)
            webbrowser.open(URL)
            return
        except Exception:
            time.sleep(1)

print(f"Starting MoCapAnything V2 - the browser opens at {URL} when it's ready.")
threading.Thread(target=open_when_ready, daemon=True).start()
sys.exit(subprocess.call([sys.executable, os.path.join("demo", "app.py")], cwd=REPO, env=env))
'''


def main():
    print("MoCapAnything V2 - one-click installer (PixelArtistry)")
    print(f"Install folder: {ROOT}")
    uv = find_uv()
    step("1/4 Downloading MoCapAnything")
    download_repo()
    step("2/4 Creating Python environment + installing PyTorch and dependencies")
    install_env(uv)
    step("3/4 Downloading model weights and example data")
    download_models()
    step("4/4 Creating launcher")
    write_launchers()
    print("\nDone! Start it with " + ("Run_MoCapAnything.bat" if IS_WIN else "./run.sh"))


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(f"\nInstall failed at: {' '.join(e.cmd)}\nScroll up for the error message.")
