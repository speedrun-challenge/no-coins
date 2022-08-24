import csv
import datetime
import json
import time
from typing import Dict

import requests

from util import is_before_deadline


def get_user_id(username: str) -> str:
  src_url = f'https://www.speedrun.com/api/v1/users/{username}'
  return json.loads(requests.get(src_url).text)['data']['id']


def get_time(username: str) -> Dict:
  user_id = get_user_id(username)
  entry = {'name': username, 'id': user_id}
  # Subway Surfers
  subsurf_url = f'https://www.speedrun.com/api/v1/runs?user={user_id}&game=y65797de&category=n2y350ed&status=verified&orderby=submitted&direction=desc'
  runs = json.loads(requests.get(subsurf_url).text)['data']

  # Variable filter: "No hoverboard/keys"
  runs = list(
    filter(lambda r: r['values']['j84eeg2n'] == '21gy6p81', runs))
  runs = list(filter(lambda r: is_before_deadline(r['submitted']), runs))

  try:
    entry['subsurf_t'] = runs[0]['times']['primary_t']
  except IndexError:
    entry['subsurf_t'] = 0

  # Temple Run 2
  tr2_url = f'https://www.speedrun.com/api/v1/runs?user={user_id}&game=m1mky3d2&category=wdmmn84d&status=verified&orderby=submitted&direction=desc'
  runs = json.loads(requests.get(tr2_url).text)['data']
  runs = list(filter(lambda r: is_before_deadline(r['submitted']), runs))

  try:
    entry['tr2_t'] = runs[0]['times']['primary_t']
  except IndexError:
    entry['tr2_t'] = 0
  return entry


############

print('Reading CSV...')
users = []
with open('bounty.csv', newline='') as csv_file:
  spam_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
  for row in spam_reader:
    users.append(row[1].strip())
users = list(set(users[1:]))
print('Users:', len(users), users)

print('Fetching user runs...')
entries = []
for username in users:
  try:
    entry = get_time(username)
    entries.append(entry)
    time.sleep(0.65)
  except:
    print(f' (failed fetching "{username}")')
print(f'Fetched {len(entries)} user times.')

# Ranking subsurf
print('Calculating ranks per game...')
entries.sort(key=lambda x: x['subsurf_t'], reverse=True)
last_value = None
count = 0
for i in range(len(entries)):
  entry = entries[i]
  if entry['subsurf_t'] != last_value:
    count = i
  entry['subsurf_rank'] = count + 1
  last_value = entry['subsurf_t']
  entries[i] = entry

# Ranking tr2
entries.sort(key=lambda x: x['tr2_t'], reverse=True)
for i in range(len(entries)):
  entry = entries[i]
  if entry['tr2_t'] != last_value:
    count = i
  entry['tr2_rank'] = count + 1
  last_value = entry['tr2_t']
  entries[i] = entry

# Calculate rank_sum
for i in range(len(entries)):
  entries[i]['rank_sum'] = entries[i]['subsurf_rank'] + entries[i]['tr2_rank']

print('Calculating overall position...')
entries.sort(key=lambda x: x['rank_sum'])

for i in range(len(entries)):
  entry = entries[i]
  if entry['rank_sum'] != last_value:
    count = i
  entry['position'] = count + 1
  last_value = entry['rank_sum']
  entries[i] = entry

print('Exporting...')
prefix = 'export const ENTRIES = '
with open('../src/app/entries.ts', 'w') as write_file:
  write_file.write(prefix + json.dumps(entries))

datetime = str(datetime.datetime.utcnow()).split('.')[0]
with open('../src/app/update-time.ts', 'w') as write_file:
  write_file.write(f'export const UPDATE_TIME = "{datetime}"')

print('Done!')
