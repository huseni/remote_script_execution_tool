#!/bin/bash
DATE="date +%d-%m-%Y"

s1="wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -"
s2="sudo apt-get install -y apt-transport-https"
s3='echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-5.x.list'
s4='sudo apt-get -y update && sudo apt-get install -y filebeat'
s5='sudo update-rc.d filebeat defaults 95 10'
s6='sudo chmod 777 /home/ubuntu/filebeat.yml'
s7='sudo chown -hR root:root /home/ubuntu/filebeat.yml'
s8='sudo rm -rf /etc/filebeat/filebeat.yml'
s9='sudo cp -rf /home/ubuntu/filebeat.yml /etc/filebeat/filebeat.yml'
s10='sudo /etc/init.d/filebeat start'
$s1
$s2
$s3
$s4
$s5
$s6
$s7
$s8
$s9
$s10
