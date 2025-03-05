<script lang="ts">
	import { getPositioner } from '$lib/slider.svelte.js';
	import { Button } from "$lib/components/ui/button/index.js";
	import * as Tooltip from "$lib/components/ui/tooltip/index.js";
	import { Play, Pause, SkipForward, SkipBack, Rewind, FastForward } from 'lucide-svelte';

	/** @type {{ data: any }} */
	let { data } = $props();

	// Wavesurfer instance
	let wavesurfer: any;
	const positioner = getPositioner();

	// Audio data
	const bbcAudiowf = data.data.audioWave.data;
	const audioSrc = `/audio-mp3/${data.data.audioId}.mp3`;
	
	// State variables
	let isPlaying = $state(false);
	let currentTime = $state(0);
	let duration = $state(0);
	let playbackRate = $state(1);

	// Format time as MM:SS
	function formatTime(timeInSeconds) {
		if (!timeInSeconds && timeInSeconds !== 0) return "0:00";
		const minutes = Math.floor(timeInSeconds / 60);
		const seconds = Math.floor(timeInSeconds % 60);
		return `${minutes}:${seconds.toString().padStart(2, '0')}`;
	}

	async function waveform(node: HTMLElement) {
		try {
			const { default: WaveSurfer } = await import('wavesurfer.js');

			wavesurfer = WaveSurfer.create({
				container: node,
				height: 80,
				waveColor: '#94a3b8', // slate-400
				progressColor: '#8b5cf6', // violet-500
				cursorColor: '#6b21a8', // purple-800
				cursorWidth: 2,
				mediaControls: false,
				minPxPerSec: 0.1,
				interact: true,
				dragToSeek: { debounceTime: 100 },
				autoScroll: true,
				media: document.querySelector('audio'),
				audioRate: playbackRate,
				peaks: [bbcAudiowf],
				plugins: [],
			});

			// Set up event listeners
			wavesurfer.on('ready', () => {
				duration = wavesurfer.getDuration();
			});

			wavesurfer.on('timeupdate', (currentTimeValue) => {
				currentTime = currentTimeValue;
				positioner.set(currentTimeValue);
			});

			wavesurfer.on('play', () => {
				isPlaying = true;
			});

			wavesurfer.on('pause', () => {
				isPlaying = false;
			});

			wavesurfer.on('finish', () => {
				isPlaying = false;
				currentTime = 0;
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

	// Playback controls
	function togglePlayback() {
		if (!wavesurfer) return;
		wavesurfer.playPause();
	}

	function skipBackward(seconds = 5) {
		if (!wavesurfer) return;
		const newTime = Math.max(0, currentTime - seconds);
		wavesurfer.setTime(newTime);
	}

	function skipForward(seconds = 15) {
		if (!wavesurfer) return;
		const newTime = Math.min(duration, currentTime + seconds);
		wavesurfer.setTime(newTime);
	}

	function setSpeed(speed) {
		if (!wavesurfer) return;
		playbackRate = speed;
		wavesurfer.setPlaybackRate(speed);
	}

	// Public method to jump to a specific timestamp
	export function jumpToTimestamp(seconds) {
		if (!wavesurfer) return;
		wavesurfer.setTime(seconds);
	}

	// Keyboard shortcuts
	function handleKeydown(event) {
		// Space key for play/pause
		if (event.code === 'Space' && !event.target.matches('input, textarea, [contenteditable]')) {
			event.preventDefault(); // Prevent page scrolling
			togglePlayback();
		}
		
		// Left arrow to skip back
		if (event.code === 'ArrowLeft' && !event.target.matches('input, textarea, [contenteditable]')) {
			event.preventDefault();
			skipBackward(5);
		}
		
		// Right arrow to skip forward
		if (event.code === 'ArrowRight' && !event.target.matches('input, textarea, [contenteditable]')) {
			event.preventDefault();
			skipForward(15);
		}
	}

	// Setup keyboard listener
	$effect(() => {
		window.addEventListener('keydown', handleKeydown);
		return () => {
			window.removeEventListener('keydown', handleKeydown);
		};
	});
</script>

<div class="flex flex-col gap-y-4 w-full max-w-4xl mx-auto">
	<!-- Hidden audio element -->
	<div class="hidden">
		<audio src={audioSrc}></audio>
	</div>

	<!-- Waveform visualization -->
	<div class="relative">
		<div class="h-[80px] rounded-lg bg-slate-100" use:waveform></div>
		
		<!-- Time indicators -->
		<div class="flex justify-between mt-1 text-sm text-slate-700">
			<span>{formatTime(currentTime)}</span>
			<span>{formatTime(duration)}</span>
		</div>
	</div>

	<!-- Controls -->
	<div class="flex items-center justify-between mt-2 gap-2">
		<!-- Play/Pause Button -->
		<Tooltip.Provider>
			<Tooltip.Root>
				<Tooltip.Trigger asChild>
					<Button 
						variant="default" 
						size="icon" 
						class="h-10 w-10 bg-purple-600 hover:bg-purple-700 text-white"
						onclick={togglePlayback}
					>
						{#if isPlaying}
							<Pause size={20} />
						{:else}
							<Play size={20} />
						{/if}
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content>
					<p>{isPlaying ? 'Pause' : 'Play'}</p>
				</Tooltip.Content>
			</Tooltip.Root>
		</Tooltip.Provider>

		<div class="flex items-center gap-1">
			<!-- Skip Back Button -->
			<Tooltip.Provider>
				<Tooltip.Root>
					<Tooltip.Trigger asChild>
						<Button 
							variant="outline" 
							size="icon" 
							class="h-9 w-9"
							onclick={() => skipBackward(5)}
						>
							<Rewind size={18} />
						</Button>
					</Tooltip.Trigger>
					<Tooltip.Content>
						<p>Rewind 5s</p>
					</Tooltip.Content>
				</Tooltip.Root>
			</Tooltip.Provider>

			<!-- Playback Speed Buttons -->
			<div class="flex gap-1 mx-2">
				{#each [1, 1.5, 2] as rate}
					<Button 
						variant={playbackRate === rate ? "default" : "outline"} 
						size="sm"
						class={playbackRate === rate ? "bg-slate-800" : ""}
						onclick={() => setSpeed(rate)}
					>
						{rate}x
					</Button>
				{/each}
			</div>

			<!-- Skip Forward Button -->
			<Tooltip.Provider>
				<Tooltip.Root>
					<Tooltip.Trigger asChild>
						<Button 
							variant="outline" 
							size="icon" 
							class="h-9 w-9"
							onclick={() => skipForward(15)}
						>
							<FastForward size={18} />
						</Button>
					</Tooltip.Trigger>
					<Tooltip.Content>
						<p>Forward 15s</p>
					</Tooltip.Content>
				</Tooltip.Root>
			</Tooltip.Provider>
		</div>
	</div>
</div>