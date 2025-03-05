<script lang="ts">
	import { getPositioner } from '$lib/slider.svelte.js';
	import PauseIcon from 'lucide-svelte/icons/pause';
	import PlayIcon from 'lucide-svelte/icons/play';
	import Button from '$lib/components/ui/button/button.svelte';
	import * as Tooltip from "$lib/components/ui/tooltip/index.js";


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

			wavesurfer.on('init', () => {
				audioDuration = wavesurfer.getDuration();
				console.log("this was triggered")
				console.log(audioDuration)
			});

			wavesurfer.on('timeupdate', (currentTime: number) => {
				currentPlaybackPosition = currentTime;
				positioner.set(currentTime);
				audioDuration = wavesurfer.getDuration();
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
		wavesurfer.setTime(seconds);
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

	let podcastsData = [
		{
			podid: '1000694721078',
			name: 'HS Visio -podcast',
			date: '21.2.2025',
			subject: 'Eurooppa voi ratkaista sodan rahalla, vieraana Valtteri Ahti',
			teaser: ''
		},
		{
			podid: '1000694507711',
			name: 'Suomen nostatus',
			date: '20.2.2025',
			subject: 'Nyt Yhdysvallat tekee juuri sen, mitä toivomme',
			teaser: ''
		},
		{
			podid: '1000694237224',
			name: 'Futucast',
			date: '20.2.2025',
			subject: 'Tony Rehn | Muovia hiilidioksidista - miten päästöistä tehdään raaka-ainetta',
			teaser: ''
		},
		{
			podid: '1000690745960',
			name: 'Futucast',
			date: '10.2.2025',
			subject:
				'Ossi Kettunen | Arktisen alueen geopolitiikka: Trump, Grönlanti, Kiina, Venäjä ja Suomi',
			teaser: ''
		},
		{
			podid: '1000690742506',
			name: 'Startup-ministeriö',
			date: '10.2.2025',
			subject: 'Näin Supercell, Wolt ja Slush tekevät PR-työtä feat Heini Vesander',
			teaser: ''
		},
		{
			podid: '1000689947691',
			name: 'HS Visio -podcast',
			date: '7.2.2025',
			subject: 'Nvidia on suomalaisten kansanosake, vieraana Jukka Lepikkö',
			teaser: ''
		},
		{
			podid: '1000694985285',
			name: 'Lauantaikerho',
			date: '22.2.2025',
			subject: 'Vaalikevät sarastaa jo: Vaihtuuko valta Helsingissä? Lauantaikerho',
			teaser: ''
		},
		{
			podid: '1000695190411',
			name: 'Ysärin lapset',
			date: '23.2.2025',
			subject: 'Uusi minisarja kertoo 90-luvun kännäävistä nuorista',
			teaser: ''
		},
		{
			podid: '1000695009482',
			name: 'inderesPodi',
			date: '22.2.2024',
			subject: 'Tulosviikkosummaus (21.2.2025) | inderesPodi 222',
			teaser: ''
		},
		{
			podid: '1000695442653',
			name: '#neuvottelija Sami Miettinen',
			date: '24.2.2025',
			subject: 'Trumpin ajan vientipolitiikka | Rydman',
			teaser: ''
		},
		{
			podid: '1000695356036',
			name: 'Puheenaihe',
			date: '23.2.2025',
			subject: 'Tekoäly: Neuroverkot, robotit ja evoluutio (Risto Miikkulainen)',
			teaser: ''
		},
		{
			podid: '1000694751482',
			name: 'inderesPodi',
			date: '21.2.2025',
			subject: 'Näkökulmia vastuulliseen sijoittamiseen osa 1, vieraana Vesa Puttonen ',
			teaser: ''
		},
		{
			podid: '1000695702568',
			name: 'Väkevä elämä - Viisaampi mieli, vahvempi keho',
			date: '25.2.2025',
			subject:
				'Mikael Paajanen - Miten teet itsestäsi hybridiliikkujan, jolla on sekä voimaa että kestävyyttä?',
			teaser: ''
		},
		{
			podid: '1000695422901',
			name: 'Mimmit sijoittaa',
			date: '24.2.2025',
			subject: 'K3 J2: Kannattaako NYT ostaa (sijoitus)asunto? Ekonomisti vastaa',
			teaser: ''
		},
		{
			podid: '1000695440009',
			name: 'Futucast',
			date: '24.2.2025',
			subject: 'Jyri Kosola | Tulevaisuuden sotateknologia #517',
			teaser: ''
		},
		{
			podid: '1000694633694',
			name: 'Politiikan viikko',
			date: '21.2.2025',
			subject: 'Jakso 17: Ukrainasta ilman Ukrainaa',
			teaser: ''
		},
		{
			podid: '1000694811790',
			name: 'Mikä meitä vaivaa?',
			date: '21.2.2025',
			subject: 'Jakso 121: Latistuksen mankeli',
			teaser: ''
		},
		{
			podid: '1000695645737',
			name: 'Seinä kolmannelle',
			date: '24.2.2025',
			subject: 'Brittifutispodcast: Mestaruustaisto on päättynyt',
			teaser: ''
		},
		{
			podid: '1000695364559',
			name: 'Puurojengi',
			date: '23.2.2025',
			subject: '86. Etikettikoulu',
			teaser: ''
		},
		{
			podid: '1000694151332',
			name: 'Puurojengi',
			date: '19.2.2025',
			subject: '85. Vältyin täpärästi kiroukselta',
			teaser: ''
		},
		{
			podid: '1000695641515',
			name: 'Bella Table',
			date: '24.2.2025',
			subject: '218. Ihaninta just nyt',
			teaser: ''
		},
		{
			podid: '1000695413973',
			name: 'Psykopodiaa',
			date: '24.2.2025',
			subject: '174. Tyhmä työelämä. Vieraana Mona Moisala.',
			teaser: ''
		},
		{
			podid: '1000695735266',
			name: 'Sijoituskästi',
			date: '25.2.2025',
			subject: '#207 Onko Trump seonnut? ft. Tero Kuittinen',
			teaser: ''
		}
	];

	let thisPodcast = podcastsData.find((podcast) => podcast.podid == data.data.audioId);
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
		<div class="h-[80px] rounded-lg bg-slate-100" use:waveform></div>
		
		<!-- Time indicators -->
		<div class="flex justify-between mt-1 text-sm text-slate-700">
			<span>{formatTime(currentPlaybackPosition)}</span>
			<span>{formatTime(audioDuration)}</span>
		</div>
	</div></div>
<hr />

<div class="flex items-center justify-between mt-2 gap-2">
	<!-- Play/Pause Button -->

				<Button 
					variant="default" 
					size="icon" 
					class="h-10 w-10 bg-purple-600 hover:bg-purple-700 text-white"
					onclick={togglePlayback}
				>
					{#if isPlaying}
					<PauseIcon size={20} />
					{:else}
					<PlayIcon size={20} />
					{/if}
				</Button>

	<div class="flex items-center gap-1">
		<!-- Skip Back Button -->
		<Tooltip.Provider>
			<Tooltip.Root>
				<Tooltip.Trigger>
					<Button 
						variant="outline" 
						size="icon" 
						class="h-9 w-9"
						onclick={() => skipBack(5)}
					>
						rw
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
				<Tooltip.Trigger>
					<Button 
						variant="outline" 
						size="icon" 
						class="h-9 w-9"
						onclick={() => skipForward(15)}
					>
						ff
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content>
					<p>Forward 15s</p>
				</Tooltip.Content>
			</Tooltip.Root>
		</Tooltip.Provider>
	</div>
</div>

<div class="flex flex-row items-center">
	<div class="container mx-auto mt-4 p-4 pt-0">
		<p class="text-sm">{thisPodcast.date}</p>
		<h1 class="text-2xl">{thisPodcast.name}</h1>
		<p class="text-md">{thisPodcast.subject}</p>
	</div>
	<div class="mt-4 flex gap-2">
		<button
			class="group h-12 w-24 select-none rounded-lg bg-white px-3 text-center text-lg leading-8 text-neutral-950
  shadow-[0_-1px_0_0px_#d4d4d8_inset,0_0_0_1px_#f4f4f5_inset,0_0.5px_0_1.5px_#fff_inset]
   hover:bg-neutral-50 hover:via-neutral-900 hover:to-neutral-800
   active:shadow-[-1px_0px_1px_0px_#e4e4e7_inset,1px_0px_1px_0px_#e4e4e7_inset,0px_0.125rem_1px_0px_#d4d4d8_inset]"
			onclick={togglePlayback}
			aria-label={isPlaying ? 'Pause' : 'Play'}
		>
			{#if isPlaying}
				<PauseIcon size={24} class="m-auto block" />
			{:else}
				<PlayIcon size={24} class="m-auto block" />
			{/if}</button
		>
		<button
			class="group h-12 w-24 select-none rounded-lg bg-white px-3 text-lg leading-8 text-neutral-950
  shadow-[0_-1px_0_0px_#d4d4d8_inset,0_0_0_1px_#f4f4f5_inset,0_0.5px_0_1.5px_#fff_inset]
   hover:bg-neutral-50 hover:via-neutral-900 hover:to-neutral-800
   active:shadow-[-1px_0px_1px_0px_#e4e4e7_inset,1px_0px_1px_0px_#e4e4e7_inset,0px_0.125rem_1px_0px_#d4d4d8_inset]"
			onclick={(document.querySelector('audio').playbackRate = 1.5)}
		>
			<span class="block group-active:[transform:translate3d(0,1px,0)]">1.5x</span></button
		>
		<button
			class="group h-12 w-24 select-none rounded-lg bg-white px-3 text-lg leading-8 text-neutral-950
  shadow-[0_-1px_0_0px_#d4d4d8_inset,0_0_0_1px_#f4f4f5_inset,0_0.5px_0_1.5px_#fff_inset]
   hover:bg-neutral-50 hover:via-neutral-900 hover:to-neutral-800
   active:shadow-[-1px_0px_1px_0px_#e4e4e7_inset,1px_0px_1px_0px_#e4e4e7_inset,0px_0.125rem_1px_0px_#d4d4d8_inset]"
			onclick={(document.querySelector('audio').playbackRate = 2)}
		>
			<span class="block group-active:[transform:translate3d(0,1px,0)]">2x</span></button
		>
		<button
			class="group h-12 w-24 select-none rounded-lg bg-white px-3 text-lg leading-8 text-neutral-950
  shadow-[0_-1px_0_0px_#d4d4d8_inset,0_0_0_1px_#f4f4f5_inset,0_0.5px_0_1.5px_#fff_inset]
   hover:bg-neutral-50 hover:via-neutral-900 hover:to-neutral-800
   active:shadow-[-1px_0px_1px_0px_#e4e4e7_inset,1px_0px_1px_0px_#e4e4e7_inset,0px_0.125rem_1px_0px_#d4d4d8_inset]"
			onclick={(document.querySelector('audio').playbackRate = 2.5)}
		>
			<span class="block group-active:[transform:translate3d(0,1px,0)]">2.5x</span></button
		>
		<button
			class="group h-12 w-24 select-none rounded-lg bg-white px-3 text-lg leading-8 text-neutral-950
  shadow-[0_-1px_0_0px_#d4d4d8_inset,0_0_0_1px_#f4f4f5_inset,0_0.5px_0_1.5px_#fff_inset]
   hover:bg-neutral-50 hover:via-neutral-900 hover:to-neutral-800
   active:shadow-[-1px_0px_1px_0px_#e4e4e7_inset,1px_0px_1px_0px_#e4e4e7_inset,0px_0.125rem_1px_0px_#d4d4d8_inset]"
			onclick={(document.querySelector('audio').playbackRate = 3)}
		>
			<span class="block group-active:[transform:translate3d(0,1px,0)]">3x</span></button
		>
	</div>
</div>
