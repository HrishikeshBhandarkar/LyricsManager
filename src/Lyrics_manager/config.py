import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.json"

def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config(config_data: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)

def get_whisper_model_size() -> str:
    config = load_config()
    return config.get("whisper_model", "large-v2")

def get_preferred_provider() -> str:
    config = load_config()
    return config.get("preferred_provider", "")

def configure_settings():
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
    
    config = load_config()
    
    console.print("\n[bold color(208)]--- CONFIGURATION MENU ---[/bold color(208)]")
    console.print("[bold white]What would you like to configure?[/bold white]")
    console.print("  [bold color(208)][1][/bold color(208)] [bold white]AI Model Size[/bold white] (WhisperX Base vs Large-V2)")
    console.print("  [bold color(208)][2][/bold color(208)] [bold white]Preferred Provider Priority[/bold white] (Bini, QQ, NetEase, Musixmatch, etc.)")
    console.print("  [bold color(208)][3][/bold color(208)] [bold white]View Current Configuration[/bold white]")
    console.print("  [bold color(208)][4][/bold color(208)] [grey70]Cancel / Exit[/grey70]")
    
    choice = Prompt.ask("\n[bold color(208)]Select option[/bold color(208)]", default="1")
    
    if choice == "1":
        curr_model = config.get("whisper_model", "large-v2")
        console.print(f"\n[bold white]AI Model Size (Current: [bold color(208)]{curr_model}[/bold color(208)])[/bold white]")
        console.print("  [bold color(208)][1][/bold color(208)] [bold green]Base (Recommended)[/bold green] [grey70]— Blazing fast inference, lightweight VRAM[/grey70]")
        console.print("  [bold color(208)][2][/bold color(208)] [bold white]Large-V2[/bold white] [grey70]— Recommended if you want very precise word stamps; not recommended if you have a bottleneck of VRAM and if you prefer speed[/grey70]")
        
        m_choice = Prompt.ask("\n[bold color(208)]Select model size[/bold color(208)]", default="1" if curr_model == "base" else "2")
        config["whisper_model"] = "base" if m_choice == "1" else "large-v2"
        save_config(config)
        console.print(f"\n[bold green][OK] AI Model updated to: '{config['whisper_model']}'[/bold green]\n")
        
    elif choice == "2":
        curr_prov = config.get("preferred_provider", "") or "None (Default Smart Router)"
        console.print(f"\n[bold white]Preferred Provider Priority (Current: [bold color(208)]{curr_prov}[/bold color(208)])[/bold white]")
        console.print("[grey70]If set, Lyric Manager will always search this provider first before any other.[/grey70]\n")
        
        prov_table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
        prov_table.add_column("Alias", style="bold white underline", width=10)
        prov_table.add_column("Provider Name", style="color(208)", width=26)
        prov_table.add_column("Description", style="grey70")
        
        prov_table.add_row("bini", "BiniLyrics (Apple Music)", "Word-by-Word (TTML)")
        prov_table.add_row("qq", "QQ Music", "Word-by-Word (QRC)")
        prov_table.add_row("netease", "NetEase Cloud Music", "Word-by-Word (YRC)")
        prov_table.add_row("kugou", "KuGou Music", "Word-by-Word (KRC)")
        prov_table.add_row("mxm", "Musixmatch", "Word-by-Word (RichSync)")
        prov_table.add_row("pax", "Paxsenix", "Apple Music ELRC")
        prov_table.add_row("lrc", "LRCLIB", "Line-Synced fallback")
        prov_table.add_row("none", "None", "Disable preference, use smart auto-order")
        
        console.print(Panel(prov_table, border_style="color(208)", title="[bold white]Available Aliases[/bold white]", title_align="left"))
        
        prov_choice = Prompt.ask("\n[bold color(208)]Enter alias or 'none'[/bold color(208)]", default=config.get("preferred_provider", "") or "none").strip().lower()
        
        if prov_choice in ["none", "", "null", "no"]:
            config["preferred_provider"] = ""
            console.print("[bold green][OK] Preferred provider cleared! Using default smart order.[/bold green]\n")
        else:
            config["preferred_provider"] = prov_choice
            console.print(f"[bold green][OK] Preferred provider set to: '{prov_choice}'[/bold green]\n")
            
        save_config(config)
        
    elif choice == "3":
        console.print("\n[bold color(208)]--- CURRENT CONFIGURATION ---[/bold color(208)]")
        cfg_table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
        cfg_table.add_column("Key", style="bold white underline", width=22)
        cfg_table.add_column("Value", style="color(208)")
        
        cfg_table.add_row("Whisper Model", config.get("whisper_model", "large-v2"))
        cfg_table.add_row("Preferred Provider", config.get("preferred_provider", "") or "None (Smart Auto)")
        cfg_table.add_row("Config File", str(CONFIG_PATH))
        
        console.print(Panel(cfg_table, border_style="color(208)", title="[bold white]Settings Summary[/bold white]", title_align="left"))
        console.print()
    else:
        console.print("[grey50]Configuration unchanged.[/grey50]\n")
