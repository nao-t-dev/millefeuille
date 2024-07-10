#!/usr/bin/env python
# -*- coding: utf8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os,sys
import glob
from PIL import Image
from itertools import product
from functools import partial

def loadInputPath():
  inputDir = os.path.abspath(os.path.dirname(__file__))
  inputDirPath = filedialog.askdirectory(initialdir = inputDir)
  inputString.set(inputDirPath)

def loadOutputPath():
  outputDir = os.path.abspath(os.path.dirname(__file__))
  outputDirPath = filedialog.askdirectory(initialdir = outputDir)
  outputString.set(outputDirPath)

def close():
  app.quit()

def generate(saveType):
  inputPathtoGen = input_path_textbox.get() + '/**/'
  outputPathtoGen = output_path_textbox.get()
  conpressRate = compress_rate_textbox.get()
  if inputPathtoGen != '' and outputPathtoGen != '':
    input_dir_list = glob.glob(inputPathtoGen)
    input_dir_list.sort()
    input_dir_list_path_ary = []
    for i, dirpath in enumerate(input_dir_list):
      tmp_list = glob.glob(dirpath + '/*.png')
      if len(tmp_list) > 0:
        tmp_list.sort()
        input_dir_list_path_ary.append(tmp_list)

    dir_count = len(input_dir_list_path_ary)
    generate_path_ary = []
    generate_path_ary = list(product(*input_dir_list_path_ary))
    image_count = 0
    for i, path_list in enumerate(generate_path_ary):
      result_image = Image.open(path_list[0]).convert("RGBA")
      filename = os.path.splitext(os.path.basename(path_list[0]))[0]
      for i, path in enumerate(path_list):
        if i < len(path_list) - 1:
          paste_image = Image.open(path_list[i + 1]).convert("RGBA")
          result_image.paste(paste_image, (0, 0), paste_image)
          filename += os.path.splitext(os.path.basename(path_list[i + 1]))[0]

      os.makedirs(outputPathtoGen + '/output', exist_ok=True)

      if saveType == 'jpg':
        result_image_resized = result_image.resize((result_image.size[0], result_image.size[1]), Image.LANCZOS)
        result_image_resized = result_image_resized.convert('RGB')
        result_image_resized.save(outputPathtoGen + '/output/' + filename + '.jpg', "JPEG", quality= int(conpressRate))

      elif saveType == 'png':
        result_image = result_image.save(outputPathtoGen + '/output/' + filename + '.png', quality=100)

      image_count += 1

app = Tk()
app.geometry("460x250")
app.title("millefeuille / ミルフィーユ")

input_path_label = Label(
  app,
  text="元となる画像フォルダ"
)
inputString = StringVar()
inputString.set(os.path.abspath(os.path.dirname(__file__)) + '/input')
input_path_textbox = Entry(textvariable=inputString, width=40)

input_path_load_btn = Button(
  app,
  width=5,
  height=1,
  text="参照",
  command=loadInputPath
)

output_path_label = Label(
  app,
  text="出力先"
)
outputString = StringVar()
outputString.set(os.path.abspath(os.path.dirname(__file__)))
output_path_textbox = Entry(textvariable=outputString, width=40)

output_path_load_btn = Button(
  app,
  width=5,
  height=1,
  text="参照",
  command=loadOutputPath
)

compress_rate_label = Label(
  app,
  text="圧縮率（0-100）"
)
compressRate = StringVar()
compressRate.set('100')
compress_rate_textbox = Entry(textvariable=compressRate, width=10)

generate_btn = Button(
  app,
  width=12,
  height=2,
  text="pngで生成する",
  # command=generate("png")
  command=partial(generate, "png")
)

generate_jpg_btn = Button(
  app,
  width=12,
  height=2,
  text="jpgで生成する",
  # command=generate("jpg")
  command=partial(generate, "jpg")
)

quit_btn = Button(
  app,
  width=5,
  height=1,
  text="終了",
  command=close
)

input_path_label.grid(column=0,columnspan=3,row=0,padx=10,pady=5)
input_path_textbox.grid(column=0,columnspan=3,row=1,padx=10)
input_path_load_btn.grid(column=3,columnspan=1,row=1,padx=10)

output_path_label.grid(column=0,columnspan=3,row=2,padx=10,pady=5)
output_path_textbox.grid(column=0,columnspan=3,row=3,padx=10)
output_path_load_btn.grid(column=3,columnspan=1,row=3,padx=10)

compress_rate_label.grid(column=1,columnspan=1,row=4,padx=10,pady=5)
compress_rate_textbox.grid(column=1,columnspan=1,row=5,padx=10)

generate_jpg_btn.grid(column=1,columnspan=1,row=6,padx=10,pady=5)
generate_btn.grid(column=2,columnspan=1,row=6,padx=10,pady=5)

# quit_btn.grid(column=0,columnspan=4,row=7,padx=10,pady=5)

app.mainloop()
