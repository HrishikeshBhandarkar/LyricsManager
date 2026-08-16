#!/usr/bin/env python3
"""
Lyric Manager - Uninstaller Script
Safely uninstalls lyric-manager, removes console scripts, cleans up caches,
and optionally uninstalls dependencies.
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ANSI Color Codes for terminal styling
COLOR_CYAN = "\033[96m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_BOLD = "\033[1m"
COLOR_DIM = "\033[2m"
COLOR_RESET = "\033[0m"


def print_banner():
    banner = f"""{COLOR_CYAN}{COLOR_BOLD}
============================================================
              LYRIC MANAGER — UNINSTALLER
============================================================{COLOR_RESET}"""
    print(banner)


def run_cmd(cmd_list, desc=None):
    """Runs a subprocess command with clean output handling."""
    if desc:
        print(f"{COLOR_CYAN}>> {desc}...{COLOR_RESET}")
    try:
        res = subprocess.run(cmd_list, capture_output=True, text=True, errors="replace")
        return res.returncode == 0, res.stdout, res.stderr
    except Exception as e:
        return False, "", str(e)


def uninstall_pip_packages(packages):
    """Uninstalls a list of packages via pip."""
    for pkg in packages:
        print(f"  Removing {COLOR_BOLD}{pkg}{COLOR_RESET}...", end=" ", flush=True)
        cmd = [sys.executable, "-m", "pip", "uninstall", "-y", pkg]
        success, stdout, stderr = run_cmd(cmd)
        if success or "not installed" in stderr.lower() or "not installed" in stdout.lower() or "skipping" in stdout.lower():
            print(f"{COLOR_GREEN}[DONE]{COLOR_RESET}")
        else:
            print(f"{COLOR_YELLOW}[SKIPPED / NOT FOUND]{COLOR_RESET}")


def clean_local_artifacts(project_root: Path, remove_config=False, remove_cache=True):
    """Cleans up .egg-info, build artifacts, __pycache__, and optional configs."""
    print(f"\n{COLOR_CYAN}>> Cleaning up project artifacts and caches...{COLOR_RESET}")
    
    cleaned_items = 0

    # 1. Egg-info and build directories
    for item in project_root.rglob("*.egg-info"):
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
            cleaned_items += 1
    
    for dir_name in ["build", "dist", ".pytest_cache"]:
        target = project_root / dir_name
        if target.exists() and target.is_dir():
            shutil.rmtree(target, ignore_errors=True)
            cleaned_items += 1

    # 2. Pycache
    for pycache in project_root.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache, ignore_errors=True)
            cleaned_items += 1

    # 3. Decryption token cache
    if remove_cache:
        qq_cache = project_root / "src" / "Lyrics_manager" / "providers" / ".qq_des_cache"
        if qq_cache.exists():
            shutil.rmtree(qq_cache, ignore_errors=True)
            cleaned_items += 1

    # 4. User config file (optional)
    if remove_config:
        config_file = project_root / "config.json"
        if config_file.exists():
            try:
                config_file.unlink()
                print(f"  Removed {COLOR_BOLD}config.json{COLOR_RESET}")
                cleaned_items += 1
            except Exception:
                pass

    print(f"  {COLOR_GREEN}[OK] Cleaned {cleaned_items} temporary/cache directory entries.{COLOR_RESET}")


def verify_uninstallation():
    """Checks if lyric_manager is still importable or registered."""
    print(f"\n{COLOR_CYAN}>> Verifying uninstallation...{COLOR_RESET}")
    cmd = [sys.executable, "-m", "pip", "show", "lyric-manager"]
    success, stdout, _ = run_cmd(cmd)
    if not success or not stdout.strip():
        print(f"  {COLOR_GREEN}[OK] lyric-manager package is successfully uninstalled.{COLOR_RESET}")
    else:
        print(f"  {COLOR_YELLOW}[!] Package still listed in pip. You can manually run: pip uninstall -y lyric-manager{COLOR_RESET}")


def main():
    parser = argparse.ArgumentParser(description="Uninstall Lyric Manager")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation and run standard uninstall")
    parser.add_argument("--full", action="store_true", help="Perform a full uninstall including provider dependencies")
    parser.add_argument("--purge", action="store_true", help="Purge everything including configurations and caches")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent

    print_banner()

    mode = "standard"
    if args.purge:
        mode = "purge"
    elif args.full:
        mode = "full"
    elif not args.yes:
        print(f"\n{COLOR_BOLD}Choose an uninstallation mode:{COLOR_RESET}\n")
        print(f"  {COLOR_BOLD}[1] Standard Uninstall (Recommended){COLOR_RESET}")
        print(f"      * Uninstalls 'lyric-manager' and CLI console commands.")
        print(f"      * Cleans build directories and pycache.")
        print(f"      * Keeps shared Python libraries (rich, mutagen, requests, torch, etc.).\n")
        
        print(f"  {COLOR_BOLD}[2] Clean Uninstall{COLOR_RESET}")
        print(f"      * Uninstalls 'lyric-manager' and standalone provider libraries (syncedlyrics).")
        print(f"      * Cleans all build artifacts and provider token caches.")
        print(f"      * Keeps configuration file and heavy libraries (torch, etc.).\n")

        print(f"  {COLOR_BOLD}[3] Purge Everything (Complete Wipe){COLOR_RESET}")
        print(f"      * Uninstalls 'lyric-manager' + provider packages.")
        print(f"      * Deletes 'config.json' and all cached data.\n")

        print(f"  {COLOR_BOLD}[4] Cancel / Exit{COLOR_RESET}\n")

        try:
            choice = input(f"{COLOR_BOLD}Enter choice [1-4] (default: 1): {COLOR_RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{COLOR_YELLOW}Uninstallation cancelled.{COLOR_RESET}")
            sys.exit(0)

        if choice in ["4", "q", "exit", "cancel"]:
            print(f"\n{COLOR_YELLOW}Uninstallation cancelled. No changes were made.{COLOR_RESET}")
            sys.exit(0)
        elif choice == "2":
            mode = "full"
        elif choice == "3":
            mode = "purge"
        else:
            mode = "standard"

    print("\n" + "=" * 60)
    print(f"  Executing {COLOR_BOLD}{mode.upper()}{COLOR_RESET} uninstallation...")
    print("=" * 60 + "\n")

    # Step 1: Uninstall primary package
    uninstall_pip_packages(["lyric-manager", "lyric_manager"])

    # Step 2: Uninstall optional / extra packages based on mode
    if mode in ["full", "purge"]:
        uninstall_pip_packages(["syncedlyrics"])
        
        if mode == "purge":
            # Optional prompt for heavy AI packages
            if not args.yes:
                try:
                    rm_ai = input(f"\nDo you also want to uninstall heavy AI packages (whisperx, demucs)? (y/n) [n]: ").strip().lower()
                except (KeyboardInterrupt, EOFError):
                    rm_ai = "n"
                if rm_ai in ["y", "yes"]:
                    uninstall_pip_packages(["whisperx", "demucs"])

    # Step 3: Clean artifacts and caches
    remove_cfg = (mode == "purge")
    clean_local_artifacts(project_root, remove_config=remove_cfg, remove_cache=True)

    # Step 4: Verify
    verify_uninstallation()

    print("\n" + "=" * 60)
    print(f"{COLOR_GREEN}{COLOR_BOLD}[DONE] Uninstallation process complete!{COLOR_RESET}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
