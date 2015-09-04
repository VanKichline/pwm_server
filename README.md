# pwm_server
A Raspberry Pi project to control high power LED strips

To install on a fresh debian install:

 - sudo apt-get update
 - sudo apt-get install git-core python-dev python-pip
 - sudo pip install wiringpi2
 - git clone https://github.com/VanKichline/pwm_server.git
 - cd pwm_server
 - sudo cp pwm_server.py /sbin/pwm_server
 - sudo nano /etc/rc.local
 - add: sudo /usr/bin/python /sbin/pwm_server < /dev/null >> /var/log/pwm_server.log 2>&1 &
 - sudo reboot

