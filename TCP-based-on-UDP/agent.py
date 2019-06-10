from config import *
import socket
import struct
import random

drop_count = 0.0
total = 0.0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address_agent_listen)

while True:

    msg_packet, addr = s.recvfrom(2048)
    length, seq, ack, isfin, issyn, isack, data = struct.unpack("6i" + str(packet_size) + "s", msg_packet)

    if isack == 1:
        if isfin == 0:
            print("get      ack       #" + str(ack))
            s.sendto(msg_packet, address_agent_send_client)
            print("fwd      ack       #" + str(ack))
        else:
            print("get      finack")
            s.sendto(msg_packet, address_agent_send_client)
            print("fwd      finack")
    else:
        total += 1
        if isfin == 0:
            print("get      data      #" + str(seq))
            rnd = random.uniform(0, 1)
            if rnd >= drop_rate:
                s.sendto(msg_packet, address_agent_send_server)
                drop_online_rate = drop_count / total
                print("fwd      data      #" + str(seq) + ",   loss rate = " + str(round(drop_online_rate, 4)))

            else:
                drop_count += 1
                drop_online_rate = drop_count / total
                print("drop     data      #" + str(seq) + ",   loss rate = " + str(round(drop_online_rate, 4)))
        else:
            print("get      fin")
            rnd = random.uniform(0, 1)
            if rnd >= drop_rate:
                s.sendto(msg_packet, address_agent_send_server)
                drop_online_rate = drop_count / total
                print("fwd      fin")

            else:
                drop_count += 1
                drop_online_rate = drop_count / total
                print("drop     fin       #" + str(seq) + ",   loss rate = " + str(round(drop_online_rate, 4)))

s.close()
