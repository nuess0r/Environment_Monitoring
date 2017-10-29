#!/usr/bin/python
# Author: Christoph Zimmermann

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import os
import ConfigParser
import rrdtool

def read_config(fname):
    #read config file if present
    cfg = ConfigParser.ConfigParser(allow_no_value=True)
    if os.path.isfile(fname):
        cfg.read(fname)
    else:
        print('Config file ' + fname + ' not found')

    if not cfg.has_section("settings"):
        print('Config file has no section settings. Consult the example config')

    return cfg


def main(argv=None):
    dirname = os.path.dirname(__file__)
    config_file = os.path.join(dirname, 'log_dht_data_and_warn.cfg')
    cfg = read_config(config_file)

    rrd_file     = cfg.get('settings', 'rrd_file')
    rrd_graphs   = cfg.get('settings', 'rrd_graphs')
    graph_width  = cfg.get('settings', 'graph_width')
    graph_height = cfg.get('settings', 'graph_height')

    HOUR = 3600
    DAY  = 24 * HOUR
    WEEK = 7 * DAY
    MONTH = 5 * WEEK

    if not os.path.isfile(rrd_file):
        print('No RRD database found! Please check if it exists and check the configured path.\nExiting')
        return 0

    if not os.path.exists(rrd_graphs):
        print('Output folder does not exist! Please check if it exists and check the configured path.\nExiting')
        return 0

    rrdtool.graph(rrd_graphs + 'temp_day.png',
		'--imgformat', 'PNG',
		'--width', graph_width,
		'--height', graph_height,
		'--start', "-%i" % DAY,
		'--end', "-1",
		'--vertical-label', 'Temperature',
		'--title', 'Temperature over a day',
		'DEF:temperature={0:s}:temperature:AVERAGE'.format(rrd_file),
		'LINE2:temperature#590099:Temperature')

    rrdtool.graph(rrd_graphs + 'humid_day.png',
		'--imgformat', 'PNG',
		'--width', graph_width,
		'--height', graph_height,
		'--start', "-%i" % DAY,
		'--end', "-1",
		'--vertical-label', 'Humidity',
		'--title', 'Humidity over a day',
                '--upper-limit', '100',
                '--lower-limit', '0',
		'DEF:humidity={0:s}:humidity:AVERAGE'.format(rrd_file),
		'LINE2:humidity#590099:Humidity')

    rrdtool.graph(rrd_graphs + 'temp_week.png',
		'--imgformat', 'PNG',
		'--width', graph_width,
		'--height', graph_height,
		'--start', "-%i" % WEEK,
		'--end', "-1",
		'--vertical-label', 'Temperature',
		'--title', 'Temperature over a week',
		'DEF:temperature={0:s}:temperature:AVERAGE'.format(rrd_file),
		'DEF:temperature_max={0:s}:temperature:MAX'.format(rrd_file),
		'DEF:temperature_min={0:s}:temperature:MIN'.format(rrd_file),
		'LINE2:temperature#590099:Avg. Temperature',
		'LINE2:temperature_max#990033:Max. Temperature',
		'LINE2:temperature_min#006899:Min. Temperature')

    rrdtool.graph(rrd_graphs + 'humid_week.png',
		'--imgformat', 'PNG',
		'--width', graph_width,
		'--height', graph_height,
		'--start', "-%i" % WEEK,
		'--end', "-1",
		'--vertical-label', 'Humidity',
		'--title', 'Humidity over a week',
                '--upper-limit', '100',
                '--lower-limit', '0',
		'DEF:humidity={0:s}:humidity:AVERAGE'.format(rrd_file),
		'DEF:humidity_max={0:s}:humidity:MAX'.format(rrd_file),
		'DEF:humidity_min={0:s}:humidity:MIN'.format(rrd_file),
		'LINE2:humidity#590099:Avg. Humidity',
		'LINE2:humidity_max#990033:Max. Humidity',
		'LINE2:humidity_min#006899:Min. Humidity')

    rrdtool.graph(rrd_graphs + 'temp_month.png',
		'--imgformat', 'PNG',
		'--width', graph_width,
		'--height', graph_height,
		'--start', "-%i" % MONTH,
		'--end', "-1",
		'--vertical-label', 'Temperature',
		'--title', 'Temperature over a month',
		'DEF:temperature={0:s}:temperature:AVERAGE'.format(rrd_file),
		'DEF:temperature_max={0:s}:temperature:MAX'.format(rrd_file),
		'DEF:temperature_min={0:s}:temperature:MIN'.format(rrd_file),
		'LINE2:temperature#590099:Avg. Temperature',
		'LINE2:temperature_max#990033:Max. Temperature',
		'LINE2:temperature_min#006899:Min. Temperature')

    rrdtool.graph(rrd_graphs + 'humid_month.png',
		'--imgformat', 'PNG',
		'--width', graph_width,
		'--height', graph_height,
		'--start', "-%i" % MONTH,
		'--end', "-1",
		'--vertical-label', 'Humidity',
		'--title', 'Humidity over a month',
                '--upper-limit', '100',
                '--lower-limit', '0',
		'DEF:humidity={0:s}:humidity:AVERAGE'.format(rrd_file),
		'DEF:humidity_max={0:s}:humidity:MAX'.format(rrd_file),
		'DEF:humidity_min={0:s}:humidity:MIN'.format(rrd_file),
		'LINE2:humidity#590099:Avg. Humidity',
		'LINE2:humidity_max#990033:Max. Humidity',
		'LINE2:humidity_min#006899:Min. Humidity')

if __name__ == "__main__":
    sys.exit(main())
