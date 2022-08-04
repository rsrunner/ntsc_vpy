import sys
sys.path.append(r"C:\everything\docs\repo\ntsc")
import ntsc_vpy
import vapoursynth as vs

core = vs.core
clip = core.ffms2.Source(source=r"C:\everything\vids\vpy\woodyvpy.vpy - 8489.png")
#clip = core.std.CropAbs(clip, 1440, 1080, (1920/2)-(1440/2))

if clip.format.color_family == vs.ColorFamily.RGB:
	clip = core.resize.Lanczos(clip, format=vs.RGB24, width=720, height=486)
else:
	clip = core.resize.Lanczos(clip, format=vs.RGB24, matrix_in_s="709", width=720, height=486)

clip = ntsc_vpy.Ntsc(
	clip=clip,
	emulating_vhs = True,
	vhs_head_switching = True,
	ringing = .5,
	video_chroma_loss = 20,
	video_chroma_phase_noise = 10,
	video_chroma_noise = 20,
	freq_noise_size = .9,
	enable_ringing2 = True,
	color_bleed_horiz = 2,
	color_bleed_vert = 0,
	vhs_edge_wave = 2
)

clip = core.resize.Lanczos(clip, format=vs.YUV420P8, matrix_s="709", width=720, height=540)

clip.set_output()