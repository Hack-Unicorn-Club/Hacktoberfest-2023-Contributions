import asyncio
import csv
import os
import json
import random
from moviepy.editor import VideoFileClip, TextClip, AudioFileClip, CompositeVideoClip, ColorClip
import aiohttp


config = json.load(open("./config.json", "r"))


async def get_stock_video():
    """
        Generates and downloads a random 9:16 stock video locally using the Pexels API.
    """
    
    headers = {"Authorization": config["PEXELS_API_KEY"]}
    params = {"query": "sunset",
              "orientation": "portrait", 
              "per_page": 50,
              "size" : "medium"
              }
    video_duration_threshold = 9
       
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.pexels.com/videos/search", headers=headers, params=params) as response:
                data = await response.json()
                videos = data["videos"]
                random_video = random.choice(videos)
                video_url = random_video["video_files"][0]["link"]
                if random_video["duration"] >= video_duration_threshold:
                    async with session.get(video_url) as video_response:
                        with open("background_video.mp4", "wb") as video_file:
                            while True:
                                chunk = await video_response.content.read(1024)
                                if not chunk:
                                    break
                                video_file.write(chunk)
                    break
                else:
                    continue
    return "background_video.mp4"


async def make_short(title : str, content: str, social_media_handle: str, filename : str):
    """
    Makes the short and saves it locally.

    Args:
        title (str): The title of the Shorts/Reel
        content (str): The content of the Shorts/Reel
        social_media_handle (str): The social media handle of the account
        filename (str): The name of the file which will get saved
    Returns:
        path (str): Path of the Short/Reel generated
    """
    
    video = VideoFileClip(await get_stock_video()).resize(height=1280, width=720)
    video = video.without_audio()
    video_duration = 9
    video = video.subclip(0, video_duration)
    
    audio_clips = os.listdir("./audio")
    audio = AudioFileClip("./audio/" + random.choice(audio_clips))
    video = video.set_audio(audio)
    video.set_duration(video_duration)
    video.resize(height=1280, width=720)
    video_width, video_hieght = video.size
    
    heading_text = \
                TextClip(title,
                            method="caption",
                            size = (video_width/1.1, video_hieght/1.1),
                            fontsize=85, 
                            font="./fonts/Geomatrix Bold.ttf", 
                            color="white", 
                            align="North",
                            stroke_color="black",
                            stroke_width=1
                        ).set_position((32, 350))
    heading_text.set_duration(video_duration)
    heading_text.on_color(color = [0,0,0], col_opacity = 0.2, size=(heading_text.w, heading_text.h))
    background_clip = ColorClip(size=(video_width, video_hieght), color=[0,0,0], ismask=False).set_opacity(0.3)
    heading_text = CompositeVideoClip([background_clip, heading_text])
    
    main_text = \
                TextClip(content,
                            method="caption",
                            size = (video_width/1.1, video_hieght/1.1),
                            fontsize=40,
                            font="./fonts/Geomatrix Medium.ttf",
                            color="white",
                            align="center"
                        ).set_position((32, 0))\
                         .set_start(7.8)

    main_text.set_duration(video_duration)

    social_media_handle_text = \
                TextClip(f"Follow For More\n@{social_media_handle}",
                            method="caption",
                            size = (video_width/1.1, video_hieght/1.1),
                            fontsize=30,
                            font="./fonts/Geomatrix Medium.ttf", 
                            color="white",
                            align="South",
                        )\
                .set_position(("center", -150))
    social_media_handle_text.set_duration(video_duration)

    video_with_text = CompositeVideoClip([video,
                                          heading_text,
                                          main_text,
                                          social_media_handle_text
                                        ])
    video_with_text = video_with_text.set_duration(video_duration) \
                                     .set_audio(audio) \
                                     .resize(height=1280, width=720)

    video_with_text.write_videofile(f"./out/{filename}.mp4", codec="libx264", audio=True, bitrate='20000k')
    
    shorts_vid = f"./out/{filename}"
    return shorts_vid


async def make_bulk_shorts(title : str, content_list: list, social_media_handle: str) -> None:
    """
    Creates bulk Shorts/Reels and saves them locally

    Args:
        title (str): The title of the Shorts/Reel
        content_list (list): The content of the Shorts/Reel
        social_media_handle (str): The social media handle of the account
    """
    
    for i in range(len(content_list)):
        await make_short(title=title, content=content_list[i],social_media_handle=social_media_handle, filename=f"{i+1}.mp4")
        print(f"Successfully generated Short/Reel #{i+1}.")
    
    print(f"Successfully generated all Shorts/Reels ({len(content_list)}).")


def extract_column(csv_file : str, column_index : int) -> list:
    """
    Extracts the entire column of a csv file and returns a list.

    Args:
        csv_file (str): Path of the csv file
        column_index (int): Index of the column, which is to be extracted

    Returns:
        list: The list of all the items which were in the column.
    """
    
    result = []
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > column_index:
                result.append(row[column_index])

    return result


if __name__ == "__main__":
    csv_file_path = "./general-facts.csv"
    column_index = 1
    content_list = extract_column(csv_file=csv_file_path, column_index=column_index)
    asyncio.run(make_bulk_shorts(title="Did You Know?", content_list=content_list, social_media_handle="factfinityy"))
