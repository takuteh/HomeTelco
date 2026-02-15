import subprocess
import re

def parse_filters(text):
    filters = []
    current = None

    for line in text.splitlines():

        # フィルター開始行
        m = re.search(r'chain (\d+).*handle (0x[0-9a-f]+|\d+)', line)
        if m:
            if current:
                filters.append(current)

            current = {
                "chain": int(m.group(1)),
                "handle": int(m.group(2), 0)
            }
            continue

        if not current:
            continue

        # MAC
        m = re.search(r'dst_mac ([0-9a-f:]+)', line)
        if m:
            current["mac_address"] = m.group(1)

        # goto
        m = re.search(r'goto chain (\d+)', line)
        if m:
            current["goto_chain"] = int(m.group(1))

    if current:
        filters.append(current)

    print(f"tc:{filters}")
    return filters


def get_tc_filters():
    cmd = ["tc", "filter", "show", "dev", "ifb0", "parent", "1:"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


parse_filters(get_tc_filters())
