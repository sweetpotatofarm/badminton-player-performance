import numpy as np
import csv
import cv2
import os
import sys
from moviepy.editor import VideoFileClip

# csv file name
print('csv file name?')
file_name = sys.stdin.readline()
file_name = file_name[:-1]
# video name
print('video name?')
video_name = sys.stdin.readline()
video_name = video_name[:-1]

# video length
clip = VideoFileClip(video_name)
video_length = clip.duration

# deal with csv file
csv_list = []
with open(file_name, newline='') as csvfile:
    csv_list = list(csv.reader(csvfile))
video_frame = len(csv_list)

# capture
vid_cap = cv2.VideoCapture(video_name)

# filter - Hit = Bot or Top
top_list=[]
bot_list=[]
for i in range(len(csv_list)):
    row = csv_list[i]
    if(row[4] == "Top"):
        top_list.append(csv_list[i])
    if(row[4] == "Bot"):
        bot_list.append(csv_list[i])

for row in top_list:
    for i in range(11, 15, 1):
        temp_str = row[i]
        s_str = temp_str.split(',')
        s_str[0] = s_str[0].split('[')
        s_str[1] = s_str[1].split(']')
        s_str[1][0] = s_str[1][0].split(' ')
        temp_list = []
        temp_list.append(s_str[0][1])
        temp_list.append(s_str[1][0][1])
        row[i] = temp_list

for row in bot_list:
    for i in range(11, 15, 1):
        temp_str = row[i]
        s_str = temp_str.split(',')
        s_str[0] = s_str[0].split('[')
        s_str[1] = s_str[1].split(']')
        s_str[1][0] = s_str[1][0].split(' ')
        temp_list = []
        temp_list.append(s_str[0][1])
        temp_list.append(s_str[1][0][1])
        row[i] = temp_list

del_num = []
for i in range(len(top_list)):
    if(top_list[i][11][0] == 0 and top_list[i][11][1] == 0):
        del_num.append(i)
for del_index in del_num:
    del top_list[del_index]
del_num = []
for i in range(len(bot_list)):
    # print(bot_list[i][13][0], bot_list[i][13][1])
    if(bot_list[i][13][0] == '0' and bot_list[i][13][1] == '0'):
        del_num.append(i)
for del_index in del_num:
    del bot_list[del_index]

# convert video to frame
def getFrame(sec):
    vid_cap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vid_cap.read()
    if hasFrames:
        cv2.imwrite("image"+str(count)+".jpg", image)
    return hasFrames

count = 1
frame_rate = (video_length/146)   # it will capture image in each (video_length/video_frame) second

# capture particular frame
for row in top_list:
    frame_num = int(row[0])
    getFrame(frame_num*frame_rate)
    img_name = "image" + str(count) + ".jpg"
    img = cv2.imread(img_name)
    top_box_lefttop = (int(row[11][0])-20, int(row[11][1])-20)
    top_box_rightbot = (int(row[12][0])+20, int(row[12][1])+20)
    bot_box_lefttop = (int(row[13][0])-20, int(row[13][1])-20)
    bot_box_rightbot = (int(row[14][0])+20, int(row[14][1])+20)

    # cut image   
    new_img = img[top_box_lefttop[1]:top_box_rightbot[1], top_box_lefttop[0]:top_box_rightbot[0]]
    cv2.imwrite("cut_image" + str(count) + "_top.jpg", new_img)

    # red rectangle image
    rectangle_color = (0, 0, 255)
    cv2.rectangle(img, top_box_lefttop, top_box_rightbot, rectangle_color, 2)
    cv2.rectangle(img, bot_box_lefttop, bot_box_rightbot, rectangle_color, 2)
    cv2.imwrite("new_image" + str(count) + "_top.jpg", img)

    count+=1
for row in bot_list:
    frame_num = int(row[0])
    getFrame(frame_num*frame_rate)
    img_name = "image" + str(count) + ".jpg"
    img = cv2.imread(img_name)
    top_box_lefttop = (int(row[11][0])-20, int(row[11][1])-20)
    top_box_rightbot = (int(row[12][0])+20, int(row[12][1])+20)
    bot_box_lefttop = (int(row[13][0])-20, int(row[13][1])-20)
    bot_box_rightbot = (int(row[14][0])+20, int(row[14][1])+20)

    # cut image   
    new_img = img[bot_box_lefttop[1]:bot_box_rightbot[1], bot_box_lefttop[0]:bot_box_rightbot[0]]
    cv2.imwrite("cut_image" + str(count) + "_bot.jpg", new_img)

    # red rectangle image
    rectangle_color = (0, 0, 255)
    cv2.rectangle(img, top_box_lefttop, top_box_rightbot, rectangle_color, 2)
    cv2.rectangle(img, bot_box_lefttop, bot_box_rightbot, rectangle_color, 2)
    cv2.imwrite("new_image" + str(count) + "_bot.jpg", img)
    count+=1

for i in range(1, count, 1):
    os.remove("image" + str(i) + ".jpg")

# convert frame to 1 sec video
vid_count = 1
for row in top_list:
    frame_list = []
    frame_num = int(row[0])
    for i in range(frame_num-10, frame_num+10, 1):
        getFrame(i*frame_rate)
        img_name = "image" + str(count) + ".jpg"
        img = cv2.imread(img_name)
        height, width, layers = img.shape
        size = (width,height)
        frame_list.append(img)
        count+=1
    pathOut = "video" + str(vid_count) + "_top.avi"
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), 20, size)
    for i in range(len(frame_list)):
        # writing to a image array
        out.write(frame_list[i])
    out.release()

    frame_list = []
    frame_num = int(row[0])
    top_box_lefttop = (int(row[11][0])-20, int(row[11][1])-20)
    top_box_rightbot = (int(row[12][0])+20, int(row[12][1])+20)
    for i in range(frame_num-10, frame_num+10, 1):
        getFrame(i*frame_rate)
        img_name = "image" + str(count) + ".jpg"
        img = cv2.imread(img_name)
        new_img = img[top_box_lefttop[1]:top_box_rightbot[1], top_box_lefttop[0]:top_box_rightbot[0]]
        height, width, layers = new_img.shape
        size = (width,height)
        frame_list.append(new_img)
        count+=1
    pathOut = "video" + str(vid_count) + "_cut_top.avi"
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), 20, size)
    for i in range(len(frame_list)):
        # writing to a image array
        out.write(frame_list[i])
    out.release()

    for i in range(count-40, count, 1):
        os.remove("image" + str(i) + ".jpg")

    vid_count+=1

for row in bot_list:
    frame_list = []
    frame_num = int(row[0])
    for i in range(frame_num-10, frame_num+10, 1):
        getFrame(i*frame_rate)
        img_name = "image" + str(count) + ".jpg"
        img = cv2.imread(img_name)
        height, width, layers = img.shape
        size = (width,height)
        frame_list.append(img)
        count+=1
    pathOut = "video" + str(vid_count) + "_bot.avi"
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), 20, size)
    for i in range(len(frame_list)):
        # writing to a image array
        out.write(frame_list[i])
    out.release()

    frame_list = []
    frame_num = int(row[0])
    bot_box_lefttop = (int(row[13][0])-20, int(row[13][1])-20)
    bot_box_rightbot = (int(row[14][0])+20, int(row[14][1])+20)
    for i in range(frame_num-10, frame_num+10, 1):
        getFrame(i*frame_rate)
        img_name = "image" + str(count) + ".jpg"
        img = cv2.imread(img_name)
        new_img = img[bot_box_lefttop[1]:bot_box_rightbot[1], bot_box_lefttop[0]:bot_box_rightbot[0]]
        height, width, layers = new_img.shape
        size = (width,height)
        frame_list.append(new_img)
        count+=1
    pathOut = "video" + str(vid_count) + "_cut_bot.avi"
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), 20, size)
    for i in range(len(frame_list)):
        # writing to a image array
        out.write(frame_list[i])
    out.release()

    for i in range(count-40, count, 1):
        os.remove("image" + str(i) + ".jpg")

    vid_count+=1