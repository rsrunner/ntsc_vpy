from ntsc import Ntsc, random_ntsc, NumpyRandom
from PIL import Image
import numpy as np
import cv2
import os, sys
cool = sys.argv[1]
resize = (720, 486) # 720p 486 lines
sourceimg = Image.open(cool).convert('RGB').resize(resize)
ntobj = Ntsc(random=NumpyRandom(1024)) # Create Ntsc object
# Thine's All-Time Preset
ntobj._emulating_vhs = True
ntobj._vhs_head_switching = True
ntobj._ringing = .2
ntobj._video_chroma_loss = 10
ntobj._video_chroma_phase_noise = 10
ntobj._video_chroma_noise = 10
ntobj._freq_noise_size = .9
ntobj._enable_ringing2 = True
ntobj._color_bleed_horiz = 2
ntobj._color_bleed_vert = 0
ntobj._vhs_edge_wave = 2
# ntobj = random_ntsc()

ndarray = np.array(sourceimg) # Convert to numpy array
print(ndarray.dtype)
ndarray = cv2.cvtColor(ndarray, cv2.COLOR_RGB2BGR)

for i in range(2):
	ndarray = ntobj.composite_layer(ndarray, ndarray, field=i, fieldno=i)

ndarray = cv2.cvtColor(ndarray, cv2.COLOR_BGR2RGB)
outimg = Image.fromarray(ndarray)

outcool = os.path.splitext(cool)
outimg.save(outcool[0]+"_vhs"+outcool[1])