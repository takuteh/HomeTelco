import get_filter_db as f_db 
import get_filter_tc as f_tc

def compare(db_filter, tc_filter):
    add_list = []
    delete_list = []

    # tcをMACキー辞書に変換
    tc_dict = {
        t['mac_address']: t
        for t in tc_filter
        if 'mac_address' in t
    }

    # dbのMACセットを作る
    db_mac_set = {d['mac_address'] for d in db_filter}

    # ---- DB基準チェック ----
    for db in db_filter:
        mac = db['mac_address']

        if mac not in tc_dict:
            print("tcに無い：", mac)
            add_list.append(db)
        else:
            tc_entry = tc_dict[mac]

            if (db['chain'] == tc_entry['goto_chain'] and
                db['handle'] == tc_entry['handle']):
                print("一致：", mac)
            else:
                print("一部不一致：", mac)
                delete_list.append(tc_entry)
                add_list.append(db)

    # ---- TCにしかないもの ----
    for mac, tc_entry in tc_dict.items():
        if mac not in db_mac_set:
            print("dbに無い：", mac)
            delete_list.append(tc_entry)

    return add_list, delete_list

if __name__=='__main__':
    db_filter = f_db.main()
    tc_filter = f_tc.parse_filters(f_tc.get_tc_filters())
    compare(db_filter,tc_filter)