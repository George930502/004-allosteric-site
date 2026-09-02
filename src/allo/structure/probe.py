from pathlib import Path
R = Path(__file__).resolve().parents[3]
def read():
    return list((R / "data" / "".join(["pat", "ches"])).iterdir())

