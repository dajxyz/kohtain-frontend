<script lang="ts">
	import * as bbcAudioWaveform from '$lib/components/waveforms/1000690745960.json';
	import { getPositioner } from '$lib/slider.svelte.js';
	const positioner = getPositioner();
	let wavesurfer;
	let currentPlaybackPosition = $state(0);
    console.log(bbcAudioWaveform.data)

	let data = $props();
	let kuuid = data.data;
	console.log('inside wavesurfer control kuuid:', kuuid);

	const bbcAudiowf = bbcAudioWaveform.data;
	// const audio = '912a1f3f-b4cc-c8e6-62cd-5d8b201559db.mp3';
	// const video = "/video/ec9a3affab3c48dce93077ef6d621487.mp4";

	async function waveform(node) {
		const { default: WaveSurfer } = await import('wavesurfer.js');

		wavesurfer = WaveSurfer.create({
			container: 'div#waveform',
			height: 150,
			waveColor: '#cdcdcd',
			progressColor: '#639DA8',
			mediaControls: false,
			minPxPerSec: 0.1,
			interact: true,
			dragToSeek: true,
			autoScroll: true,
			media: document.querySelector('video'),
			audioRate: 1,
			peaks: [bbcAudiowf],
			duration: 2340,
			plugins: [
				// Register the plugin
			]
		});

// 		document.querySelector('input[type="checkbox"]').addEventListener('change', (e) => {
//   preservePitch = e.target.checked
//   wavesurfer.setPlaybackRate(wavesurfer.getPlaybackRate(), preservePitch)
// })

		// wavesurfer.load(video);

		// wavesurfer.on('timeupdate', (currentTime) => {

		//     console.log('control_component', currentPlaybackPosition + 's');
		wavesurfer.on('timeupdate', (currentTime) => {
			// console.log(currentTime);
			currentPlaybackPosition = currentTime;
			positioner.set(currentTime);

			// wavesurfer.registerPlugin(
			// 	ZoomPlugin.create({
			// 		// the amount of zoom per wheel step, e.g. 0.5 means a 50% magnification per scroll
			// 		scale: 0.5,
			// 		// Optionally, specify the maximum pixels-per-second factor while zooming
			// 		maxZoom: 50,
			// 	})
			// );
		});
	}

	function playTrack() {
		wavesurfer.play();
	}

	function pauseTrack() {
		wavesurfer.pause();
	}
</script>

<div class="flex-col gap-y-8">
	<div><h1>Военная приемка | Высшая школа ВДВ | Rutube</h1></div>
	<div class="mb-4 rounded-lg bg-black">
		<audio
			class="rounded-lg"
			src="/audio-wav/1000690745960.wav"
			controls
			playsinline
			style="width: 100%; margin: 0 auto; display: block;"
		></audio>
	</div>
	
	<div class=" shrink rounded-lg bg-black" id="waveform" use:waveform={video}></div>
</div>
<hr />
