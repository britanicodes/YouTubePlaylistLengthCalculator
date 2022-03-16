import re
from datetime import timedelta
from googleapiclient.discovery import build

api_key = 'AIzaSyDNKA-ZHaQM8neL7UQ5SXDTWhKCCjqeRC8'

youtube = build('youtube', 'v3', developerKey=api_key)

hours_regex = re.compile(r'(\d+)H')
minutes_regex = re.compile(r'(\d+)M')
seconds_regex = re.compile(r'(\d+)S')

total_seconds = 0
nextPageToken = None

while True:
	pl_request = youtube.playlistItems().list(
		part='contentDetails',
		playlistId="PLWDQtIyZRZu17Oha9o2zC0aD7adlmAZl6",
		maxResults=50,
		pageToken=nextPageToken
	)

	pl_response = pl_request.execute()

	# print(pl_response)
	vid_ids = []
	for item in pl_response['items']:
		vid_ids.append(item['contentDetails']['videoId'])

	# print(','.join(vid_ids))

	vid_request = youtube.videos().list(
		part="contentDetails",
		id='.'.join(vid_ids)
		)
 
	vid_response = vid_request.execute()

	for item in vid_response['items']:
		duration = item['contentDetails']['duration']
	
		hours = hours_regex.search(duration)
		minutes = minutes_regex.search(duration)
		seconds = seconds_regex.search(duration)

		hours = int(hours.group(1)) if hours else 0
		minutes = int(minutes.group(1)) if minutes else 0
		seconds = int(seconds.group(1)) if seconds else 0

		video_seconds = timedelta(
			hours=hours,
			minutes=minutes,
			seconds=seconds
		).total_seconds()

		total_seconds += video_seconds

	nextPageToken = pl_response.get('nextPageToken')

	if not nextPageToken:
		break

total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print(f'{hours}:{minutes}:{seconds}')