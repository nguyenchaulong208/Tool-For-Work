import subprocess
import csv
import json

OUTPUT_FILE = "symlink_deep_report.csv"

# PowerShell command to list all reparse points (symlink, junction, mount point)
PS_COMMAND = r"""
Get-ChildItem -Path C:\ -Recurse -Force -ErrorAction SilentlyContinue |
Where-Object { $_.Attributes -match "ReparsePoint" } |
Select-Object FullName, LinkType, Target |
ConvertTo-Json -Depth 5
"""

def run_powershell(cmd):
    result = subprocess.run(
        ["powershell", "-Command", cmd],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    return result.stdout

def save_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "type", "target"])
        for item in data:
            writer.writerow([
                item.get("FullName", ""),
                item.get("LinkType", ""),
                item.get("Target", "")
            ])

if __name__ == "__main__":
    print("Scanning deeply for all symlink/junction/reparse points...")

    output = run_powershell(PS_COMMAND)

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        print("Error: Could not parse PowerShell output.")
        exit()

    if isinstance(data, dict):
        data = [data]

    save_csv(data, OUTPUT_FILE)

    print(f"Done! Found {len(data)} reparse points. Saved to {OUTPUT_FILE}")