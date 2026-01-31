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

def delete_filter(handle,chain,dev="ifb0"):
    """handle 指定で filter を削除"""
    cmd = f"tc filter del dev {dev} parent 1: protocol ip chain {chain} pref 10 handle {handle} flower"
    run_tc_cmd(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tcフィルタ削除")
    parser.add_argument("--handle", required=True, help="削除する filter の handle")
    parser.add_argument("--chain", required=True, help="削除する filter の chain")
    args = parser.parse_args()

    delete_filter(args.handle,args.chain)
