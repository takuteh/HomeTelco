#!/bin/sh

set -e

UPLINK_IF="eth0"
AP_IF="eth1"
BR_IF="br0"
IFB_IF="ifb0"

nmcli device set eth0 managed no
nmcli device set eth1 managed no

ip link add name "$BR_IF" type bridge

ip link set dev "$UPLINK_IF" down
ip link set dev "$AP_IF" down

ip addr flush dev "$UPLINK_IF"
ip addr flush dev "$AP_IF"

ip link set dev "$UPLINK_IF" master "$BR_IF"
ip link set dev "$AP_IF" master "$BR_IF"

ip addr flush dev "$BR_IF"
ip addr add 10.100.0.131/24 dev "$BR_IF"

ip link set dev "$UPLINK_IF" up
ip link set dev "$AP_IF" up
ip link set dev "$BR_IF" up

modprobe ifb
ip link add "$IFB_IF" type ifb
ip link set dev "$IFB_IF" up

tc qdisc add dev "$UPLINK_IF" handle ffff: ingress

#UPLINK_IFのingressをegressとしてIFB_IFにリダイレクト
tc filter add dev "$UPLINK_IF" parent ffff: protocol ip u32 \
match u32 0 0 \
action mirred egress redirect dev "$IFB_IF"

#IFB_IF来たパケットをデフォルトで1000クラスに振り分け
tc qdisc add dev "$IFB_IF" root handle 1: htb default 1000
tc class add dev ifb0 parent 1: classid 1:1000 htb rate 1000mbit ceil 1000mbit
