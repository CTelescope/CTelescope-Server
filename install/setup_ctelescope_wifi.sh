INFO="[\e[1m\e[1;34m*\e[0m]"
# Update
printf "\e[35mUPDATE PACKAGES\e[0m\n"
# sudo apt-get update -y
# sudo apt-get upgrade -y
# Install dnsmasq + hostapd
printf "\e[35mSETUPING ACCESS POINT\e[0m\n"
#sudo apt-get remove --purge dnsmasq -y
#sudo rm -r /etc/dnsmasq.d -f
sudo apt install dnsmasq -y
sudo apt install hostapd -y
 
#   255.255.255.248 -> NETMASK
#   192.168.2.248   -> @Réseau
#   192.168.2.249   -> @IP Wlan0
#   192.168.2.250   |
#   192.168.2.251   |   DHCP
#   192.168.2.252   |   pool
#   192.168.2.253   |
#   192.168.2.254   -> Passerelle
#   192.168.2.255   -> @BC
WLAN="0"
NETMASK="/29"
WLAN0_IP="192.168.2.249${NETMASK}"
ROUTERS_IP="192.168.2.1${NETMASK}"
PWD="telescope_bts_snir"

printf "$INFO Stopping services\n"
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd


if [ ! -e "/etc/dhcpcd.conf" ] ; then
    touch "/etc/dhcpcd.conf"
else
    printf "$INFO Creating backup for /etc/dhcpcd.conf\n"
    sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.backup
fi

if grep -Fxq "##### CTELESCOPE #####
interface wlan${WLAN}
nohook wpa_supplicant
static ip_address=${WLAN0_IP}
static routers=${ROUTERS_IP}" "/etc/dhcpcd.conf"
then
    echo "[!] Already present in the file"
else
    sudo echo "
##### CTELESCOPE #####
interface wlan${WLAN}
nohook wpa_supplicant
static ip_address=${WLAN0_IP}
static routers=${ROUTERS_IP}
" >> /etc/dhcpcd.conf
fi



printf "$INFO Restart dhcpcd with new config\n"
sudo service dhcpcd restart

if [ ! -e "/etc/dnsmasq.conf" ] ; then
    touch "/etc/dnsmasq.conf"
else
    printf "$INFO Creating backup for /etc/dnsmasq.conf\n"
    sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.backup  
fi
# Config dhcp pool
sudo echo "
#RPiHotspot config - Internet
interface=wlan0
bind-dynamic
domain-needed
bogus-priv
dhcp-range=192.168.2.50,192.168.2.55,255.255.255.248,12h
" > /etc/dnsmasq.conf

if [ ! -e "/etc/hostapd/hostapd.conf" ] ; then
    touch "/etc/hostapd/hostapd.conf"
else
    printf "$INFO Creating backup for /etc/hostapd/hostapd.conf\n"
    sudo cp /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.backup 
fi

sudo echo "
##### CTELESCOPE #####
interface=wlan0
driver=nl80211
ssid=CTelescope
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
" > /etc/hostapd/hostapd.conf

if [ ! -e "/etc/default/hostapd" ] ; then
    touch "/etc/default/hostapd"
else
    printf "$INFO Creating backup for /etc/default/hostapd\n"
    sudo cp /etc/default/hostapd /etc/default/hostapd.backup
fi

sudo echo "
# Defaults for hostapd initscript
#
# WARNING: The DAEMON_CONF setting has been deprecated and will be removed
#          in future package releases.
#
# See /usr/share/doc/hostapd/README.Debian for information about alternative
# methods of managing hostapd.
#
# Uncomment and set DAEMON_CONF to the absolute path of a hostapd configuration
# file and hostapd will be started during system boot. An example configuration
# file can be found at /usr/share/doc/hostapd/examples/hostapd.conf.gz
#
DAEMON_CONF='/etc/hostapd/hostapd.conf'
# Additional daemon options to be appended to hostapd command:-
#       -d   show more debug messages (-dd for even more)
#       -K   include key data in debug messages
#       -t   include timestamps in some debug messages
#
# Note that -B (daemon mode) and -P (pidfile) options are automatically
# configured by the init.d script and must not be added to DAEMON_OPTS.
#
#DAEMON_OPTS=''
" > /etc/default/hostapd


printf "$INFO Enable hostapd\n"
sudo systemctl unmask hostapd
sudo systemctl enable hostapd

printf "$INFO Starting services\n"
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# sudo nano /etc/sysctl.conf
# sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
# sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
# iptables-restore < /etc/iptables.ipv4.nat

printf "\e[35mINSTALL MJPEG STREAMER\e[0m\n"
sudo dpkg -i mjpg-streamer_2.0_armhf.deb

sudo systemctl start mjpg-streamer
sudo systemctl status mjpg-streamer
sudo systemctl enable mjpg-streamer

sudo mjpg_streamer -i "input_uvc.so -r 640x480 -d /dev/video0 -f 24 -q 80"
sudo mjpg_streamer -o "output_http.so -p 5001"

printf "\e[35mINSTALL WIRINGPI\e[0m\n"
sudo dpkg -i wiringpi-2.61-1-armhf.deb