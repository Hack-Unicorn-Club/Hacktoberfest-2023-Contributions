from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import json
import os
import random


video_titles = ["Did you know this? 🤯", "That's CRAZY! 😲", "Comment if you already knew! ⬇", "Woah! 😮", ]
video_description = '#youtube, #video, #vlog, #live, #life, #funny, #trending, #comedy, #entertainment, #music, #viral, #challenge, #dance, #reaction, #prank, #beauty, #fashion, #lifestyle, #food, #animals, #sports, #gaming, #howto, #diy, #technology, #musicvideo, #cover, #acoustic, #pop, #rock, #hiphop, #country, #dancevideo, #funnyvideo, #comedyvideo, #musicreaction, #prankvideo, #beautyvideo, #fashionvideo, #lifestylevideo, #foodvideo, #animalvideo, #sportsvideo, #gamingvideo, #howtovideo, #diyvideo, #technologyvideo, #news, #politics, #sports, #entertainment, #science, #technology, #business, #education, #travel, #food, #fashion, #beauty, #cars, #videogames, #movies, #music, #art, #lifestyle, #health, #fitness, #parenting, #relationships, #self-improvement, #travel, #food, #fashion, #beauty, #home, #garden, #diy, #crafts, #photography, #videography, #music, #art, #books, #movies, #tv, #podcasts, #games, #sports, #technology, #business, #education, #news, #politics, #science, #nature, #animals, #space, #history, #culture, #religion, #philosophy, #mindfulness, #meditation, #yoga, #wellness, #self-care, #love, #happiness, #peace, #gratitude, #inspiration, #motivation, #growth, #success, #dreams, #goals, #future, #life, #love crazy facts, insane facts, facts, fun facts, weird facts, interesting facts, unbelievable facts, mind-blowing facts, trivia, knowledge, learning, education, entertainment, humor, surprise, shock, amazement, curiosity, wonder, awe, inspiration, motivation, growth, success, dreams, goals, future, life, love, animal facts, science facts, history facts, geography facts, math facts, technology facts, pop culture facts, celebrity facts, sports facts, news facts, politics facts, religion facts, philosophy facts, educational, informative, learning, knowledge, mind-blowing, surprising, shocking, amazing, curious, wonderful, awe-inspiring, motivational, inspiring, growth, success, dreams, goals, future, life, love, animal, science, history, geography, math, technology, pop culture, celebrity, sports, news, politics, religion, philosophy #crazyfacts, #insanefacts, #facts, #funfacts, #weirdfacts, #interestingfacts, #unbelievablefacts, #mindblowingfacts, #trivia, #knowledge, #learning, #education, #entertainment, #humor, #surprise, #shock, #amazement, #curiosity, #wonder, #awe, #inspiration, #motivation, #growth, #success, #dreams, #goals, #future, #life, #love, #animalfacts, #sciencefacts, #historyfacts, #geographyfacts, #mathfacts, #technologyfacts, #popculturefacts, #celebrityfacts, #sportsfacts, #newsfacts, #politicsfacts, #religionfacts, #philosophyfacts, #educational, #informative, #learning, #knowledge, #mindblowing, #surprising, #shocking, #amazing, #curious, #wonderful, #aweinspiring, #motivational, #inspiring, #growth, #success, #dreams, #goals, #future, #life, #love, #animal, #science, #history, #geography, #math, #technology, #popculture, #celebrity, #sports, #news, #politics, #religion, #philosophy'
video_tags = "crazy facts, insane facts, facts, fun facts, weird facts, interesting facts, unbelievable facts, trivia knowledge, learning, education, entertainment, surprise, amazement, curiosity, wonder, inspiration, motivation, growth, success, dreams, goals, future, life, love, animal facts, science facts, history facts, geography facts, math facts, technology facts, celebrity facts, sports facts, news facts, philosophy facts".split(",")

credentials_file = "./mulkshortsmaker-62ebde0e50a2.json"
credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
youtube = build('youtube', 'v3', credentials=credentials)


no = 1
for video in os.listdir("./out")[0:5]:
    request_body = {
        'snippet': {
            'title': random.choice(video_titles) + " #shorts " + str(no),
            'description': video_description,
            'tags': video_tags,
            'categoryId': '27',
            'channelID': 'UCTkgKWM1tydV1_mL6PNsqSg'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }
    
    media = MediaFileUpload(f"./out/{video}.mp4")
    videos_insert_response = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    ).execute()
    
    print(f'Video uploaded! Video URL: https://youtube.com/watch?v={videos_insert_response["id"]}')
    no += 1
