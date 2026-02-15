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

def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT d.chain, d.handle ,d.mac_address
        FROM device_info d
    """)

    rows = cur.fetchall()

    for r in rows:
        print(f"db:{r}")


    cur.close()
    conn.close()
    
    return rows

if __name__ == "__main__":
    main()
