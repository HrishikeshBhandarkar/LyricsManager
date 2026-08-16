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

DEFAULT_PROVIDER_ORDER = ["bini", "kugou", "netease", "qq", "mxm", "pax", "lrc"]

def get_whisper_model_size() -> str:
    config = load_config()
    return config.get("whisper_model", "base")

def prompt_first_time_ai_model() -> str:
    """
    If the user runs AI mode for the first time without having configured a model,
    prompts them with model explanations and recommends the Base model.
    """
    config = load_config()
    if config.get("ai_model_configured"):
        return config.get("whisper_model", "base")
        
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.panel import Panel
    
    console = Console()
    
    info_text = (
        "[bold white]Which AI Whisper model would you like to use?[/bold white]\n\n"
        "  [bold color(208)][1] Base Model (Recommended)[/bold color(208)]\n"
        "      • Instant and enough for day-to-day use for languages like English.\n"
        "      • Lightweight (~140 MB) and fast inference on both CPU and GPU.\n\n"
        "  [bold color(208)][2] Large Model (Large-V2)[/bold color(208)]\n"
        "      • Takes a lot of time and VRAM, but is more precise.\n"
        "      • Works with other languages, but is still a hit or miss (~1.5 GB)."
    )
    
    console.print()
    console.print(Panel(info_text, border_style="color(208)", title="[bold white]🤖 First-Time AI Model Selection[/bold white]", title_align="left"))
    
    choice = Prompt.ask(
        "[bold color(208)]Select model [1] Base (Recommended) or [2] Large-V2[/bold color(208)]",
        choices=["1", "2"],
        default="1"
    )
    
    chosen_model = "base" if choice == "1" else "large-v2"
    config["whisper_model"] = chosen_model
    config["ai_model_configured"] = True
    save_config(config)
    
    console.print(f"[bold green]✔ Saved '{chosen_model}' as your preferred AI model! (Change anytime via /config)[/bold green]\n")
    return chosen_model

def get_preferred_provider() -> str:
    config = load_config()
    return config.get("preferred_provider", "")

def get_provider_order() -> list[str]:
    config = load_config()
    custom_order = config.get("provider_order")
    if isinstance(custom_order, list) and custom_order:
        base_order = [p.lower().strip() for p in custom_order if isinstance(p, str)]
    else:
        base_order = list(DEFAULT_PROVIDER_ORDER)
        
    pref = get_preferred_provider().lower().strip()
    if pref and pref in base_order:
        base_order.remove(pref)
        base_order.insert(0, pref)
    elif pref:
        base_order.insert(0, pref)
        
    return base_order

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
    console.print("  [bold color(208)][2][/bold color(208)] [bold white]Top Preferred Provider[/bold white] (Quick 1-step top priority)")
    console.print("  [bold color(208)][3][/bold color(208)] [bold white]Full Custom Fallback Order[/bold white] (Override full search sequence)")
    console.print("  [bold color(208)][4][/bold color(208)] [bold white]View Current Configuration[/bold white]")
    console.print("  [bold color(208)][5][/bold color(208)] [grey70]Cancel / Exit[/grey70]")
    
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
        console.print(f"\n[bold white]Top Preferred Provider Priority (Current: [bold color(208)]{curr_prov}[/bold color(208)])[/bold white]")
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
        prov_table.add_row("none", "None", "Disable preference, use configured fallback order")
        
        console.print(Panel(prov_table, border_style="color(208)", title="[bold white]Available Aliases[/bold white]", title_align="left"))
        
        prov_choice = Prompt.ask("\n[bold color(208)]Enter alias or 'none'[/bold color(208)]", default=config.get("preferred_provider", "") or "none").strip().lower()
        
        if prov_choice in ["none", "", "null", "no"]:
            config["preferred_provider"] = ""
            console.print("[bold green][OK] Preferred provider cleared! Using full fallback sequence.[/bold green]\n")
        else:
            config["preferred_provider"] = prov_choice
            console.print(f"[bold green][OK] Preferred provider set to: '{prov_choice}'[/bold green]\n")
            
        save_config(config)
        
    elif choice == "3":
        current_chain = get_provider_order()
        console.print(f"\n[bold white]Full Custom Fallback Order & Search Chain[/bold white]")
        console.print(f"[grey70]Current active sequence: [bold color(208)]{' -> '.join(current_chain)}[/bold color(208)][/grey70]")
        console.print("[grey70]Enter comma-separated provider aliases in your exact preferred fallback sequence, or 'default' to reset.[/grey70]\n")
        
        valid_aliases = {"bini", "qq", "netease", "kugou", "mxm", "pax", "lrc"}
        user_chain_input = Prompt.ask("[bold color(208)]Enter custom fallback sequence[/bold color(208)]", default=", ".join(current_chain))
        
        if user_chain_input.strip().lower() in ["default", "reset"]:
            config["provider_order"] = list(DEFAULT_PROVIDER_ORDER)
            console.print("[bold green][OK] Reset to default provider fallback chain![/bold green]\n")
        else:
            new_chain = [x.strip().lower() for x in user_chain_input.split(",") if x.strip().lower() in valid_aliases]
            if new_chain:
                config["provider_order"] = new_chain
                console.print(f"\n[bold green][OK] Custom fallback chain updated: [bold white]{' -> '.join(new_chain)}[/bold white][/bold green]\n")
            else:
                console.print("[bold red]No valid aliases provided. Fallback chain unchanged.[/bold red]\n")
                
        save_config(config)
        
    elif choice == "4":
        console.print("\n[bold color(208)]--- CURRENT CONFIGURATION ---[/bold color(208)]")
        cfg_table = Table(show_header=True, header_style="color(208) bold", box=None, padding=(0, 1))
        cfg_table.add_column("Key", style="bold white underline", width=22)
        cfg_table.add_column("Value", style="color(208)")
        
        cfg_table.add_row("Whisper Model", config.get("whisper_model", "large-v2"))
        cfg_table.add_row("Preferred Top Provider", config.get("preferred_provider", "") or "None (Follows Chain)")
        cfg_table.add_row("Fallback Search Chain", " -> ".join(get_provider_order()))
        cfg_table.add_row("Config File", str(CONFIG_PATH))
        
        console.print(Panel(cfg_table, border_style="color(208)", title="[bold white]Settings Summary[/bold white]", title_align="left"))
        console.print()
    else:
        console.print("[grey50]Configuration unchanged.[/grey50]\n")
