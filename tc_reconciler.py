import tc_executer
import get_filter_db
import get_filter_tc
import compare_ac
import time

INTERVAL = 30

def reconciliation_loop():
    while True:
        try:
            reconciliation()
        except Exception as e:
            print("Error in reconciler loop:", e)

        time.sleep(INTERVAL)

def reconciliation():
    db_filter = get_filter_db.main()
    tc_filter = get_filter_tc.parse_filters(get_filter_tc.get_tc_filters())
    add_list,delete_list= compare_ac.compare(db_filter,tc_filter)

    print(f"del:{delete_list}")
    print(f"add:{add_list}")

    for entry in delete_list:
        print("delete")
        tc_executer.delete_filter(entry['handle'], 0)

    for entry in add_list:
        print("add")
        tc_executer.add_filter(
            entry['mac_address'],
            entry['chain'],
            entry['handle']
        )

if __name__=="__main__":
    reconciliation_loop()