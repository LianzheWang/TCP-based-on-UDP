import socket
import struct
import os
from config import *


def make_struct(length=packet_size, seq=0, ack=0, isfin=0, issyn=0, isack=1, data=" ".encode()):
    sss = struct.pack("6i" + str(packet_size) + "s", length, seq, ack, isfin, issyn, isack, data)
    return sss


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address_server_listen_agent)

try:
    os.remove(dest_path)
except:
    pass

file = open(dest_path, 'w')
file.close()
f = open(dest_path, 'wb')

buff_ = bytes()
buff_count = 0
curr = 1
ended = False

while True:
    msg_packet, addr = s.recvfrom(2048)
    length, seq, ack_, isfin, issyn, isack, data = struct.unpack("6i" + str(packet_size) + "s", msg_packet)

    if isfin == 0:
        print("recv     data      #" + str(seq))
        if seq < curr:
            ack_ = seq

        if seq == curr:
            ack_ = curr
            curr += 1
            buff_ = buff_ + data
            buff_count += 1

        if seq > curr:
            ack_ = curr - 1
        packet = make_struct(ack=ack_, isfin=isfin)
        s.sendto(packet, address_server_send_agent)
        print("send     ack       #" + str(ack_))
        if buff_count >= buffer_size:
            f.write(buff_)
            buff_ = bytes()
            buff_count = 0
            print("flush")

    else:
        print("recv     fin")
        if seq < curr:
            ack_ = seq
            isfin = 0

        if seq == curr:
            ack_ = curr
            # curr += 1
            buff_ = buff_ + data[:length]
            buff_count += 1

        if seq > curr:
            ack_ = curr - 1
            isfin = 0

        if isfin == 1:
            packet = make_struct(ack=ack_, isfin=isfin)
            s.sendto(packet, address_server_send_agent)
            print("send     finack")
            if not ended:
                f.write(buff_)
                f.flush()
                print("flush")
                ended = True
            buff_ = bytes()
            buff_count = 0

            break
        else:
            packet = make_struct(ack=ack_, isfin=isfin)
            s.sendto(packet, address_server_send_agent)
            print("send     ack       #" + str(ack_))

s.close()
f.close()
