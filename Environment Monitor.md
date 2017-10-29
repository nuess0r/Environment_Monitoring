# Vorbereitung

## Raspberry Pi

### Vorbereiten

#### Material Bereitstellen
- Raspberry Pi 3
- Micro SD Karte (sollte schon im Raspberry Pi 3 eingelegt sein)
- Netzteil
- HDMI Kabel
- HDMI nach DVI Adapter
- Breadboard
- DHT11 Feuchtigkeits und Temperatursensor
- 1602 LCD mit aufgelötetem I²C Adapter
- 10 kOhm Widerstand

#### Am Arbeitsplatz vorhanden
- Monitor
- Tastatur
- Netzwerk

#### Aufbau
1. Raspberry Pi mit Tastatur und Netzwerk verbinden
1. Raspberry Pi mit HDMI Kabel und DVI Adapter an Monitor anschliessen

### Raspian Installation

1. Debian Jessy Lite herunterladen https://www.raspberrypi.org/downloads/raspbian/2
1. Gemäss Anleitung SD Karte beschreiben https://www.raspberrypi.org/documentation/installation/installing-images/README.md
1. SD Karte einlegen
1. Netzteil anschliessen
1. Bootvorgang abwarten
1. Einloggen mit standard Benutzer pi und Passwort raspberry

### Raspian Konfiguration

#### raspi-config

In der Kommandozeile das Konfigurationsprogramm raspi-config starten und folgende Einstellungen vornehmen:

1. Konfigurationsprogramm starten: sudo raspi-config
1. Hostname ändern
1. Tastatur Layout ändern (4 Localisation Options)
1. SSH Server aktivieren (5 Interfacing Options)
1. I²C aktivieren (5 Interfacing Options)
1. Raspberry Pi neustarten: sudo reboot


#### Netzwerk

1. Einloggen mit standard Benutzer pi und Passwort raspberry
1. Verbindung testen: `ping zbw.ch`
1. Ansonsten IP beziehen: `sudo dhclient eth0`
1. Nochmals testen
1. IP Adresse anzeigen lassen: `/sbin/ifconfig`
1. Vom Laptop aus testen ob ein remote Login per SSH möglich ist

#### Paketquellen und Updates

1. Paketquellen aktualisieren: `sudo apt update`
1. Updates installieren: sudo apt dist-upgrade
1. Installierte und verfügbare Pakete können mit Aptitude angesehen werden: `sudo aptitude`


## Ein- und Ausgänge (GPIOs)

**Nur 3.3 V Pegel. Raspberry Pins werden zerstört mit 5 V!**

Raspberry Pi besitzt nur digitale Ein- und Ausgänge. Es können daher direkt keine Analogwerte gemessen werden. Dazu wird immer ein Analog/Digital Konverter (ADC) benötigt oder ein aktiver Sensor mit digitaler Schnittstelle.

Die digitalen Ein- und Ausgänge sind vergleichbar mit denen des Arduinos, sie können in der Software als Eingang, Ausgang konfiguriert werden mit optionalem Pull-Up oder Pull-Down Widerstand.

Informationen zu den Anschlüssen und den Pin Nummern für WiringPi sind unter https://pinout.xyz/ zu finden.


## LCD in Betrieb nehmen

### Hardware

Zum Einsatz kommt ein LC Display das zwei Teilen mit je 16 alphanumerischen Zeichen (Zahlen und Buchstaben) darstellen kann.
Die Ansteuerung des Displays ist kompatibel zum sehr verbreiteten HD44780 Displaytreiberchip.

Das Display wird, um Pins zu sparen, per mit einem I²C Konverter an den Raspberry Pi angeschlossen.
Dazu werden vier Verbindungskabel (Buchse - Buchse) benötigt.

| LCD      | Raspberry Pi |
| -------- | ------------ |
| GND      | GND          |
| VCC      | 5 V          |
| SDA      | SDA          |
| SCL      | SCL          |

### Software

Falls noch nicht gemacht, I²C aktivieren:
1. Konfigurationsprogramm starten: sudo raspi-config
1. I²C aktivieren (5 Interfacing Options)
1. Raspberry Pi neustarten: `sudo reboot`

Libraries installieren:
1. `sudo apt install i2c-tools build-essential python-dev python-smbus python-pip git`
1. `sudo pip install adafruit-charlcd`

#### Beispiel code

Folgenden Code in eine neue Datei mit dem Namen lcd_test1.py auf dem Raspberry Pi kopieren.
Zum Beginn in den Pfad `/home/pi/`.
Das kann z. B. per SSH und nano (oder einem anderen Editor wie vi) oder per scp erledigt werden.


Das so erstellte Python Skript mit `python lcd_test1.py` ausführen.

    #!/usr/bin/env python2.7
    # -*- coding: utf-8 -*-

    from Adafruit_CharLCD import Adafruit_CharLCD
    import Adafruit_GPIO.PCF8574 as PCF
    import time

    gpio = PCF.PCF8574(address=0x3f)

    # Define PCF pins connected to the LCD.
    lcd_rs        = 0	
    lcd_rw        = 1
    lcd_en        = 2
    lcd_backlight = 3
    d4,d5,d6,d7   = 4,5,6,7
    cols,lines    = 16,2
    
    gpio.setup(lcd_rw, PCF.OUT)
    gpio.output(lcd_rw, 0)

    # Instantiate LCD Display
    lcd = Adafruit_CharLCD(lcd_rs, lcd_en, d4, d5, d6, d7, cols, lines,
                           lcd_backlight, invert_polarity=False, gpio=gpio)
    
    lcd.clear()
    lcd.message('  Raspberry Pi\n  I2C LCD 0x3f')
    lcd.set_backlight(1)

#### Beispiel code 2

Folgenden Code in eine neue Datei mit dem Namen lcd_test2.py auf dem Raspberry Pi kopieren.
Zum Beginn in den Pfad `/home/pi/`.
Das kann z. B. per SSH und nano (oder einem anderen Editor wie vi) oder per scp erledigt werden.


Das so erstellte Python Skript mit `python lcd_test2.py` ausführen.

    #!/usr/bin/env python2.7
    # -*- coding: utf-8 -*-

    from Adafruit_CharLCD import Adafruit_CharLCD
    import Adafruit_GPIO.PCF8574 as PCF
    import time

    gpio = PCF.PCF8574(address=0x3f)

    # Define PCF pins connected to the LCD.
    lcd_rs        = 0
    lcd_rw        = 1
    lcd_en        = 2
    lcd_backlight = 3
    d4,d5,d6,d7   = 4,5,6,7
    cols,lines    = 16,2

    gpio.setup(lcd_rw, PCF.OUT)
    gpio.output(lcd_rw, 0)

    # Instantiate LCD Display
    lcd = Adafruit_CharLCD(lcd_rs, lcd_en, d4, d5, d6, d7, cols, lines,
                           lcd_backlight, invert_polarity=False, gpio=gpio)

    # Demo scrolling message right/left.
    lcd.clear()
    message = 'Scroll'
    lcd.message(message)
    for i in range(cols - len(message)):
        time.sleep(0.5)
        lcd.move_right()
    for i in range(cols - len(message)):
        time.sleep(0.5)
        lcd.move_left()

    # Demo turning backlight off and on.
    lcd.clear()
    lcd.message('Flash backlight\nin 5 seconds...')
    time.sleep(5.0)
    # Turn backlight off.
    lcd.set_backlight(0)
    time.sleep(2.0)
    # Change message.
    lcd.clear()
    lcd.message('Goodbye!')
    # Turn backlight on.
    lcd.set_backlight(1)


Quelle:
http://www.rototron.info/using-an-i2c-lcd-display-with-a-raspberry-pi/
https://learn.adafruit.com/character-lcd-with-raspberry-pi-or-beaglebone-black/usage


#### Script um IP anzuzeigen

Python script show_ip_on_lcd.py:

    #!/usr/bin/env python2.7
    # -*- coding: utf-8 -*-

    from Adafruit_CharLCD import Adafruit_CharLCD
    import Adafruit_GPIO.PCF8574 as PCF
    import time
    import socket
    import fcntl
    import struct

    # Define PCF pins connected to the LCD.
    lcd_rs        = 0
    lcd_rw        = 1
    lcd_en        = 2
    lcd_backlight = 3
    d4,d5,d6,d7   = 4,5,6,7
    cols,lines    = 16,2


    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])


    gpio = PCF.PCF8574(address=0x3f)

    gpio.setup(lcd_rw, PCF.OUT)
    gpio.output(lcd_rw, 0)

    # Instantiate LCD Display
    lcd = Adafruit_CharLCD(lcd_rs, lcd_en, d4, d5, d6, d7, cols, lines,
                           lcd_backlight, invert_polarity=False, gpio=gpio)


    ip_address = get_ip_address('eth0')

    lcd.clear()
    lcd.message('My IP address is\n' + ip_address)
    lcd.set_backlight(1)


Init script (show_ip_on_lcd.sh):

    #! /bin/sh
    ### BEGIN INIT INFO
    # Provides:          $show_ip_on_lcd
    # Required-Start:    $network
    # Required-Stop:
    # Should-Start:      $portmap
    # Default-Start:     S
    # Default-Stop:
    # Short-Description: Shows the IP address of eth0 on a I2C LCD
    # Description:       Shows the IP address of eth0 on a I2C LCD
    ### END INIT INFO

    case "$1" in
	start)
	    python /usr/local/bin/show_ip_on_lcd.py
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


systemd service script (show_ip_on_lcd.service):

    [Unit]
    Description=Show IP address on LCD
    After=network.target

    [Service]
    Type=oneshot
    ExecStart=/usr/bin/python /usr/local/bin/show_ip_on_lcd.py > /tmp/show_ip.log

    [Install]
    WantedBy=multi-user.target



Installation mit System-V Init System:
- `sudo cp show_ip_on_lcd.py /usr/local/bin/`
- `sudo cp show_ip_on_lcd.sh /etc/init.d/`
- `sudo rc-update default /etc/init.d/show_ip_on_lcd.sh`


Installation mit systemd (default unter Raspian Jessie):
- `sudo cp show_ip_on_lcd.py /usr/local/bin/`
- `sudo cp show_ip_on_lcd.service /etc/systemd/system/`
- `sudo systemctl enable show_ip_on_lcd.service`



### DHT11 Feuchtigkeits und Temperatursensor

### Hardware

Pinning des DHT/AM2302 Sensors (von Links nach Rechts):

* VCC (3.3 V Power)
* Data out
* Not connected
* Ground

Zwischen dem Datenpin und VCC muss ein Pull-Up Widerstand mit 10 KOhm angeschlossen werden.

Schliessen sie den Datenpin am GPIO 4 (BCM 4) an.


### Software

Folgen sie dem Tutorial unter https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/software-install-updated
bis und mit dem Punkt Testing the Library.

Schreiben sie ein Skript/Programm, dass alle paar Sekunden den Sensor ausliest und die Daten auf dem LCD darstellt.


## Sensor Daten aufzeichnen

Schreiben sie ein Skript/Programm, dass alle paar Minuten den Sensor ausliest und die Daten zusammen mit einem Timestamp in eine Datei speichert.

Als Dateiformat bieten sich csv oder rrd an.

Die Beispiellösung verwendet einen Cronjob der jeweils ein Python Skript aufruft, dass RRDtool nutzt. Es steht ihnen frei andere Lösungswege einzuschlagen.

RRDtool dient zum Speichern und Visualisieren von regelmässigen Datenpunkten zusammen mit einem Timestamp (http://oss.oetiker.ch/rrdtool/).


Um RRDtool mit Python zu verwenden müssen sie die passende Libraries installieren:
- `sudo apt install rrdtool python-rrdtool`

Crontab:
http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples

## Einfache Webseite um Sensor Daten anzuzeigen

### Sensor Daten visualisieren

Wenn sie zum Aufzeichnen schon RRDtool verwendet haben, können sie ihre Daten damit auch visualisieren. In der Python Syntax sieht das z. B. so aus:

    rrdtool.graph('/home/pi/temp_day.png',
		'--imgformat', 'PNG',
		'--width', graph_width,
		'--height', graph_height,
		'--start', "-%i" % DAY,
		'--end', "-1",
		'--vertical-label', 'Temperature',
		'--title', 'Temperature over a day',
		'DEF:temperature={0:s}:temperature:AVERAGE'.format(rrd_file),
		'LINE2:temperature#590099:Temperature')

Im Zusammenhang mit CSV Dateien bieten sich auch andere Libraries wie z. B. MathPlotLib oder Kommandozeilenwerkzeuge wie GNUplot an.

### Webserver aufsetzen

sudo apt install apache2

Öffnen sie einen Browser und testen sie ob die default Webseite angezeigt wird.

Die Daten, die der Webserver ausliefert, sind defaultmässig unter dem Pfad `/var/www/html/` gespeichert.

### Statische HTML Seite

Erstellen sie eine einfach statische Webseite, die die erzeugten Visualisierung anzeigt.

Sie können das vorhandene Beispiel (index.html) dazu verwenden.

### Optionen und Erweiterungen

Den weiteren Verlauf des Projektes bestimmen sie selber. Die folgenden Aufgaben sollen als Anregung dienen.

1. Lagern sie alle system- und benutzerspezifischen Angaben in eine Konfigurationsdatei aus (in Musterlösungen enthalten)
1. Alarmierung per E-Mail (in Musterlösungen enthalten)
1. Test E-Mail generieren per Tastendruck
1. Schliessen sie mehrere Taster an um auf dem Display eine Menustruktur benutzen zu können um z. B. weitere Daten (IP Adresse, Uptime, Uhrzeit etc.) abzurufen oder Einstellungen zu verändern
1. Visualisierung dynamisch generieren mit Server-side Scripting
1. Visualisierung dynamisch generieren im Browser per JavaScript. Dazu muss der Webserver die Sensordaten z. B. als JSON anliefern können
1. Weitere Sensorn anschliessen wie z. B. Bewegungsmelder
1. Zusätzlich zur Webseite mit den Visualisierungen soll eine Webseite generiert werden, die den Status anzeigt, also ob die eingestellten Grenzwerte eingehalten werden. Es reicht wenn Ok bzw. Failed angezeigt wird.
1. Programmieren sie einen Arduino UNO mit Ethernet Shield so, dass dieser regelmässig den Status des Raspberry Pi prüft und auf LEDs anzeigt.
1. Schliessen sie an den Arduino oder den Raspberry Pi einen Buzzer an, der akustisch Warnt wenn die Grenzwerte überschritten werden.
