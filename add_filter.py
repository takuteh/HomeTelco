#!/usr/bin/env python3
import subprocess
import argparse

def run_tc_cmd(cmd):
    """tcコマンド実行"""
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"成功: {cmd}")
    except subprocess.CalledProcessError as e:
        print(f"エラー: {cmd}\n{e}")

def add_filter(mac, chain,handle, dev="ifb0"):
    """
    tcでMACアドレスにフィルタを追加
    - mac: 対象MACアドレス
    - chain: chain番号
    """
    cmd = f"tc filter add dev {dev} parent 1: protocol ip chain 0 pref 10 handle {handle} flower " \
      f"dst_mac {mac} action goto chain {chain}"

    run_tc_cmd(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tcフィルタ追加")
    parser.add_argument("--mac",required=True, help="MACアドレス")
    parser.add_argument("--chain",default=1000, help="ユーザーID")
    parser.add_argument("--handle",required=True,help="端末ID")
    args = parser.parse_args()

    add_filter(args.mac, args.chain,args.handle)
