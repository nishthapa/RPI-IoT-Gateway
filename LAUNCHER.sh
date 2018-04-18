#!/bin/bash


#............ STARTING UP NRF MODULE ............#
sleep 2
pushd ~/Desktop/RPI_GATEWAY/NRF24L01/
lxterminal -e python NRF_MQTT.py
sleep 1
#................................................#



#.......... STARTING UP TEST MODULE 1 ...........#
pushd ..
pushd TEST
lxterminal -e python TEST_PUB_1.py
sleep 1
#................................................#



#.......... STARTING UP TEST MODULE 2 ...........#
lxterminal -e python TEST_PUB_2.py
sleep 1
#................................................#



#........ STARTING UP MASTER SUBSCRIBER .........#
pushd ../MASTER_SUBS
lxterminal -e python MASTER_SUB.py
sleep 1
#................................................#



#......... STARTING UP PACKET ROUTER ............#
sleep 1
# pushd ~/Desktop/RPI_GATEWAY/PACKET_ROUTER/
pushd ../PACKET_ROUTER
lxterminal -e python PACKET_ROUTER.py
sleep 1
#................................................#