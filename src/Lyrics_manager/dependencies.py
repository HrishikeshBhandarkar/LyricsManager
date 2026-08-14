import sys
import subprocess
import importlib.util
from pathlib import Path

# Core required libraries for basic Lyric Manager functionality
CORE_DEPENDENCIES = [
    {"name": "rich", "package": "rich>=13.0.0", "desc": "Terminal UI, tables, panels & progress bars", "critical": True},
    {"name": "prompt_toolkit", "package": "prompt_toolkit>=3.0.0", "desc": "Interactive shell autocomplete & suggestions", "critical": True},
    {"name": "click", "package": "click>=8.0.0", "desc": "Command-line interface & argument parser", "critical": True},
    {"name": "mutagen", "package": "mutagen>=1.47.0", "desc": "Universal audio metadata tag reader & embedder", "critical": True},
    {"name": "requests", "package": "requests>=2.31.0", "desc": "HTTP client for querying lyric web APIs", "critical": True},
    {"name": "syncedlyrics", "package": "syncedlyrics", "desc": "Fallback provider for line-synced lyrics", "critical": False},
]

# AI Neural Network dependencies (WhisperX & Demucs)
AI_DEPENDENCIES = [
    {"name": "torch", "package": "torch", "desc": "PyTorch deep learning tensor engine"},
    {"name": "torchaudio", "package": "torchaudio", "desc": "PyTorch audio processing library"},
    {"name": "whisperx", "package": "whisperx", "desc": "Whisper ASR & Wav2Vec2 phonetic forced aligner"},
    {"name": "demucs", "package": "demucs", "desc": "Hybrid Transformer neural vocal separation"},
]


def is_installed(module_name: str) -> bool:
    """Checks if a python module is importable in the current environment."""
    return importlib.util.find_spec(module_name) is not None


def install_package(package_str: str) -> bool:
    """Installs a python package via pip in a subprocess."""
    try:
        cmd = [sys.executable, "-m", "pip", "install", package_str]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Could not install {package_str}: {e}")
        return False


def check_core_dependencies() -> bool:
    """
    Checks core dependencies on startup.
    Prompts the user with a clean UI for consent before downloading any missing package.
    """
    missing_core = [dep for dep in CORE_DEPENDENCIES if not is_installed(dep["name"])]
    if not missing_core:
        return True

    print("\n" + "=" * 65)
    print("       LYRIC MANAGER — DEPENDENCY CHECK")
    print("=" * 65)
    print("Lyric Manager detected missing core Python libraries:\n")

    for idx, dep in enumerate(missing_core, start=1):
        crit_tag = "[Required]" if dep["critical"] else "[Optional]"
        print(f"  {idx}. {dep['name']} {crit_tag} — {dep['desc']}")

    print("\n" + "-" * 65)

    for dep in missing_core:
        ans = input(f"Would you like to install '{dep['name']}' now? (y/n) [y]: ").strip().lower()
        if ans not in ["n", "no"]:
            print(f">> Installing {dep['package']} via pip...")
            success = install_package(dep["package"])
            if success:
                print(f"✔ Successfully installed {dep['name']}!")
            else:
                print(f"✖ Failed to install {dep['name']}. You can install it manually: pip install {dep['package']}")
                if dep["critical"]:
                    return False
        else:
            print(f">> Skipped '{dep['name']}'.")
            if dep["critical"]:
                print(f"[!] Warning: '{dep['name']}' is a required core library.")

    print("=" * 65 + "\n")
    return True


def prompt_ai_setup_consent() -> bool:
    """
    Prompts user for explicit consent before installing heavy AI neural models/packages.
    Connects to setup.py or installs PyTorch, WhisperX, and Demucs.
    """
    missing_ai = [dep for dep in AI_DEPENDENCIES if not is_installed(dep["name"])]
    if not missing_ai:
        return True

    print("\n" + "=" * 65)
    print("       AI FORCED ALIGNMENT ENGINE — SETUP REQUIRED")
    print("=" * 65)
    print("AI-powered vocal separation & forced alignment requires deep learning")
    print("neural libraries (PyTorch, WhisperX, Demucs).\n")
    print("Missing AI modules:")
    for dep in missing_ai:
        print(f"  ◆ {dep['name']} — {dep['desc']}")

    print("\n" + "-" * 65)
    ans = input("Do you want to enable the AI Engine and install these packages now? (y/n) [y]: ").strip().lower()

    if ans in ["n", "no"]:
        print("\n>> AI setup skipped. Standard Web API lyric fetching will remain active.")
        return False

    print("\n>> Starting AI Environment Installation (this may take a few minutes)...")
    
    root_dir = Path(__file__).resolve().parent.parent.parent
    setup_file = root_dir / "setup.py"
    
    # If setup.py exists in project root, run pip install -e .
    if setup_file.exists():
        print(">> Running setup.py via pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", str(root_dir)])

    # Install individual missing AI packages
    for dep in missing_ai:
        print(f">> Installing {dep['name']}...")
        install_package(dep["package"])

    print("\n✔ AI Environment setup completed!\n" + "=" * 65 + "\n")
    return True


if __name__ == "__main__":
    check_core_dependencies()
