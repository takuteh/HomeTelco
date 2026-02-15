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

def delete_filter(handle,chain,dev="ifb0"):
    """handle 指定で filter を削除"""
    cmd = f"tc filter del dev {dev} parent 1: protocol ip chain {chain} pref 10 handle {handle} flower"
    run_tc_cmd(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tcフィルタ操作")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add コマンド
    add_parser = subparsers.add_parser("add", help="フィルタ追加")
    add_parser.add_argument("--mac", required=True)
    add_parser.add_argument("--chain", required=True, type=int)
    add_parser.add_argument("--handle", required=True, type=int)

    # delete コマンド
    del_parser = subparsers.add_parser("delete", help="フィルタ削除")
    del_parser.add_argument("--chain", required=True, type=int)
    del_parser.add_argument("--handle", required=True, type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_filter(args.mac, args.chain, args.handle)
    elif args.command == "delete":
        delete_filter(args.handle, args.chain)

#python tclet.py add --mac 0c:85:e1:8f:8a:aa --chain 10 --handle 101
#python tclet.py delete --chain 0 --handle 101