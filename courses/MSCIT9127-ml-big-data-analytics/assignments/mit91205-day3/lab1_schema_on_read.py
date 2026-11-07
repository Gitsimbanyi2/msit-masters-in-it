"""Lab 1 — the same bytes mean different columns under a different SerDe."""

LINE = b"2024-03-15|North|450.00"

def pipe_serde(raw):
    dt, region, amount = raw.decode().split("|")
    return {"dt": dt, "region": region, "amount": float(amount)}


def comma_serde(raw):
    parts = raw.decode().split(",")
    if len(parts) != 3:
        raise ValueError(f"comma SerDe expected 3 fields, got {parts!r}")
    return {"dt": parts[0], "region": parts[1], "amount": float(parts[2])}


print(f"Bytes: {LINE!r}")
print(f"Pipe SerDe: {pipe_serde(LINE)}")
try:
    comma_serde(LINE)
except ValueError as exc:
    print(f"Comma SerDe on the same bytes: {exc}")
print("Schema-on-read still has a schema. It is applied when the file is read.")
