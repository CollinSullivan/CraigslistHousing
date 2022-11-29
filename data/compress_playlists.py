import json
import pandas as pd
import argparse
import os
import csv

# num unique artists, num unique albums, num followers, num tracks, average song duration (from json),
# average valence etc (from spotifytracks), average popularity of songs (from spotifytracks)
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Compress playlists from JSON into TXT')
  parser.add_argument('csv', help='the csv file to append to')
  parser.add_argument('json', help='the playlist json')
  parser.add_argument('--delete', action='store_true', help='delete the JSON once done')
  args = parser.parse_args()

  tracks = pd.read_csv('spotifytracks.csv')
  spotvars = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness',
              'liveness', 'valence', 'popularity']
  track_id_to_vars = {}
  for row in tracks.itertuples():
    track_id_to_vars[row.track_id] = {sv: getattr(row, sv) for sv in spotvars}

  with open(args.json, 'r') as fr:
    jsondata = json.load(fr)
  
  csvfile = open(args.csv, 'a', newline='')
  writer = csv.writer(csvfile)
  if os.stat(args.csv).st_size == 0:
    writer.writerow(['num_tracks', 'num_albums', 'num_followers', 'num_artists', 'avg_song_duration_ms',
                     'avg_danceability', 'avg_energy', 'avg_speechiness', 'avg_acousticness', 'avg_instrumentalness', 
                     'avg_liveness', 'avg_valence', 'avg_popularity'])

  for playlist in jsondata['playlists']:
    playlist_data = [playlist['num_tracks'], playlist['num_albums'], playlist['num_followers'],
                     playlist['num_artists'], round(playlist['duration_ms'] / playlist['num_tracks'])]

    track_count = 0
    spotvar_sums = {sv: 0 for sv in spotvars}

    for track in playlist['tracks']:
      tid = track['track_uri'].split(':')[-1]
      if tid in track_id_to_vars:
        track_count += 1
        for sv in spotvars:
          spotvar_sums[sv] += track_id_to_vars[tid][sv]

    
    for sv in spotvars:
      if track_count > 1:
        playlist_data.append(round(spotvar_sums[sv] / track_count, 3))
      else:
        playlist_data.append(None)

    writer.writerow(playlist_data)

  csvfile.close()

  if args.delete:
    os.remove(args.json)