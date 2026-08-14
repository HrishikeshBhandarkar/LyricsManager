import sys
import os
import time
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Fix SpeechBrain / Lightning / Pyannote k2 lazy import bug
try:
    from speechbrain.utils.importutils import LazyModule
    _orig_sb_getattr = LazyModule.__getattr__
    def _safe_sb_getattr(self, attr):
        try:
            return _orig_sb_getattr(self, attr)
        except Exception as e:
            raise AttributeError(attr) from e
    LazyModule.__getattr__ = _safe_sb_getattr
except ImportError:
    pass

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt

# Try to import prompt_toolkit for interactive mode
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter, Completer
    from prompt_toolkit.styles import Style
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False

from Lyrics_manager.fetcher import (
    api_providers, 
    format_to_reference_elrc, 
    is_truly_enhanced,
    _run_ai_fallback_queue
)
import Lyrics_manager.config as cfg

console = Console()

def print_logo():
    text = Text()
    # 8-bit Blocky Logo matching 'opencode' style
    text.append("█░░ █▄█ █▀█ █ █▀▀  ", style="white bold")
    text.append("█▀▄▀█ █▀█ █▄░█ █▀█ █▀▀ █▀▀ █▀█\n", style="color(208) bold")
    text.append("█▄▄ ░█░ █▀▄ █ █▄▄  ", style="white bold")
    text.append("█░▀░█ █▀█ █░▀█ █▀█ █▄█ ██▄ █▀▄\n", style="color(208) bold")
    console.print(text)

def print_help_menu():
    table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
    table.add_column("Command", style="bold white underline", width=14)
    table.add_column("Description", style="grey70")
    
    table.add_row("/fetch", "Search web APIs for synced lyrics (Line or Word-by-Word)")
    table.add_row("/ai", "Scan folder & run WhisperX AI auto-aligner with Demucs")
    table.add_row("/scan", "Scan directory & mass-process lyrics with batch re-fetching")
    table.add_row("/config", "Configure AI model sizes & set preferred API provider")
    table.add_row("/help", "Show this command reference")
    table.add_row("/exit", "Exit the application")
    
    console.print(Panel(table, border_style="color(208)", title="[bold white]❖ Interactive Commands[/bold white]", title_align="left"))


PROVIDER_ALIASES = {
    "qq": "QQ Music",
    "bini": "BiniLyrics (Apple Music)",
    "mxm": "Musixmatch",
    "netease": "NetEase",
    "kugou": "KuGou",
    "pax": "Paxsenix",
    "lrc": "LRCLIB"
}

def perform_api_fetch(title: str, artist: str, format_req: str, out_dir: Path, track_data: dict = None, save_choice: str = "2", progress_ctx = None, provider_alias: str = None, blacklist: list = None):
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from .embedder import embed_lyrics

    if track_data is None:
        track_data = {"title": title, "artist": artist, "duration_ms": 210000}

    # Only print this if not in a master progress context to avoid spam
    if not progress_ctx:
        console.print(f"\n[bold white]Searching APIs for:[/bold white] [color(208)]'{title}' by '{artist}'[/color(208)]")
    
    out_dir.mkdir(parents=True, exist_ok=True)
    
    best_found_format = None
    suboptimal_queue = []
    
    final_lyrics = ""
    final_ext = ""
    found_provider = ""
    
    if not provider_alias:
        import Lyrics_manager.config as cfg
        provider_alias = cfg.get_preferred_provider()
        
    target_provider = PROVIDER_ALIASES.get(provider_alias.lower(), provider_alias) if provider_alias else None
    blacklist = blacklist or []

    def run_fetch_loop(progress_obj):
        nonlocal best_found_format, final_lyrics, final_ext, found_provider
        
        valid_providers = []
        for name, filename, fn in api_providers:
            if target_provider and name.lower() != target_provider.lower():
                continue
            if name in blacklist:
                continue
            valid_providers.append((name, filename, fn))
            
        task_id = progress_obj.add_task(f"[white]Fetching '{title}'...", total=len(valid_providers))
        
        for name, filename, fn in valid_providers:
            try:
                raw_res = fn(track_data)
                if raw_res:
                    formatted_res = format_to_reference_elrc(raw_res, title=title, artist=artist)
                    is_enh = is_truly_enhanced(formatted_res)
                    
                    if is_enh and best_found_format != "word":
                        best_found_format = "word"
                        final_lyrics = formatted_res
                        final_ext = Path(filename).suffix
                        found_provider = name
                        break # Found the best format, stop searching!
                    elif not is_enh and not best_found_format:
                        best_found_format = "line"
                        final_lyrics = formatted_res
                        final_ext = Path(filename).suffix
                        found_provider = name
            except Exception:
                pass
            
            progress_obj.advance(task_id)
            
        progress_obj.update(task_id, completed=len(valid_providers), description=f"[green]Finished searching for '{title}'[/green]")
        if progress_ctx:
            progress_obj.remove_task(task_id) # Clean up subtask so master progress isn't cluttered

    if progress_ctx:
        run_fetch_loop(progress_ctx)
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40, complete_style="color(208)", finished_style="green"),
            TaskProgressColumn(),
            console=console,
            transient=False
        ) as progress:
            run_fetch_loop(progress)

    if final_lyrics:
        # If the user specifically requested Line-Synced (LRC), strip word timestamps from ELRC
        if format_req == "line" and best_found_format == "word":
            import re
            final_lyrics = re.sub(r"<\d{2}:\d{2}\.\d{2,3}>", "", final_lyrics)
            best_found_format = "line"
            final_ext = ".lrc"
            if not progress_ctx: console.print("  └── [bold cyan]Converted to standard LRC (Line-Synced) as requested.[/bold cyan]")

        status_str = "[green]WORD-BY-WORD[/green]" if best_found_format == "word" else "[yellow]LINE-SYNCED[/yellow]"
        if not progress_ctx: console.print(f"  └── [bold white]Found:[/bold white] {status_str} via {found_provider}")
        
        # Save logic
        audio_path = track_data.get("path")
        
        # Sidecar file
        if save_choice in ["2", "3"]:
            # Standardize filename to Title - Artist
            clean_name = "".join([c for c in f"{title} - {artist}" if c.isalpha() or c.isdigit() or c in " -_"]).rstrip()
            out_path = out_dir / f"{clean_name}{final_ext}"
            out_path.write_text(final_lyrics, encoding="utf-8")
            if not progress_ctx: console.print(f"  └── [bold white]Saved:[/bold white] [grey50]{out_path.name}[/grey50]")
            
        # Embed
        if save_choice in ["1", "3"]:
            if audio_path and Path(audio_path).exists():
                try:
                    embed_lyrics(str(audio_path), final_lyrics)
                    if not progress_ctx: console.print(f"  └── [bold green]Embedded lyrics into audio file successfully![/bold green]")
                except Exception as e:
                    if not progress_ctx: console.print(f"  └── [bold red]Failed to embed: {e}[/bold red]")
            else:
                if not progress_ctx: console.print(f"  └── [bold yellow]Could not embed: No audio file path provided.[/bold yellow]")
    else:
        if not progress_ctx: console.print(f"  └── [bold red]No lyrics found.[/bold red]")

    return found_provider


def interactive_fetch():
    console.print("\n[bold white]--- FETCH FROM WEB APIs ---[/bold white]")
    title = Prompt.ask("[bold color(208)]Enter song title[/bold color(208)]")
    artist = Prompt.ask("[bold color(208)]Enter artist name[/bold color(208)]")
    fmt_choice = Prompt.ask("[bold white]Desired format?[/bold white] [1] Line-by-Line [2] Word-by-Word", default="2")
    format_req = "line" if fmt_choice == "1" else "word"
    
    console.print("\n[bold white]How would you like to save the lyrics?[/bold white]")
    console.print("  [1] Embed into Audio File (Skipped if no audio file provided)")
    console.print("  [2] Save as sidecar file (.lrc/.elrc)")
    console.print("  [3] Both")
    save_choice = Prompt.ask("[bold color(208)]Select option[/bold color(208)]", default="2")
    
    perform_api_fetch(title, artist, format_req, Path.cwd(), save_choice=save_choice)

def interactive_ai():
    from Lyrics_manager.scanner import scan
    from Lyrics_manager.selector import selector
    from Lyrics_manager.data4api import get_params
    
    console.print("\n[bold white]--- AI FORCED ALIGNMENT (DIRECTORY SCAN) ---[/bold white]")
    directory = Prompt.ask("[bold color(208)]Enter folder path to scan for audio files[/bold color(208)]", default=str(Path.cwd()))
    
    found = scan(directory)
    if not found:
        console.print("[bold red]No audio files found or invalid directory.[/bold red]")
        return
        
    table = Table(show_header=True, header_style="color(208) bold")
    table.add_column("ID", style="color(208)")
    table.add_column("Filename", style="white")
    for idx, track in found.items():
        table.add_row(str(idx), track["name"])
    console.print(table)
    
    sel_str = Prompt.ask("[bold white]Enter IDs to process (space-separated) or 0 for all[/bold white]", default="0")
    try:
        indices = [int(x) for x in sel_str.split()]
    except ValueError:
        console.print("[bold red]Invalid selection![/bold red]")
        return
        
    selected_tracks = selector(indices, found)
    if not selected_tracks:
        console.print("[bold red]Invalid selection or no tracks selected![/bold red]")
        return
        
    parsed, failed = get_params(selected_tracks)
    
    if failed:
        console.print(f"[bold yellow]Failed to read metadata for {len(failed)} files.[/bold yellow]")
        
    fmt_choice = Prompt.ask("[bold white]Desired format?[/bold white] [1] Line-by-Line [2] Word-by-Word", default="2")
    format_req = "line" if fmt_choice == "1" else "word"
    
    console.print("\n[bold white]How would you like to save the lyrics?[/bold white]")
    console.print("  [1] Embed into Audio File")
    console.print("  [2] Save as sidecar file (.lrc/.elrc)")
    console.print("  [3] Both")
    save_choice = Prompt.ask("[bold color(208)]Select option[/bold color(208)]", default="3")
    
    queue = []
    for idx, track_data in parsed.items():
        title = track_data.get("title", track_data["path"].stem)
        artist = track_data.get("artist", "Unknown")
        queue.append({
            "title": title,
            "artist": artist,
            "path": track_data["path"]
        })
        
    if queue:
        _run_ai_fallback_queue(queue, format_req, save_choice=save_choice)

def interactive_scan():
    from Lyrics_manager.scanner import scan
    from Lyrics_manager.selector import selector
    from Lyrics_manager.data4api import get_params
    
    console.print("\n[bold white]--- SCAN DIRECTORY ---[/bold white]")
    directory = Prompt.ask("[bold color(208)]Enter folder path to scan[/bold color(208)]", default=str(Path.cwd()))
    
    found = scan(directory)
    if not found:
        console.print("[bold red]No audio files found or invalid directory.[/bold red]")
        return
        
    table = Table(show_header=True, header_style="color(208) bold")
    table.add_column("ID", style="color(208)")
    table.add_column("Filename", style="white")
    for idx, track in found.items():
        table.add_row(str(idx), track["name"])
    console.print(table)
    
    sel_str = Prompt.ask("[bold white]Enter IDs to process (space-separated) or 0 for all[/bold white]", default="0")
    try:
        indices = [int(x) for x in sel_str.split()]
    except ValueError:
        console.print("[bold red]Invalid selection![/bold red]")
        return
        
    selected_tracks = selector(indices, found)
    if not selected_tracks:
        console.print("[bold red]Invalid selection or no tracks selected![/bold red]")
        return
        
    parsed, failed = get_params(selected_tracks)
    
    if failed:
        console.print(f"[bold yellow]Failed to read metadata for {len(failed)} files.[/bold yellow]")
        
    console.print("\n[bold white]What would you like to do with these tracks?[/bold white]")
    console.print("  [1] Fetch lyrics from Web APIs")
    console.print("  [2] Run AI Forced Aligner directly")
    action = Prompt.ask("[bold color(208)]Select action[/bold color(208)]", default="1")
    
    fmt_choice = Prompt.ask("[bold white]Desired format?[/bold white] [1] Line-by-Line [2] Word-by-Word", default="2")
    format_req = "line" if fmt_choice == "1" else "word"
    
    console.print("\n[bold white]How would you like to save the lyrics?[/bold white]")
    console.print("  [1] Embed into Audio File")
    console.print("  [2] Save as sidecar file (.lrc/.elrc)")
    console.print("  [3] Both")
    save_choice = Prompt.ask("[bold color(208)]Select option[/bold color(208)]", default="3")
    
    # Process
    if action == "1":
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
        
        # Track results for the review phase
        results_map = {}
        blacklist_map = {idx: [] for idx in parsed.keys()}
        
        def run_batch_fetch():
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold white]{task.description}"),
                BarColumn(bar_width=50, complete_style="green", finished_style="green"),
                TaskProgressColumn(),
                console=console,
                transient=False
            ) as master_progress:
                
                master_task_id = master_progress.add_task("Mass Processing Songs...", total=len(parsed))
                
                for idx, track_data in parsed.items():
                    title = track_data.get("title", track_data["path"].stem)
                    artist = track_data.get("artist", "Unknown")
                    out_dir = track_data["path"].parent
                    
                    master_progress.update(master_task_id, description=f"Processing {title} by {artist}...")
                    
                    full_track = {"title": title, "artist": artist, "path": track_data["path"]}
                    provider = perform_api_fetch(
                        title, artist, format_req, out_dir, 
                        track_data=full_track, save_choice=save_choice, 
                        progress_ctx=master_progress,
                        blacklist=blacklist_map[idx]
                    )
                    
                    results_map[idx] = provider or "Failed"
                    if provider:
                        blacklist_map[idx].append(provider)
                    
                    master_progress.advance(master_task_id)
                    
                master_progress.update(master_task_id, description="[bold green]All songs processed![/bold green]")
        
        # First run
        run_batch_fetch()
        
        # Review Loop
        while True:
            console.print("\n[bold color(208)]--- BATCH RESULTS ---[/bold color(208)]")
            res_table = Table(show_header=True, header_style="color(208) bold")
            res_table.add_column("ID", style="color(208)")
            res_table.add_column("Song", style="white")
            res_table.add_column("Result", style="green")
            
            for idx, provider in results_map.items():
                track_name = parsed[idx].get("title", parsed[idx]["path"].stem)
                status_color = "red" if provider == "Failed" else "green"
                res_table.add_row(str(idx), track_name, f"[{status_color}]{provider}[/{status_color}]")
            console.print(res_table)
            
            review_str = Prompt.ask("[bold white]Are you not satisfied by any? (Enter IDs space-separated to re-fetch, or 0 if satisfied)[/bold white]", default="0")
            if review_str.strip() == "0":
                break
                
            try:
                review_ids = [int(x) for x in review_str.split()]
            except ValueError:
                console.print("[bold red]Invalid selection![/bold red]")
                continue
                
            # Filter parsed to only the ones they want to refetch
            parsed = {idx: parsed[idx] for idx in review_ids if idx in parsed}
            if not parsed:
                break
                
            console.print(f"\n[bold yellow]Re-fetching {len(parsed)} songs (excluding previous providers)...[/bold yellow]")
            run_batch_fetch()
            
    elif action == "2":
        queue = []
        for idx, track_data in parsed.items():
            title = track_data.get("title", track_data["path"].stem)
            artist = track_data.get("artist", "Unknown")
            queue.append({
                "title": title,
                "artist": artist,
                "path": str(track_data["path"])
            })
        _run_ai_fallback_queue(queue, format_req, save_choice=save_choice)

class CommandAutoSuggest:
    """Provides inline grey text auto-suggestions based on commands list"""
    def __init__(self, commands):
        self.commands = commands
    def get_suggestion(self, buffer, document):
        text = document.text
        if not text:
            return None
        for cmd in self.commands:
            if cmd.startswith(text) and cmd != text:
                from prompt_toolkit.auto_suggest import Suggestion
                return Suggestion(cmd[len(text):])
        return None

    async def get_suggestion_async(self, buffer, document):
        return self.get_suggestion(buffer, document)

class CommandCompleter(Completer):
    """Custom completer that ensures the dropdown stays visible and matches exactly what is typed including '/'."""
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        for cmd in self.commands:
            if cmd.startswith(text):
                from prompt_toolkit.completion import Completion
                yield Completion(cmd, start_position=-len(text))

def run_interactive_shell():
    print_logo()
    
    if not HAS_PROMPT_TOOLKIT:
        console.print("[red]prompt_toolkit not installed. Falling back to basic shell.[/red]")
        return
    
    commands = [
        '/fetch', '/ai', '/scan', '/config', '/help',
        '/help fetch', '/help ai', '/help config',
        '/fetch --help', '/ai --help', '/config --help',
        '/exit'
    ]
    command_completer = CommandCompleter(commands)
    
    style = Style.from_dict({
        'prompt': 'ansiyellow bold',
    })
    
    session = PromptSession(
        completer=command_completer,
        auto_suggest=CommandAutoSuggest(commands),
        style=style,
        complete_while_typing=True
    )
    
    console.print("[grey50]Type [bold white]/[/bold white] to see commands or [bold white]/help[/bold white] for details.[/grey50]\n")
    
    while True:
        try:
            text = session.prompt('lyric_manager> ').strip()
            if not text:
                continue
                
            if text in ['/exit', 'exit', 'quit', '/quit', 'q']:
                console.print("[bold color(208)]Goodbye![/bold color(208)]")
                break
            elif text.startswith('/help') or text.startswith('help'):
                parts = text.split()
                if len(parts) > 1:
                    sub = parts[1].lower().lstrip('/')
                    if sub in ['fetch', 'web', 'api']:
                        print_fetch_help()
                    elif sub in ['ai', 'align', 'whisper']:
                        print_ai_help()
                    elif sub in ['config', 'settings', 'cfg']:
                        print_config_help()
                    elif sub in ['provider', 'providers']:
                        print_fetch_help()
                    else:
                        print_cli_help()
                else:
                    print_cli_help()
            elif text in ['/fetch --help', 'fetch --help', '/fetch -h', 'fetch -h']:
                print_fetch_help()
            elif text in ['/ai --help', 'ai --help', '/ai -h', 'ai -h']:
                print_ai_help()
            elif text in ['/config --help', 'config --help', '/config -h', 'config -h']:
                print_config_help()
            elif text in ['/config', 'config']:
                import Lyrics_manager.config as cfg
                cfg.configure_settings()
            elif text in ['/fetch', 'fetch']:
                interactive_fetch()
            elif text in ['/ai', 'ai']:
                interactive_ai()
            elif text in ['/scan', 'scan']:
                interactive_scan()
            else:
                console.print(f"[bold red]Unknown command:[/bold red] {text}. Type /help")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

def print_cli_help():
    from rich.panel import Panel
    from rich.table import Table

    print_logo()
    
    console.print("[bold white]Welcome to [bold color(208)]Lyric Manager[/bold color(208)]! The ultimate CLI & AI engine for synchronized lyrics.[/bold white]\n")

    # Features Panel
    feat_table = Table(box=None, padding=(0, 1), show_header=False)
    feat_table.add_column("Bullet", style="color(208) bold", width=3)
    feat_table.add_column("Feature", style="bold white underline", width=22)
    feat_table.add_column("Desc", style="grey70")

    feat_table.add_row("◆", "Interactive Mode", "Run [bold white]lyric_manager[/bold white] with no flags to launch the interactive shell.")
    feat_table.add_row("◆", "7 Web Providers", "Fetches from [bold white]LRCLIB, Musixmatch, QQ Music, NetEase, KuGou, BiniLyrics (Apple Music), Paxsenix[/bold white].")
    feat_table.add_row("◆", "AI WhisperX Engine", "Demucs vocal separation + WhisperX forced alignment for word-level sync.")
    feat_table.add_row("◆", "Directory Scanner", "Recursively mass-processes entire audio folders with nested progress bars.")
    feat_table.add_row("◆", "Metadata Embedding", "Embeds synced lyrics (.elrc / .lrc) directly into ID3 / Vorbis tags.")
    feat_table.add_row("◆", "Dynamic Re-Fetch", "Easily reject unsatisfactory lyrics and re-fetch from alternative providers.")

    console.print(Panel(feat_table, border_style="color(208)", title="[bold white]❖ Core Features[/bold white]", title_align="left"))
    console.print()

    # Commands Panel
    cmd_table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
    cmd_table.add_column("Command", style="bold white", width=12)
    cmd_table.add_column("Description", style="grey70", width=38)
    cmd_table.add_column("Command Help", style="cyan")

    cmd_table.add_row("fetch", "Fetch lyrics from 7 web APIs", "lyric_manager fetch --help")
    cmd_table.add_row("ai", "Run WhisperX AI forced aligner", "lyric_manager ai --help")
    cmd_table.add_row("config", "Configure AI models & preferred provider", "lyric_manager config --help")
    
    console.print(Panel(cmd_table, border_style="color(208)", title="[bold white]⚡ CLI Commands[/bold white]", title_align="left"))
    console.print()

    # Provider Aliases Panel
    prov_table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
    prov_table.add_column("Alias", style="bold white underline", width=12)
    prov_table.add_column("Provider Name", style="color(208)", width=28)
    prov_table.add_column("Precision & Type", style="grey70")

    prov_table.add_row("bini", "BiniLyrics (Apple Music)", "Word-by-Word (TTML / ELRC)")
    prov_table.add_row("qq", "QQ Music", "Word-by-Word (QRC / ELRC)")
    prov_table.add_row("netease", "NetEase Cloud Music", "Word-by-Word (YRC / ELRC)")
    prov_table.add_row("kugou", "KuGou Music", "Word-by-Word (KRC / ELRC)")
    prov_table.add_row("mxm", "Musixmatch", "Word-by-Word (RichSync / ELRC)")
    prov_table.add_row("pax", "Paxsenix", "Word & Line (Apple Music API)")
    prov_table.add_row("lrc", "LRCLIB", "Line-Synced & Plain lyrics fallback")

    console.print(Panel(prov_table, border_style="color(208)", title="[bold white]♦ Provider Aliases (--provider)[/bold white]", title_align="left"))

    console.print("\n[bold grey50]Tip: Just run [bold white]lyric_manager[/bold white] without any arguments to enter the interactive dropdown shell![/bold grey50]\n")


def print_fetch_help():
    from rich.panel import Panel
    from rich.table import Table

    print_logo()
    console.print("[bold white]Command: [bold color(208)]lyric_manager fetch[/bold color(208)][/bold white]")
    console.print("[grey70]Search and fetch synchronized lyrics from 7 web API sources (Line or Word-by-Word).[/grey70]\n")

    # Options Table
    opts_table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
    opts_table.add_column("Option", style="bold white underline", width=22)
    opts_table.add_column("Description", style="grey70")

    opts_table.add_row("--title <TEXT>", "Song title (e.g. \"Starboy\"). Prompts if omitted.")
    opts_table.add_row("--artist <TEXT>", "Artist / band name (e.g. \"The Weeknd\"). Prompts if omitted.")
    opts_table.add_row("--format [LRC|ELRC]", "Target lyric format. ELRC = Word-by-Word, LRC = Line-Synced (Default: ELRC).")
    opts_table.add_row("--provider <ALIAS>", "Optional provider alias to query directly and bypass smart router.")
    opts_table.add_row("--help, -h", "Show this dedicated help page.")

    console.print(Panel(opts_table, border_style="color(208)", title="[bold white]❖ Options & Flags[/bold white]", title_align="left"))
    console.print()

    # Provider Aliases
    prov_table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
    prov_table.add_column("Alias", style="bold white underline", width=12)
    prov_table.add_column("Provider Name", style="color(208)", width=28)
    prov_table.add_column("Format Support", style="grey70")

    prov_table.add_row("bini", "BiniLyrics (Apple Music)", "Word-by-Word (TTML)")
    prov_table.add_row("qq", "QQ Music", "Word-by-Word (QRC)")
    prov_table.add_row("netease", "NetEase Cloud Music", "Word-by-Word (YRC)")
    prov_table.add_row("kugou", "KuGou Music", "Word-by-Word (KRC)")
    prov_table.add_row("mxm", "Musixmatch", "Word-by-Word (RichSync)")
    prov_table.add_row("pax", "Paxsenix", "Apple Music ELRC")
    prov_table.add_row("lrc", "LRCLIB", "Line-Synced fallback")

    console.print(Panel(prov_table, border_style="color(208)", title="[bold white]♦ Available Provider Aliases[/bold white]", title_align="left"))
    console.print()

    # Examples
    ex_table = Table(show_header=False, box=None, padding=(0, 1))
    ex_table.add_column("Bullet", style="color(208) bold", width=3)
    ex_table.add_column("Command", style="cyan")

    ex_table.add_row("►", 'lyric_manager fetch --title "Starboy" --artist "The Weeknd"')
    ex_table.add_row("►", 'lyric_manager fetch --title "Sanam Re" --artist "Mithoon" --format LRC')
    ex_table.add_row("►", 'lyric_manager fetch --title "Pungi" --artist "Pritam" --provider pax --format ELRC')

    console.print(Panel(ex_table, border_style="color(208)", title="[bold white]⚡ Examples[/bold white]", title_align="left"))
    console.print()


def print_ai_help():
    from rich.panel import Panel
    from rich.table import Table

    print_logo()
    console.print("[bold white]Command: [bold color(208)]lyric_manager ai[/bold color(208)][/bold white]")
    console.print("[grey70]Generates synchronized lyrics via AI using Demucs vocal isolation + WhisperX forced alignment.[/grey70]")
    console.print("[grey70]✦ [bold yellow]Note:[/bold yellow] AI Forced Alignment works best for [bold white]English[/bold white]; other languages are hit-or-miss depending on vocal style.[/grey70]\n")

    # Options Table
    opts_table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
    opts_table.add_column("Option", style="bold white underline", width=22)
    opts_table.add_column("Description", style="grey70")

    opts_table.add_row("--audio <PATH>", "Path to audio file (.mp3, .flac, .wav, .m4a, etc.). [Required]")
    opts_table.add_row("--transcript <PATH>", "Optional path to plain .txt lyrics. If omitted, lyrics are fetched via LRCLIB.")
    opts_table.add_row("--format [LRC|ELRC]", "Target output format. ELRC = Word-by-Word, LRC = Line-Synced (Default: ELRC).")
    opts_table.add_row("--help, -h", "Show this dedicated help page.")

    console.print(Panel(opts_table, border_style="color(208)", title="[bold white]❖ Options & Flags[/bold white]", title_align="left"))
    console.print()

    # AI Pipeline
    pipe_table = Table(show_header=False, box=None, padding=(0, 1))
    pipe_table.add_column("Step", style="color(208) bold", width=4)
    pipe_table.add_column("Phase", style="bold white underline", width=22)
    pipe_table.add_column("Desc", style="grey70")

    pipe_table.add_row("1.", "Demucs Vocal Isolation", "Splits audio stems and isolates clean acapella vocals.")
    pipe_table.add_row("2.", "Phoneme Alignment", "WhisperX dynamically aligns phonemes to word boundaries.")
    pipe_table.add_row("3.", "ELRC / LRC Output", "Exports millisecond-accurate timestamped synchronized lyrics.")

    console.print(Panel(pipe_table, border_style="color(208)", title="[bold white]⚙ AI Alignment Architecture[/bold white]", title_align="left"))
    console.print()

    # Examples
    ex_table = Table(show_header=False, box=None, padding=(0, 1))
    ex_table.add_column("Bullet", style="color(208) bold", width=3)
    ex_table.add_column("Command", style="cyan")

    ex_table.add_row("►", 'lyric_manager ai --audio "./song.mp3"')
    ex_table.add_row("►", 'lyric_manager ai --audio "./song.flac" --transcript "./lyrics.txt" --format ELRC')

    console.print(Panel(ex_table, border_style="color(208)", title="[bold white]⚡ Examples[/bold white]", title_align="left"))
    console.print()


def print_config_help():
    from rich.panel import Panel
    from rich.table import Table

    print_logo()
    console.print("[bold white]Command: [bold color(208)]lyric_manager config[/bold color(208)][/bold white]")
    console.print("[grey70]Interactive configuration wizard for AI model sizes and default preferred providers.[/grey70]\n")

    cfg_table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
    cfg_table.add_column("Setting", style="bold white underline", width=22)
    cfg_table.add_column("Options", style="color(208)", width=24)
    cfg_table.add_column("Description", style="grey70")

    cfg_table.add_row("AI Model Size", "base | large-v2", "base: Recommended (Blazing fast) | large-v2: Very precise word stamps, high VRAM")
    cfg_table.add_row("Preferred Provider", "bini, qq, mxm, netease, kugou, pax, lrc, none", "Permanent top-priority API source for lyric searches.")

    console.print(Panel(cfg_table, border_style="color(208)", title="[bold white]❖ Configurable Settings[/bold white]", title_align="left"))
    console.print()

    ex_table = Table(show_header=False, box=None, padding=(0, 1))
    ex_table.add_column("Bullet", style="color(208) bold", width=3)
    ex_table.add_column("Command", style="cyan")
    ex_table.add_row("►", "lyric_manager config")

    console.print(Panel(ex_table, border_style="color(208)", title="[bold white]⚡ Usage[/bold white]", title_align="left"))
    console.print()


@click.group(invoke_without_command=True, add_help_option=False)
@click.pass_context
@click.option('--help', '-h', is_flag=True, help="Show this help message.")
def main(ctx, help):
    """LYRIC MANAGER: The Ultimate Top-Tier CLI for Lyrics Syncing."""
    if help:
        print_cli_help()
        sys.exit(0)
        
    if ctx.invoked_subcommand is None:
        run_interactive_shell()

@main.command(add_help_option=False)
@click.option('--title', help="Song title")
@click.option('--artist', help="Artist name")
@click.option('--format', 'format_req', type=click.Choice(['LRC', 'ELRC'], case_sensitive=False), default='ELRC', help="Output format")
@click.option('--provider', 'provider_alias', help="Optional provider alias (e.g. qq, bini, mxm, netease, kugou, pax, lrc)")
@click.option('--help', '-h', is_flag=True, help="Show this help message.")
def fetch(title, artist, format_req, provider_alias, help):
    """Fetch lyrics from Web APIs"""
    if help:
        print_fetch_help()
        sys.exit(0)
    if not title:
        title = Prompt.ask("[bold color(208)]Enter song title[/bold color(208)]")
    if not artist:
        artist = Prompt.ask("[bold color(208)]Enter artist name[/bold color(208)]")
    console.print("[bold color(208)]LYRIC MANAGER[/bold color(208)] - CLI Mode")
    format_internal = "word" if format_req.upper() == "ELRC" else "line"
    perform_api_fetch(title, artist, format_internal, Path.cwd(), provider_alias=provider_alias)

@main.command(add_help_option=False)
@click.option('--audio', type=click.Path(exists=True), help="Path to audio file")
@click.option('--transcript', type=click.Path(exists=True), help="Optional path to transcript .txt")
@click.option('--format', 'format_req', type=click.Choice(['LRC', 'ELRC'], case_sensitive=False), default='ELRC')
@click.option('--help', '-h', is_flag=True, help="Show this help message.")
def ai(audio, transcript, format_req, help):
    """Generate AI synchronized lyrics (WhisperX)"""
    if help:
        print_ai_help()
        sys.exit(0)
    if not audio:
        audio = Prompt.ask("[bold color(208)]Enter path to audio file[/bold color(208)]")
    console.print("[bold color(208)]LYRIC MANAGER[/bold color(208)] - AI Mode")
    format_internal = "word" if format_req.upper() == "ELRC" else "line"
    
    title = Prompt.ask("[bold color(208)]Enter Title[/bold color(208)]", default=Path(audio).stem if audio else "Unknown")
    artist = Prompt.ask("[bold color(208)]Enter Artist[/bold color(208)]", default="Unknown")
    
    t_text = ""
    if transcript:
        t_text = Path(transcript).read_text(encoding="utf-8")
        
    console.print("\n[bold white]How would you like to save the lyrics?[/bold white]")
    console.print("  [1] Embed into Audio File")
    console.print("  [2] Save as sidecar file (.lrc/.elrc)")
    console.print("  [3] Both")
    save_choice = Prompt.ask("[bold color(208)]Select option[/bold color(208)]", default="3")
    
    queue = [{
        "title": title,
        "artist": artist,
        "path": str(audio),
        "transcript": t_text
    }]
    _run_ai_fallback_queue(queue, format_internal, save_choice=save_choice)

@main.command(add_help_option=False)
@click.option('--help', '-h', is_flag=True, help="Show this help message.")
def config(help):
    """Configure Settings"""
    if help:
        print_config_help()
        sys.exit(0)
    import Lyrics_manager.config as cfg
    cfg.configure_settings()

if __name__ == "__main__":
    main()
