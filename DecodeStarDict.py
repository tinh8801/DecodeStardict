#StartSict to MDict Source Text
'''
Cấu trúc từ điển StarDict
  Phần từ vựng và dịch nghĩa được tách ra nằm ở 2 file
    File .idx chứa từ vựng cùng với thông tin để truy vấn phần dịch nghĩa trong file .dict
        Mỗi từ vựng là chuỗi bytes kết thúc bằng 0x00
        4 bytes tiếp theo là offset của phần dịch nghĩa
        4 bytes tiếp theo là độ dài của phần dịch nghĩa
        Nếu version từ điển là 3.0.0+ thì offset và độ dài sẽ là 8 bytes
    File .dict chứa phần dịch nghĩa
        Dựa vào thông tin offset và độ dài ở trên để đọc dữ liệu
    File .ifo chứa thông tin mô tả về từ điển
'''
import os
import argparse
import time

def get_file_size(f):
    tmp = open(f, "rb")
    tmp.seek(0, os.SEEK_END)
    fs = tmp.tell()
    tmp.close()
    return fs
    
def Convert(idx, dct, txt):
    try:
        idx_file = open(idx, "rb")
        dict_file = open(dct, "rb")
        text_file = open(txt, "w+", encoding = "UTF-8")
    except:
        print("I/O Error!")
        quit()
    keyword_array = list()
    info_array = list()
    meaning_array = list()
    keyword = ""
    offset = 0
    length = 0
    b = 0
    print("Converting...")
    begin = time.time() 
    while idx_file.tell() < get_file_size(idx):
        b = idx_file.read(1)
        if int.from_bytes(b) != 0:
            keyword_array.append(int.from_bytes(b))       
        else:
            tmp = bytes(keyword_array)
            keyword = tmp.decode("UTF-8")
            #print(f"Keyword: {keyword}")
            text_file.write(keyword)
            text_file.write("\n")
            
            for a in range(0, 8):
                info_array.append(int.from_bytes(idx_file.read(1)))
            #print(idx_file.tell()
            offset = int.from_bytes(bytes(info_array[0:4]))
            length = int.from_bytes(bytes(info_array[4:8]))
            #print(f"Offset: {offset}")
            #print(f"Length: {length}")
            
            dict_file.seek(offset)
            meaning_array = dict_file.read(length)
            s = meaning_array.decode("UTF-8")
            #print(s)
            text_file.write("<pre>")
            text_file.write(s)
            text_file.write("</pre>")
            text_file.write("\n")
            text_file.write("</>")
            text_file.write("\n")
            info_array = []
            keyword_array = []
            
    idx_file.close()
    dict_file.close()
    text_file.close()
    print(f"Export to {txt}")
    print("Done")
    now = time.time()
    print(f"Convert time: {now - begin} seconds")
    
def main():
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":: Stardict Decode                                                       ::")
    print(":: Phiên bản: 0.1                                                        ::")
    print(":: Date: 2025.06.28                                                      ::")
    print(":: Tác giả: Huy Thắng                                                    ::")
    print(":: Convert StarDict to MDict source text                                 ::")
    print(":: Câu lệnh: DecodeStarDict.py [idx_file] [dict_file] [output_file]      ::")
    print(":: Ví dụ:                                                                ::")
    print(":: DecodeStarDict.py E-V.idx E-V.dict output.txt                         ::")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    
    parser = argparse.ArgumentParser(description="StarDict to MDict")
    parser.add_argument("idx_file", help="Tập tin .idx", type=str)
    parser.add_argument("dict_file", help="Tập tin .dict", type=str)
    parser.add_argument("output_file", help="Tập tin .txt", type=str)
    arg = parser.parse_args()
    
    try:
        Convert(arg.idx_file, arg.dict_file, arg.output_file)
    except:
        print("Có lỗi xảy ra.")
        quit()

if __name__ == "__main__":
    main()
    #Convert("xe.idx", "xe.dict", "kq.txt")

    