import json
import os

import libtorrent as lt
import time
import sys

DEFAULT_DHT_ROUTERS = [
    ("dht.libtorrent.org", 25401),
    ("router.bittorrent.com", 6881),
    ("router.utorrent.com", 6881)
]

ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
settings = ses.get_settings()
settings['prefer_rc4'] = True
ses.set_settings(settings)
ses.start_dht()
for router in DEFAULT_DHT_ROUTERS:
    ses.add_dht_router(*router)

print "Libtorrent settings:"
print json.dumps(ses.get_settings())

if len(sys.argv) < 2:
    print "Require save path as 2nd argument!"
    sys.exit(1)

handles = []
start_time = time.time()

torrents_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

# Make output dir
if not os.path.exists(os.path.join(sys.argv[1], 'output')):
    os.makedirs(os.path.join(sys.argv[1], 'output'))

with open(os.path.join(sys.argv[1], 'output', 'download_stats.csv'), 'w') as out_file:
    out_file.write('time,infohash,speed_up,speed_down,progress\n')


def add_torrent(torrent_path):
    global handles
    info = lt.torrent_info(torrent_path)
    h = ses.add_torrent({'save_path': sys.argv[1], 'ti': info})
    handles.append((h, torrent_path))
    print 'starting', h.name()
    return h


for torrent_path in os.listdir(torrents_dir):
    add_torrent(os.path.join(torrents_dir, torrent_path))

while True:
    to_remove = []

    with open(os.path.join(sys.argv[1], 'output', 'download_stats.csv'), 'a') as out_file:
        for h, torrent_url in handles:
            s = h.status()
            print '%s: %.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
                h.name(), s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)
            passed_time = time.time() - start_time
            out_file.write('%s,%s,%s,%s,%s\n' % (passed_time, str(h.info_hash()), s.upload_rate, s.download_rate, s.progress))

            if h.is_seed():
                ses.remove_torrent(h, 1)  # Remove files
                to_remove.append((h, torrent_url))
                time.sleep(3)
                add_torrent(torrent_url)

    for item in to_remove:
        handles.remove(item)

    print ""
    print "-- Alerts --"
    alerts = ses.pop_alerts()
    for a in alerts:
        if a.category() & (lt.alert.category_t.error_notification | lt.alert.category_t.performance_warning):
            print(a)
    print ""

    sys.stdout.flush()

    time.sleep(5)
