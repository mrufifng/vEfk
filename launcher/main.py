"""Tkinter-basierter Modul-Launcher.

Dieser Launcher hält eine Liste an Plugin-Modulen bereit, die jeweils in einem
Unterordner von ``modules`` abgelegt sind. Ein Klick auf den entsprechenden
Button lädt das Modul zur Laufzeit via :mod:`importlib` und ruft dessen
``run``- oder ``launch``-Funktion auf, sofern vorhanden.
"""
from __future__ import annotations

import importlib
import sys
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox
from typing import Callable, Iterable, List, Sequence

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODULES_ROOT = PROJECT_ROOT / "modules"


@dataclass(frozen=True)
class ModuleConfig:
    label: str
    module_path: str


MODULES: Sequence[ModuleConfig] = (
    ModuleConfig("PDF Merge", "modules.pdf_merge"),
    ModuleConfig("Tool 02", "modules.tool02"),
    ModuleConfig("Tool 03", "modules.tool03"),
    ModuleConfig("Tool 04", "modules.tool04"),
    ModuleConfig("Tool 05", "modules.tool05"),
    ModuleConfig("Tool 06", "modules.tool06"),
    ModuleConfig("Tool 07", "modules.tool07"),
    ModuleConfig("Tool 08", "modules.tool08"),
    ModuleConfig("Tool 09", "modules.tool09"),
    ModuleConfig("Tool 10", "modules.tool10"),
    ModuleConfig("Tool 11", "modules.tool11"),
    ModuleConfig("Tool 12", "modules.tool12"),
    ModuleConfig("Tool 13", "modules.tool13"),
    ModuleConfig("Tool 14", "modules.tool14"),
    ModuleConfig("Tool 15", "modules.tool15"),
    ModuleConfig("Tool 16", "modules.tool16"),
    ModuleConfig("Tool 17", "modules.tool17"),
    ModuleConfig("Tool 18", "modules.tool18"),
    ModuleConfig("Tool 19", "modules.tool19"),
    ModuleConfig("Tool 20", "modules.tool20"),
)


def ensure_modules_path_on_sys_path() -> None:
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))


def resolve_callable(module) -> Callable[[], None] | None:
    for candidate in ("run", "launch"):
        func = getattr(module, candidate, None)
        if callable(func):
            return func
    return None


def load_plugin(module_config: ModuleConfig) -> None:
    ensure_modules_path_on_sys_path()
    module_path = module_config.module_path
    if not (MODULES_ROOT / module_path.split(".")[-1]).exists():
        messagebox.showerror(
            "Modul nicht gefunden",
            f"Erwarteter Modulordner existiert nicht:\n{MODULES_ROOT / module_path.split('.')[-1]}",
        )
        return

    try:
        module = importlib.import_module(module_path)
    except Exception as exc:  # pragma: no cover - UI feedback only
        messagebox.showerror("Laden fehlgeschlagen", f"Modul konnte nicht geladen werden:\n{exc}")
        return

    func = resolve_callable(module)
    if func is None:
        messagebox.showwarning(
            "Kein Einstiegspunkt",
            "Das Modul stellt weder eine run() noch eine launch()-Funktion bereit.",
        )
        return

    try:
        func()
    except Exception as exc:  # pragma: no cover - UI feedback only
        messagebox.showerror("Fehler beim Start", f"Modul-Aufruf schlug fehl:\n{exc}")


def build_buttons(container: tk.Widget, modules: Iterable[ModuleConfig]) -> List[tk.Button]:
    buttons: List[tk.Button] = []
    for index, module_config in enumerate(modules):
        button = tk.Button(
            container,
            text=module_config.label,
            command=lambda cfg=module_config: load_plugin(cfg),
            width=25,
            height=2,
        )
        button.grid(row=index // 2, column=index % 2, padx=10, pady=5, sticky="ew")
        buttons.append(button)
    return buttons


def create_window() -> tk.Tk:
    root = tk.Tk()
    root.title("vEfk Module Launcher")
    root.geometry("400x500")
    root.resizable(False, False)

    header = tk.Label(root, text="Module", font=("Arial", 14, "bold"))
    header.pack(pady=(10, 5))

    grid_frame = tk.Frame(root)
    grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

    build_buttons(grid_frame, MODULES)

    return root


def main() -> None:
    MODULES_ROOT.mkdir(exist_ok=True)
    window = create_window()
    window.mainloop()


if __name__ == "__main__":
    main()
