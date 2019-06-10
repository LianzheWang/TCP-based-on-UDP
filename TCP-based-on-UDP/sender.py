from config import *
import socket
import struct
import os
from threading import Thread
from time import *

congest_window_threshold = default_threshold
window_size = 1.0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address_client_listen_agent)


# typedef struct

# {

#     int length;

#     int seq;

#     int ack;

#     int isfin;

#     int issyn;

#     int isack;

#     char[1000] data;

# } packet_struct;

def make_struct(length=packet_size, seq=0, ack=0, isfin=0, issyn=0, isack=0, data=" ".encode()):
    sss = struct.pack("6i" + str(packet_size) + "s", length, seq, ack, isfin, issyn, isack, data)
    return sss


largest = 1
pak_buff = []

f = open(source_path, 'rb')
flag = True

file_size = os.path.getsize(source_path)
num_packets = file_size // packet_size + 1
curr = 1
largest = 0
base = 1
started = time()
sended = 0


def sendout():
    global sended
    global started
    global base
    global largest
    global curr
    global num_packets
    global flag
    global window_size
    global congest_window_threshold
    global pak_buff
    while flag:
        if base > num_packets:
            flag = False

        if (time() - started) > time_out:
            curr = base
            congest_window_threshold = float(int(window_size) // 2)
            if congest_window_threshold < 1.0:
                congest_window_threshold = 1.0
            window_size = 1.0
            started = time()
            print("timeout                  Threshold = " + str(int(congest_window_threshold)))

        if curr > num_packets:
            continue

        if curr < base + int(window_size):
            if curr > largest:
                if curr == num_packets:
                    pak_buff.append(f.read())
                else:
                    pak_buff.append(f.read(packet_size))
                largest = curr

            msg = pak_buff[curr - base]

            if curr == num_packets:
                packet = make_struct(length=file_size - (num_packets - 1) * packet_size, seq=curr, isfin=1, data=msg)

                if curr > sended:
                    print("send     fin")
                    sended += 1
                else:
                    print("resnd    fin")

            else:
                packet = make_struct(seq=curr, data=msg)
                if curr > sended:
                    print("send     data      #" + str(curr) + ",   winSize = " + str(int(window_size)))
                    sended += 1
                else:
                    print("resnd    data      #" + str(curr) + ",   winSize = " + str(int(window_size)))

            s.sendto(packet, address_client_send_agent)
            curr += 1


t = Thread(target=sendout)
t.start()

while True:
    ack_packet, addr = s.recvfrom(2048)
    length, seq, ack, isfin, issyn, isack, data = struct.unpack("6i" + str(packet_size) + "s", ack_packet)
    if isfin == 0:

        if ack == base:
            base = ack + 1
            pak_buff.pop(0)
            started = time()
            if window_size < congest_window_threshold:
                window_size += 1.0
            else:
                window_size += 1 / float(int(window_size))
        print("recv     ack       #" + str(ack))
    else:
        print("recv     finack")
        base = num_packets + 1
        break

f.close()
s.close()
# t.join()
