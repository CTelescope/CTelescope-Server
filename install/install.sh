INFO="[\e[1m\e[1;34m*\e[0m]"
# Check root
if [ $(whoami) != "root" ]; then
    printf "\e[1;31mNeed root permission!\n"
    exit;
fi
# Test for network conection
for interface in $(ls /sys/class/net/ | grep -v lo);
do
  if [ $(cat /sys/class/net/$interface/carrier) = 1 ]; then OnLine=1; fi
done
if ! [ $OnLine ]; then echo "\e[1;31mNot Online" > /dev/stderr; exit; fi
# Update
printf "\e[35mUPDATE & INSTALL PACKAGES\e[0m\n"
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt install hostapd -y
sudo apt install dnsmasq -y
sudo apt install pip -y
sudo apt install libavcodec-dev -y
sudo apt install libgtk2.0-dev -y
sudo apt install libgtk-3- -ydev

printf "\e[35mINSTALL MJPEG STREAMER\e[0m\n"
sudo dpkg -i mjpg-streamer_2.0_armhf.deb

printf "\e[35mPython packages\e[0m\n"
sudo apt-get install libatlas-base-dev
pip install sphinx flask  flask_cors  opencv-python  astropy[recommended]
pip install -U numpy

printf "\e[35mSETUPING ACCESS POINT\e[0m\n"
#                       #   255.255.255.248 -> NETMASK
#                       #   10.0.0.248   -> @Réseau
#                       #   10.0.0.249   -> @IP Interface Wlan0
#                       #   10.0.0.250   |
#    NETWORK CONFIG     #   10.0.0.251   |   DHCP
#                       #   10.0.0.252   |   pool
#                       #   10.0.0.253   |
#                       #   10.0.0.254   -> Passerelle
#                       #   10.0.0.255   -> @BC
#     EDITABLE PART     #
# v v v v v v v v v v v #
WLAN="0"
WLAN_IP="10.0.0.249"
WLAN_GW="10.0.0.254"
WLAN_NM="255.255.255.248"

SSID="CTelescope"
PWD="telescope_bts_snir"
NB_CLIENT=1

ETH0_STATIQUE_IP="192.168.1.30"  #  
ETH0_STATIQUE_GW="192.168.1.254" # 
ETH0_NM="255.255.255.0"          #  Ne pas changer
ETH0_NW_IP="192.168.1.0"         #  
ETH0_BC="192.168.1.255"          #

printf "$INFO Stopping services\n"
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd

if [ ! -e "/etc/dhcpcd.conf" ] ; then
    touch "/etc/dhcpcd.conf"
else
    printf "$INFO Creating backup for /etc/dhcpcd.conf\n"
    sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.backup
fi
sudo echo "
# Inform the DHCP server of our hostname for DDNS.
ctelescope
# Use the hardware address of the interface for the Client ID.
clientid
# Persist interface configuration when dhcpcd exits.
persistent

nohook wpa_supplicant
nohook lookup-hostname

# ##### CTELESCOPE ACCESS POINT #####
 interface wlan${WLAN}
     static ip_address=${WLAN_IP}
     static routers=${WLAN_GW}
" > /etc/dhcpcd.conf


if [ ! -e "/etc/network/interfaces" ] ; then
    touch "/etc/network/interfaces"
else
    printf "$INFO Creating backup for /etc/network/interfaces\n"
    sudo cp /etc/network/interfaces /etc/dhcpcd.conf.backup
fi
sudo echo "
# interfaces(5) file used by ifup(8) and ifdown(8)

# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'

# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

auto lo iface
lo inet loopback auto

eth0 iface
eth0 inet static

iface eth0 inet static
       address ${ETH0_STATIQUE_IP}
       netmask ${ETH0_NM}
       gateway ${ETH0_STATIQUE_GW}
       network ${ETH0_NW_IP}
       broadcast ${ETH0_BC}
" > /etc/network/interfaces

printf "$INFO Restart dhcpcd with new config\n"
sudo service dhcpcd restart

if [ ! -e "/etc/dnsmasq.conf" ] ; then
    touch "/etc/dnsmasq.conf"
else
    printf "$INFO Creating backup for /etc/dnsmasq.conf\n"
    sudo cp /etc/dnsmasq.conf /etc/dnsma sq.conf.backup
fi
#
#    ! IF THIS FILE PREVIOSLY MODIFY YOU NEED TO CHANGE THE DHCP RANGE !
#
sudo echo "
#RPiHotspot
# resolv-file=/etc/dnsmasq.resolv
interface=wlan${WLAN}
dhcp-range=10.0.0.250,10.0.0.253,255.255.255.248,12h
" > /etc/dnsmasq.conf

if [ ! -e "/etc/hostapd/hostapd.conf" ] ; then
    touch "/etc/hostapd/hostapd.conf"
else
    printf "$INFO Creating backup for /etc/hostapd/hostapd.conf\n"
    sudo cp /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.backup
fi

sudo echo "
country_code=FR
interface=wlan${WLAN}
driver=nl80211
ssid=${SSID}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=$PWD
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
max_num_sta=$NB_CLIENT
" > /etc/hostapd/hostapd.conf

if [ ! -e "/etc/default/hostapd" ] ; then
    touch "/etc/default/hostapd"
else
    printf "$INFO Creating backup for /etc/default/hostapd\n"
    sudo cp /etc/default/hostapd /etc/default/hostapd.backup
fi

sudo echo "
DAEMON_CONF='/etc/hostapd/hostapd.conf'
" > /etc/default/hostapd

if [ ! -e "/lib/dhcpcd/dhcpcd-hooks/40-route" ] ; then
    touch "/lib/dhcpcd/dhcpcd-hooks/40-route"
else
    printf "$INFO Creating backup for /lib/dhcpcd/dhcpcd-hooks/40-route\n"
    sudo cp /lib/dhcpcd/dhcpcd-hooks/40-route /lib/dhcpcd/dhcpcd-hooks/40-route.backup
fi
#
#    ! NEED TO MODIFY MANUALLY !
#          Static routes
#
sudo echo "
ip route add 192.168.1.0/24 via ${WLAN_GW}
ip route add 10.0.0.0/29 via ${ETH0_STATIQUE_GW}
" > /lib/dhcpcd/dhcpcd-hooks/40-route

sudo echo "
net.ipv4.ip_forward=1
" > /etc/sysctl.conf

printf "$INFO Enable the wireless access point service and set it to start when your Raspberry Pi boots\n"
sudo systemctl unmask hostapd
sudo systemctl enable hostapd

printf "$INFO Starting services\n"
sudo systemctl start hostapd
sudo systemctl start dnsmasq

sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -t nat -A  POSTROUTING -o wlan0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

printf "$INFO Config startup scripts\n"
sudo echo "

iptables-restore < /etc/iptables.ipv4.nat

sudo systemctl start mjpg-streamer
sudo systemctl enable mjpg-streamer
sudo mjpg_streamer -i \"input_uvc.so -r 640x480 -d /dev/video0 -f 24 -q 80\"
sudo mjpg_streamer -o \"output_http.so -p 5001\"

exit 0
" > /etc/rc.local