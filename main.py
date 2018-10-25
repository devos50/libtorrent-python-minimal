import libtorrent as lt
import time
import sys

ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})

if len(sys.argv) < 2:
  print "Require save path as 2nd argument!"
  sys.exit(1)

torrent_urls = [
  'http://releases.ubuntu.com/18.10/ubuntu-18.10-desktop-amd64.iso.torrent',
  'http://releases.ubuntu.com/18.10/ubuntu-18.10-live-server-amd64.iso.torrent',
  'http://releases.ubuntu.com/18.04/ubuntu-18.04.1-desktop-amd64.iso.torrent',
  'http://releases.ubuntu.com/18.04/ubuntu-18.04.1-live-server-amd64.iso.torrent',
  'http://releases.ubuntu.com/16.04/ubuntu-16.04.5-desktop-amd64.iso.torrent'
]

handles = []

def add_torrent(url):
  global handles
  h = ses.add_torrent({'save_path': sys.argv[1], 'url': torrent_url})
  handles.append((h, url))
  print 'starting', h.name()
  return h


for torrent_url in torrent_urls:
  add_torrent(torrent_url)

while True:
  to_remove = []

  for h, torrent_url in handles:
    s = h.status()
    print '%s: %.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (h.name(), s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)

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
    if a.category() & lt.alert.category_t.error_notification:
      print(a)

  sys.stdout.flush()

  time.sleep(5)
