#!/usr/bin/env python3

import mysql.connector
import subprocess

DB_CONFIG = {
    "host": "localhost",
    "user": "pi",
    "password": "raspberry",
    "database": "telcom"
}

DEV = "ifb0"


def run_tc(cmd):
    print(cmd)
    subprocess.run(cmd, shell=True, check=True)


def add_filter(mac, chain, handle):
    cmd = (
        f"tc filter add dev {DEV} parent 1: "
        f"protocol ip chain 0 pref 10 handle {handle} "
        f"flower dst_mac {mac} "
        f"action goto chain {chain}"
    )
    run_tc(cmd)


def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)

    mac="0c:85:e1:8f:8a:aa"

    cur.execute("""
        SELECT d.chain, d.handle ,f.max_speed
        FROM device_info d
        JOIN filter_policy f
          ON d.name = f.name
        WHERE d.mac_address = %s
    """,(mac,))

    rows = cur.fetchall()
    row=rows[0]
    print(f"tc filter add dev ifb0 parent 1: protocol ip chain 0 pref 10 handle {row['handle']} flower dst_mac {mac} action goto chain {row['chain']}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
