# parameter defination
default_threshold = 16.0
packet_size = 1000
time_out = 1

sender_ip = 'localhost'  #127.0.0.1
sender_port = 8887#

agent_ip = 'localhost'#
agent_port = 8888#

receiver_ip = 'localhost'
receiver_port = 8889#

drop_rate = 0.2

buffer_size = 32

source_path = "sender/cmxyfTV.jpg"
dest_path = "receiver/cmxyfTV.jpg"

address_client_send_agent = (agent_ip, agent_port)
address_client_listen_agent = ('', sender_port)

address_agent_listen = ('', agent_port)
address_agent_send_client = (sender_ip, sender_port)
address_agent_send_server = (receiver_ip, receiver_port)

address_server_send_agent = (agent_ip, agent_port)
address_server_listen_agent = ('', receiver_port)
