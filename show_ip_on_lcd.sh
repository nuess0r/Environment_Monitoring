#! /bin/sh
### BEGIN INIT INFO
# Provides:          show_ip_on_lcd
# Required-Start:    $network $remote_fs $syslog
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: Shows the IP address of eth0 on a I2C LCD
# Description:       Shows the IP address of eth0 on a I2C LCD
### END INIT INFO

case "$1" in
    start)
	/usr/bin/python /usr/local/bin/show_ip_on_lcd.py > /tmp/show_ip.log
	logger "IP address shown on LCD"
	;;
    restart|reload|force-reload)
        echo "Error: argument '$1' not supported" >&2
        exit 3
        ;;
    stop|status)
        # No-op
        ;;
    *)
        echo "Usage: $0 start|stop" >&2
        exit 3
        ;;
esac

:
