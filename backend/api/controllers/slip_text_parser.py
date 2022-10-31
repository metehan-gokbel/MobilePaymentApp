import json


def parser(data):
    try:
        slip_text = json.loads(data, strict=False)
    except Exception:
        return "xxxxxxxxxxxxxxxxxx"

    for index in slip_text[-2:]:
        try:
            index["t1"] = index["t1"].replace("Ã–", "OO*").replace("Ãœ", "UU*").replace("Ã‡", "Ç").replace("ÄŸ",
                                                                                                           "Ğ")
            index["t1"] = index["t1"].encode('iso-8859-9').decode("utf-8")
            index["t1"] = index["t1"].replace("OO*", "Ö").replace("UU*", "Ü")
        except:
            continue

    merchant_list = list()
    client_list = list()
    st_dict = dict()
    for string_index in slip_text[-2:]:  # ilk liste
        st_value = 2
        for index in string_index:  # ikinci liste
            key_check = index.keys()
            if "st" in key_check:
                if index.get("st") == 1:
                    st_value = 1
                elif index.get("st") == 0:
                    st_value = 0
                else:
                    st_value = 2

            if st_value == 1:
                inner_dict_creator_for_pax(key_check, index, merchant_list)
            elif st_value == 0:
                inner_dict_creator_for_pax(key_check, index, client_list)
            else:
                continue

    st_dict['merchant'] = merchant_list
    st_dict['client'] = client_list

    return st_dict


def inner_dict_creator_for_pax(key_check, index, inner_slip_info):  # keylist , index yani dict , yazılacak liste
    if "f" in key_check:
        if 'N' in index.values():
            if index['t1'] == '\n\n\n\n\n':
                del index
            else:
                new_line = ""
                index = index['t1'].strip(' ')
                centered_index = index.center(41, ' ')
                new_line += '1' + centered_index
                inner_slip_info.append(new_line)

        elif 'B' in index.values():
            new_line = ""
            index = index["t1"].strip(' ')
            centered_index = index.center(21, ' ')
            new_line += '2' + centered_index
            inner_slip_info.append(new_line)
        elif 'L' in index.values():
            new_line = ""
            new_line += index["t1"]
            inner_slip_info.append(new_line)
