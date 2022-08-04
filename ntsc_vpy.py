import ntsc, cv2
import numpy as np
import vapoursynth as vs

def Ntsc(
	clip,
	composite_preemphasis_cut = 1000000.0,
	composite_preemphasis = 0.0,
	vhs_out_sharpen = 1.5,
	vhs_edge_wave = 0,
	vhs_head_switching = False,
	vhs_head_switching_point = 1.0 - (4.5 + 0.01) / 262.5,
	vhs_head_switching_phase = (1.0 - 0.01) / 262.5,
	vhs_head_switching_phase_noise = 1.0 / 500 / 262.5,
	color_bleed_before = True,
	color_bleed_horiz = 0,
	color_bleed_vert = 0,
	ringing = 1.0,
	enable_ringing2 = False,
	ringing_power = 2,
	ringing_shift = 0,
	freq_noise_size = 0,
	freq_noise_amplitude = 2,
	composite_in_chroma_lowpass = True,
	composite_out_chroma_lowpass = True,
	composite_out_chroma_lowpass_lite = True,
	video_chroma_noise = 0,
	video_chroma_phase_noise = 0,
	video_chroma_loss = 0,
	video_noise = 2,
	subcarrier_amplitude = 50,
	subcarrier_amplitude_back = 50,
	emulating_vhs = False,
	nocolor_subcarrier = False,
	vhs_chroma_vert_blend = True,
	vhs_svideo_out = False,
	output_ntsc = True,
	video_scanline_phase_shift = 180,
	video_scanline_phase_shift_offset = 0,
	output_vhs_tape_speed = ntsc.VHSSpeed.VHS_SP,
	seed = 1024
):
	core = vs.core
	assert clip.format.color_family == vs.ColorFamily.RGB, "This clip isn't in RGB"
	_ntsc = ntsc.Ntsc(random=ntsc.NumpyRandom(seed))
	attributes = {x: y for (x, y) in vars().items() if "_"+x in dir(_ntsc)}
	for x, y in attributes.items():
		setattr(_ntsc, "_"+x, y) 
	def crapify(n, f):
		vsframe = f.copy()
		ndarray = np.dstack([np.asarray(vsframe[i]) for i in range(3)])
		ndarray = cv2.cvtColor(ndarray, cv2.COLOR_RGB2BGR)
		for i in range(2):
			ndarray = _ntsc.composite_layer(ndarray, ndarray, field=i, fieldno=i)
		ndarray = cv2.cvtColor(ndarray, cv2.COLOR_BGR2RGB)
		print(ndarray)
		[np.copyto(np.asarray(vsframe[i]), ndarray[:, :, i]) for i in range(3)]
		return vsframe
	return core.std.ModifyFrame(clip, clip, crapify)