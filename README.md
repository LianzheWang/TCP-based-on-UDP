# TCP-based-on-UDP
WATCH THE document FOR DETAILED INFORMATION plz :).

This project is an approximate implementation of TCP in application layer, which regards unreliable UDP transmission as data transmission in transport layer.

Actually, the protocol I implemented is NOT the standard TCP. Its re-transmission strategy is Sliding Window GBN.

To make a demo, after running the Receiver and Agent, run the sender.
Modify the CONFIG file to change the dir of file you want to transmit and the lose rate.
You could transmit any form of file.

Explanation
-------------------------------------------------------------
You will find this project easy to understand, it involves three parts: Sender, Receiver and Agent.

Agent could actually be regarded as a large network, it would make lose happen.

The protocol implementation is implicated inside the sender and receiver side. The sender got two threads to both transmit data and receive acks at the same time.

The packet form is C STYLE STRUCT. So it support agent written in C. (It might be helpful for some homework task.)


Thank U for reading my words. Code with love~ :)

12/03/2018 in National Taiwan University.
