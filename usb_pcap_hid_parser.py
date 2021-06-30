#!/usr/bin/python

# Shout out: https://medium.com/@ali.bawazeeer/kaizen-ctf-2018-reverse-engineer-usb-keystrok-from-pcap-file-2412351679f4

reference_dict = {
    "4": "a",
    "5": "b",
    "6": "c",
    "7": "d",
    "8": "e",
    "9": "f",
    "10": "g",
    "11": "h",
    "12": "i",
    "13": "j",
    "14": "k",
    "15": "l",
    "16": "m",
    "17": "n",
    "18": "o",
    "19": "p",
    "20": "q",
    "21": "r",
    "22": "s",
    "23": "t",
    "24": "u",
    "25": "v",
    "26": "w",
    "27": "x",
    "28": "y",
    "29": "z",
    "30": "1",
    "31": "2",
    "32": "3",
    "33": "4",
    "34": "5",
    "35": "6",
    "36": "7",
    "37": "8",
    "38": "9",
    "39": "0",
    "40": "Enter",
    "41": "esc",
    "42": "del",
    "43": "tab",
    "44": "space",
    "45": "-",
    "47": "[",
    "48": "]",
    "56": "/",
}

output_list = []

with open("hexoutput.txt", "r") as read_file:
    for line in read_file.readlines():
        bytesArray = bytearray.fromhex(line.strip())
        # print(f"{len(bytesArray)}")
        for byte in bytesArray:
            # print(f"{byte}")
            if byte != 0:
                output_list.append(int(byte))

# print(f"{len(output_list)}")

for hid_int_id in output_list:
    for k, v in reference_dict.items():
        temp = str(hid_int_id)
        if k == temp:
            print(f"{reference_dict[k]}")
        else:
            pass
            # print(f'No map found for this value: {k}')
