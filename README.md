# vEfk
MeinTool zur Bearbeitung meiner vEfk-Tätigkeiten

## Launcher

Der Haupt-Launcher startet ein Tkinter-Fenster mit 20 Modul-Buttons.
Module werden als Unterordner von `modules/` erwartet und beim Klick
per `importlib` geladen. Einstiegspunkt ist jeweils `run()` oder
alternativ `launch()`.

Starten mit:

```bash
python -m launcher.main
```
