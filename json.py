import json

FILE_NAME = "sample-data.json"


DN_W = 50
DESC_W = 20
SPEED_W = 8
MTU_W = 6

with open(FILE_NAME, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(
    f'{"DN":<{DN_W}} '
    f'{"Description":<{DESC_W}}  '
    f'{"Speed":<{SPEED_W}}  '
    f'{"MTU":<{MTU_W}}'
)
print(
    f'{"-" * DN_W} '
    f'{"-" * DESC_W}  '
    f'{"-" * SPEED_W}  '
    f'{"-" * MTU_W}'
)

for item in data.get("imdata", []):
    attrs = item.get("l1PhysIf", {}).get("attributes", {})
    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")

    
    dn = dn[:DN_W]
    descr = descr[:DESC_W]

    print(f"{dn:<{DN_W}} {descr:<{DESC_W}}  {speed:<{SPEED_W}}  {mtu:<{MTU_W}}")