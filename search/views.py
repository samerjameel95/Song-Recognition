import requests
import subprocess
import ffmpeg
import json
import os
import sys
from pytube import *
from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render, redirect


# defining function
def youtube(request):
    # checking whether request.method is post or not
    if request.method == 'POST':
        # getting link from frontend
        link = request.POST['link']
        video = YouTube(link)
        # setting video resolution
        stream = video.streams.get_lowest_resolution()
        # stream = video.get_audio_only(subtype = 'mp3')
        # downloads video
        video1 = stream.download(output_path = None, filename= 'video.mp4', filename_prefix= None, skip_existing= True, timeout= None, max_retries = 0)
        # Convert video from MP4 to MP3
        if (video1):
            mp4_file = "video.mp4"
            mp3_file = "audio.mp3"
            cmd = "ffmpeg -i {} -to 00:01:00  {} -y".format(mp4_file, mp3_file)
            os.system(cmd)
        else:
            print('error')
    data = {
        'api_token': '4e75fcfca13166ed9cfaa0c4df4391b1',
        'return': 'apple_music,spotify',
    }
    files = {
        'file': open('audio.mp3', 'rb'),
    }
    result = requests.post('https://api.audd.io/', data=data, files=files)
    # print(result.text)

    # print(result.json()['result']['artist'])

    # Input the key value that you want to search
    keyVal = ("artist")

    # load the json data
    customer = result.json()['result']
    # Search the key value using 'in' operator
    try:
        if keyVal in customer:
            # Print the success message and the value of the key
            # print("%s is found in JSON data" %keyVal)
            print("The value of", keyVal,"is", customer[keyVal])
        else:
            # Print the message if the value does not exist
            print("This is not a song")
    except:
        print("This is not a song")
        # exit()

    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part' : 'snippet',
            'q' : customer[keyVal],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 15,
            'type' : 'video',
            'regionCode': 'iq'
        }
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
        # if request.POST['submit'] == 'lucky':
        #     return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 15,
            'regionCode': 'iq'
        }
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'urlId': f'{ result["id"] }'
            }
            videos.append(video_data)
            print(video_data['urlId'])
    context = {
        'videos' : videos
    }
    return render(request, 'search/index.html', context)

        
        # returning HTML page
        # return render(request, 'index.html')
    return render(request, 'index.html')


# Function for Trim and Convert downloaded video to audio
# def audioConvert():
#     # Convert video from MP4 to MP3
#     if (video1):
#         mp4_file = base_dir + "video.mp4"
#         mp3_file = base_dir + "audio.mp3"
#         cmd = "ffmpeg -i {} -to 00:01:00  {} -y".format(mp4_file, mp3_file)
#         os.system(cmd)
#     else:
#         print('error')


# Function for Audio recognize
# def audD():
#     data = {
#         'api_token': '4e75fcfca13166ed9cfaa0c4df4391b1',
#         'return': 'apple_music,spotify',
#     }
#     files = {
#         'file': open('audio.mp3', 'rb'),
#     }
#     result = requests.post('https://api.audd.io/', data=data, files=files)
#     # print(result.text)

#     # print(result.json()['result']['artist'])

#     # # Input the key value that you want to search
#     keyVal = ("artist")

#     # # load the json data
#     customer = result.json()['result']
#     # Search the key value using 'in' operator
#     if keyVal in customer:
#         # Print the success message and the value of the key
#         # print("%s is found in JSON data" %keyVal)
#         print("The value of", keyVal,"is", customer[keyVal])
#     else:
#         # Print the message if the value does not exist
#         print("%s is not found in JSON data" %keyVal)


# Function for searching a song
# def index(request):
#     videos = []
#     if request.method == 'POST':
#         search_url = 'https://www.googleapis.com/youtube/v3/search'
#         video_url = 'https://www.googleapis.com/youtube/v3/videos'
#         search_params = {
#             'part' : 'snippet',
#             'q' : request.POST['search'],
#             'key' : settings.YOUTUBE_DATA_API_KEY,
#             'maxResults' : 15,
#             'type' : 'video',
#             'regionCode': 'iq'
#         }
#         r = requests.get(search_url, params=search_params)
#         results = r.json()['items']
#         video_ids = []
#         for result in results:
#             video_ids.append(result['id']['videoId'])
#         # if request.POST['submit'] == 'lucky':
#         #     return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
#         video_params = {
#             'key' : settings.YOUTUBE_DATA_API_KEY,
#             'part' : 'snippet,contentDetails',
#             'id' : ','.join(video_ids),
#             'maxResults' : 15,
#             'regionCode': 'iq'
#         }
#         r = requests.get(video_url, params=video_params)
#         results = r.json()['items']
#         for result in results:
#             video_data = {
#                 'title' : result['snippet']['title'],
#                 'id' : result['id'],
#                 'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
#                 'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
#                 'thumbnail' : result['snippet']['thumbnails']['high']['url'],
#                 'urlId': f'{ result["id"] }'
#             }
#             videos.append(video_data)
#             print(video_data['urlId'])
#     context = {
#         'videos' : videos
#     }
#     return render(request, 'search/index.html', context)
