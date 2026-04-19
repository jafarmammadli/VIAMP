from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.align import Align

console = Console()

def render(lines, t):
    prev, cur, nxt = "", "", ""

    for i in range(len(lines)-1):
        if lines[i][0] <= t < lines[i+1][0]:
            prev = lines[i][1]
            cur = lines[i+1][1]
            if i+2 < len(lines):
                nxt = lines[i+2][1]
            break

    txt = Text()

    txt.append("\n\n")
    txt.append(prev + "\n", style="dim")
    txt.append(f"▶ {cur.upper()} ◀\n", style="bold magenta")
    txt.append(nxt + "\n", style="dim")

    return Align.center(txt)