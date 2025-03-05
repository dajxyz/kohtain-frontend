<script lang="ts">
	import { getPositioner } from '$lib/slider.svelte.js';
	import PauseIcon from 'lucide-svelte/icons/pause';
	import PlayIcon from 'lucide-svelte/icons/play';
	import Button from '$lib/components/ui/button/button.svelte';
	import * as Tooltip from "$lib/components/ui/tooltip/index.js";
	import { Badge } from "$lib/components/ui/badge/index.js";


	/** @type {{ data: string }} */
	let data = $props();

	let wavesurfer: any;
	const positioner = getPositioner();

	const bbcAudiowf = data.data.audioWave.data;
	const audioSrc = `/audio-mp3/${data.data.audioId}.mp3`; // Define the audio source
	let isPlaying = $state(false);
	let currentPlaybackPosition = $state(0);
	let audioDuration = $state(0);
	let playbackRate = $state(1);

	function formatTime(timeInSeconds: number) {
		if (!timeInSeconds && timeInSeconds !== 0) return "0:00";
		const minutes = Math.floor(timeInSeconds / 60);
		const seconds = Math.floor(timeInSeconds % 60);
		return `${minutes}:${seconds.toString().padStart(2, '0')}`;
	}

	// let's check that we have the right variable
	const wavesurfer_audio_id = data.data.audioId;
	// console.log('/// ');
	// console.log('/// ');
	// console.log('/// ');
	// console.log('/// ');

	// console.log('wavesurfer_audio_id is:', wavesurfer_audio_id);
	// console.log("wavesurfer waveform looks like :", bbcAudiowf)

	// console.log('wavesurfer.svelte / audiowave.version', bbcAudiowf.version);
	// console.log('wavesurfer.svelte / audiowave.channels', bbcAudiowf.channels);
	// console.log('wavesurfer.svelte / audiowave.sample_rate', bbcAudiowf.sample_rate);
	// console.log('wavesurfer.svelte / audiowave.samples_per_pixel', bbcAudiowf.samples_per_pixel);
	// console.log('wavesurfer.svelte / audiowave.bits', bbcAudiowf.bits);
	// console.log('wavesurfer.svelte / audiowave.length', bbcAudiowf.length);

	async function waveform(node: any) {
		try {
			const { default: WaveSurfer } = await import('wavesurfer.js');

			wavesurfer = WaveSurfer.create({
				container: node, // Use the actual DOM node
				height: 50,
				waveColor: '#1c1d1b',
				progressColor: ['#eb9770', '#b73b43', '#610826'],
				mediaControls: false,
				minPxPerSec: 0.1,
				interact: true,
				dragToSeek: { debounceTime: 100 },
				autoScroll: true,
				media: document.querySelector('audio'),
				audioRate: 1,
				peaks: [bbcAudiowf],
				plugins: [],
			});

			wavesurfer.on('ready', () => {
				audioDuration = wavesurfer.getDuration();
				console.log("this was triggered")
				console.log(audioDuration)
			});

			wavesurfer.on('timeupdate', (currentTime: number) => {
				currentPlaybackPosition = currentTime;
				positioner.set(currentTime);
				// audioDuration = wavesurfer.getDuration(); // this was excessive
				// console.log(currentTime) 
			});

			// Listen for play/pause events to update our isPlaying state
			wavesurfer.on('play', () => {
				isPlaying = true;
			});

			wavesurfer.on('pause', () => {
				isPlaying = false;
			});

			// Also handle the end of the track
			wavesurfer.on('finish', () => {
				isPlaying = false;
				// console.log('finnished');
			});
			// Return a cleanup function
			return {
				destroy() {
					if (wavesurfer) {
						wavesurfer.destroy();
					}
				}
			};
		} catch (error) {
			console.error('Failed to initialize wavesurfer:', error);
		}
	}

	function skipBack(seconds = 5) {
		if (!wavesurfer) return;
		const newTime = Math.max(0, currentPlaybackPosition - seconds);
		console.log("rwrw currentPlaybackPosition", currentPlaybackPosition);
		wavesurfer.setTime(newTime);
	}

	function skipForward(seconds = 5) {
		if (!wavesurfer) return;
		const newTime = Math.min(audioDuration, currentPlaybackPosition + seconds);
		console.log("skip ff audioduration", currentPlaybackPosition);
		console.log("skip ff audioduration", audioDuration);
		wavesurfer.setTime(newTime);
	}


	function togglePlayback() {
		if (!wavesurfer) return;
		wavesurfer.playPause();
	}

	function setSpeed(speed: number) {
		if (!wavesurfer) return;
		playbackRate = speed;
		wavesurfer.setPlaybackRate(speed);
	}


	export function jumpToTimestamp(seconds: number) {
		if (!wavesurfer) return;
		// console.log('wavesurfer_control jumpToTimestamp');
		wavesurfer.setTime(seconds + 0.5);
	}

	function debugButton() {
		if (!wavesurfer) return;
		// console.log('isSeeking', wavesurfer.isSeeking());
		// console.log('isPlaying', wavesurfer.isPlaying());
		// console.log('getVolume', wavesurfer.getVolume());
		// console.log('getSrc', wavesurfer.getSrc());
		// console.log('getScroll', wavesurfer.getScroll());
		// console.log('getPlaybackRate', wavesurfer.getPlaybackRate());
		// console.log('getDuration', wavesurfer.getDuration());
		// console.log('getPlaybackRate', wavesurfer.getPlaybackRate());
	}

	function handleKeydown(event) {
		// Space key for play/pause
		if (event.code === 'Space' && !event.target.matches('input, textarea, [contenteditable]')) {
			event.preventDefault(); // Prevent page scrolling
			if (wavesurfer) {
				wavesurfer.playPause();
			}
		}

		if (event.code === 'ArrowLeft' && !event.target.matches('input, textarea, [contenteditable]')) {
			event.preventDefault();
			skipBack(5);
		}
		
		// Right arrow to skip forward
		if (event.code === 'ArrowRight' && !event.target.matches('input, textarea, [contenteditable]')) {
			event.preventDefault();
			skipForward(5);
		}
	}

	// Setup keyboard listener when component mounts
	$effect(() => {
		window.addEventListener('keydown', handleKeydown);
		// Cleanup when component unmounts
		return () => {
			window.removeEventListener('keydown', handleKeydown);
		};
	});

	// display podcast details etc.

	// console.log('wavesurfer.svelte / thisPodcast', thisPodcast);
	// console.log('wavesurfer.svelte / thisPodcast.name', thisPodcast.name);
	// console.log('wavesurfer.svelte / thisPodcast.date', thisPodcast.date);
	// console.log('wavesurfer.svelte / thisPodcast.subject', thisPodcast.subject);

	// console.log('wavesurfer.svelte / thispodcast', thisPodcast);


	// Initialize wavesurfer here or call a function to refresh it
</script>

<div class="flex-col gap-y-8">
	<div class="mb-4 rounded-lg bg-none">
		<audio class="rounded-lg" src={audioSrc}></audio>
	</div>

	<div class="relative">
		<div class="h-[55px] rounded-lg" use:waveform>
			<div id="time" class="left-0 absolute top-1/2 p-1 -translate-y-1/2 -mt-1 font-mono" style="z-index: 20">
				<Badge variant="secondary" class="font-normal">{formatTime(currentPlaybackPosition)}</Badge></div>
    		<div id="duration" class="right-0 absolute z-index: 400 top-1/2 p-1 -translate-y-1/2 -mt-1 font-mono" style="z-index: 20">
				<Badge variant="secondary" class="font-normal">{formatTime(audioDuration)}</Badge> </div>
		</div>
	</div></div>

<div class="flex items-center justify-between mt-2 gap-8">
	<!-- Play/Pause Button -->

				<Button 
					variant="outline" 
					size="sm" 
					class="w-24 "
					onclick={togglePlayback}
				>
					{#if isPlaying}
					<PauseIcon size={20} />
					{:else}
					<PlayIcon size={20} />
					{/if}
				</Button>

	<div class="flex items-center gap-x-4">
		<!-- Skip Back Button -->
		<!-- Skip Forward Button -->
		<div class="flex flex-row">
			<Tooltip.Provider>
			<Tooltip.Root>
				<Tooltip.Trigger>
					<Button 
					class="hidden lg:block w-20"
						variant="outline" 
						size="sm" 
						onclick={() => skipBack(30)}
					>
						-30s
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content>
					<p>- 30s</p>
				</Tooltip.Content>
			</Tooltip.Root>
		</Tooltip.Provider>
		
		<!-- Skip Forward Button -->
		<Tooltip.Provider>
			<Tooltip.Root>
				<Tooltip.Trigger>
					<Button 
						variant="outline" 
						size="sm" 
						onclick={() => skipBack(5)}
					>
						-5s
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content>
					<p>- 5s</p>
				</Tooltip.Content>
			</Tooltip.Root>
		</Tooltip.Provider>
		</div>

		<!-- Playback Speed Buttons -->
		<div class="flex gap-x-1 mx-2">
			{#each [1, 1.5, 2] as rate}
				<Button 
					variant="outline" 
					size="sm"
					class={playbackRate === rate ? "bg-accent active:bg-stone-300" : " active:bg-stone-300"}
					onclick={() => setSpeed(rate)}
				>
					{rate}x
				</Button>
			{/each}
		</div>

		<div class="flex flex-row">
		<!-- Skip Forward Button -->
		<Tooltip.Provider>
			<Tooltip.Root>
				<Tooltip.Trigger>
					<Button 
						variant="outline" 
						size="sm" 
						onclick={() => skipForward(5)}
					>
						+5s
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content>
					<p>+ 5s</p>
				</Tooltip.Content>
			</Tooltip.Root>
		</Tooltip.Provider>
		
		<!-- Skip Forward Button -->
		<Tooltip.Provider>
			<Tooltip.Root>
				<Tooltip.Trigger>
					<Button 
						class="hidden lg:block w-20"
						variant="outline" 
						size="sm" 
						onclick={() => skipForward(30)}
					>
						+30s
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content>
					<p>+ 30s</p>
				</Tooltip.Content>
			</Tooltip.Root>
		</Tooltip.Provider>
	</div>
	</div>
</div>
