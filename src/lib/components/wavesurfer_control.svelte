<script lang="ts">

	import { getPositioner } from '$lib/slider.svelte.js';
	import PauseIcon from 'lucide-svelte/icons/pause';
	import PlayIcon from 'lucide-svelte/icons/play';
	import Button from '$lib/components/ui/button/button.svelte';


	/** @type {{ data: string }} */
	let data = $props();

	let wavesurfer: any;
	let currentPlaybackPosition = $state(0);
	const positioner = getPositioner();

	const bbcAudiowf = data.data.audioWave.data;
	const audioSrc = `/audio-mp3/${data.data.audioId}.mp3`; // Define the audio source
	let isPlaying = $state(false);

 // let's check that we have the right variable
	const wavesurfer_audio_id = data.data.audioId;
	console.log("/// ")
	console.log("/// ")
	console.log("/// ")
	console.log("/// ")

	console.log("wavesurfer_audio_id is:", wavesurfer_audio_id)
	// console.log("wavesurfer waveform looks like :", bbcAudiowf)

	console.log(data);


	console.log("wavesurfer.svelte / audiowave.version", bbcAudiowf.version)
    console.log("wavesurfer.svelte / audiowave.channels", bbcAudiowf.channels)
    console.log("wavesurfer.svelte / audiowave.sample_rate", bbcAudiowf.sample_rate)
    console.log("wavesurfer.svelte / audiowave.samples_per_pixel", bbcAudiowf.samples_per_pixel)
    console.log("wavesurfer.svelte / audiowave.bits", bbcAudiowf.bits)
    console.log("wavesurfer.svelte / audiowave.length", bbcAudiowf.length)


	async function waveform(node: any) {
		try {
			const { default: WaveSurfer } = await import('wavesurfer.js');

			wavesurfer = WaveSurfer.create({
				container: node, // Use the actual DOM node
				height: 150,
				waveColor: '#1c1d1b',
				progressColor: ['#eb9770', '#b73b43', '#610826'],
				mediaControls: false,
				minPxPerSec: 0.1,
				interact: true,
				dragToSeek: true,
				autoScroll: true,
				media: document.querySelector('audio'),
				audioRate: 1,
				peaks: [bbcAudiowf],
				duration: 2340,
				plugins: []
			});

			wavesurfer.on('timeupdate', (currentTime) => {
				currentPlaybackPosition = currentTime;
				positioner.set(currentTime);
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

	function togglePlayback() {
		if (!wavesurfer) return;

		if (isPlaying) {
			wavesurfer.pause();
		} else {
			wavesurfer.play();
		}
	}


  function handleKeydown(event) {
    // Space key for play/pause
    if (event.code === 'Space' && !event.target.matches('input, textarea, [contenteditable]')) {
      event.preventDefault(); // Prevent page scrolling
      if (wavesurfer) {
        if (isPlaying) {
          wavesurfer.pause();
        } else {
          wavesurfer.play();
        }
      }
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


</script>

<div class="flex-col gap-y-8">
	<div class="mb-4 rounded-lg bg-none">
		<audio class="rounded-lg" src={audioSrc}></audio>
	</div>

	<div class="shrink rounded-lg bg-none" id="waveform" use:waveform></div>
</div>
<hr />

<div class="mt-4 flex gap-2">
	<button
  class="group h-12 w-24 select-none rounded-lg bg-white text-center px-3 text-lg leading-8 text-neutral-950 
  shadow-[0_-1px_0_0px_#d4d4d8_inset,0_0_0_1px_#f4f4f5_inset,0_0.5px_0_1.5px_#fff_inset]
   hover:bg-neutral-50 hover:via-neutral-900 hover:to-neutral-800 
   active:shadow-[-1px_0px_1px_0px_#e4e4e7_inset,1px_0px_1px_0px_#e4e4e7_inset,0px_0.125rem_1px_0px_#d4d4d8_inset]"
		onclick={togglePlayback}
		aria-label={isPlaying ? 'Pause' : 'Play'}
	>
		{#if isPlaying}
			<PauseIcon size={24} class="block m-auto" />
		{:else}
			<PlayIcon size={24} class="block m-auto"/>
		{/if}</button
	>
	<button
  class="group h-12 w-24 select-none rounded-lg bg-white px-3 text-lg leading-8 text-neutral-950 
  shadow-[0_-1px_0_0px_#d4d4d8_inset,0_0_0_1px_#f4f4f5_inset,0_0.5px_0_1.5px_#fff_inset]
   hover:bg-neutral-50 hover:via-neutral-900 hover:to-neutral-800 
   active:shadow-[-1px_0px_1px_0px_#e4e4e7_inset,1px_0px_1px_0px_#e4e4e7_inset,0px_0.125rem_1px_0px_#d4d4d8_inset]"
		onclick={(document.querySelector('audio').playbackRate = 1.5)}>
    <span class="block group-active:[transform:translate3d(0,1px,0)]">1.5x</span></button
	>
	<button
  class="group h-12 w-24 select-none rounded-lg bg-white px-3 text-lg leading-8 text-neutral-950 
  shadow-[0_-1px_0_0px_#d4d4d8_inset,0_0_0_1px_#f4f4f5_inset,0_0.5px_0_1.5px_#fff_inset]
   hover:bg-neutral-50 hover:via-neutral-900 hover:to-neutral-800 
   active:shadow-[-1px_0px_1px_0px_#e4e4e7_inset,1px_0px_1px_0px_#e4e4e7_inset,0px_0.125rem_1px_0px_#d4d4d8_inset]"
		onclick={(document.querySelector('audio').playbackRate = 2)}>
    <span class="block group-active:[transform:translate3d(0,1px,0)]">2x</span></button
	>
	<button
  class="group h-12 w-24 select-none rounded-lg bg-white px-3 text-lg leading-8 text-neutral-950 
  shadow-[0_-1px_0_0px_#d4d4d8_inset,0_0_0_1px_#f4f4f5_inset,0_0.5px_0_1.5px_#fff_inset]
   hover:bg-neutral-50 hover:via-neutral-900 hover:to-neutral-800 
   active:shadow-[-1px_0px_1px_0px_#e4e4e7_inset,1px_0px_1px_0px_#e4e4e7_inset,0px_0.125rem_1px_0px_#d4d4d8_inset]"
		onclick={(document.querySelector('audio').playbackRate = 2.5)}>
    <span class="block group-active:[transform:translate3d(0,1px,0)]">2.5x</span></button
	>
	<button
  class="group h-12 w-24 select-none rounded-lg bg-white px-3 text-lg leading-8 text-neutral-950 
  shadow-[0_-1px_0_0px_#d4d4d8_inset,0_0_0_1px_#f4f4f5_inset,0_0.5px_0_1.5px_#fff_inset]
   hover:bg-neutral-50 hover:via-neutral-900 hover:to-neutral-800 
   active:shadow-[-1px_0px_1px_0px_#e4e4e7_inset,1px_0px_1px_0px_#e4e4e7_inset,0px_0.125rem_1px_0px_#d4d4d8_inset]"
   onclick={(document.querySelector('audio').playbackRate = 3)}>
   <span class="block group-active:[transform:translate3d(0,1px,0)]">3x</span></button>
</div>