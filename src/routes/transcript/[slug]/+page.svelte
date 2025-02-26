<script lang="ts">
	import * as Avatar from '$lib/components/ui/avatar/index.js';
	import WavesurferControl from '$lib/components/wavesurfer_control.svelte';
	import * as Breadcrumb from '$lib/components/ui/breadcrumb/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import { getPositioner } from '$lib/slider.svelte.js';

	const positioner = getPositioner();
	let pos = $derived(positioner.position);

	const { data } = $props();

	let speaker_colours_medium = ['#394445', '#463C5B', '#67431E', '#5A242B'];
	let speaker_colours_medium_alpha = ['#394445aa', '#463C5Baa', '#67431Eaa', '#5A242Baa'];

	let speaker_colours_light = ['#ADBBBB', '#BBB2CE', '#E4B875', '#CB9DA1'];
	let speaker_colours_light_alpha = ['#ADBBBBaa', '#BBB2CEaa', '#E4B875aa', '#CB9DA1aa'];


	let speaker_colours = [
		'#6060a6ff',
		'#bd824cff',
		'#b35f84ff',
		'#3d8d87ff',
		'#9797dbff',
		'#e2bc0aff',
		'#78146eff',
		'#ff9296ff'
	];

	

	function convertTimestampToSeconds(timestamp: string | undefined): number {
		if (!timestamp) return 0;
		try {
			const [hours, minutes, seconds] = timestamp.split(':');
			const [secs, ms] = seconds.split(',');
			return parseInt(hours) * 3600 + parseInt(minutes) * 60 + parseInt(secs) + parseInt(ms) / 1000;
		} catch (e) {
			console.warn('Error converting timestamp:', timestamp, e);
			return 0;
		}
	}
	


	function stripHiddenTokens(text: string) {
		let text1 = text.replace(/\[[^\]]{0,50}\]/, '');
		let text2 = text1.replace(/\[[^\]]{0,50}\]/, '');
		return text2;
	}

	function dropMilliseconds(text: string) {
		let text1 = text.replace(/,\d{0,3}$/, '');
		return text1;
	}

	function calculateSpeakerDurations(turns: any[]) {
		return turns.reduce((acc, turn) => {
			const speakerId = turn.label;
			const duration = turn.turn.end - turn.turn.start;
			acc[speakerId] = (acc[speakerId] || 0) + duration;
			return acc;
		}, {});
	}

	function createSpeakerMapping(durations: Record<string, number>) {
		// Sort speakers by duration in descending order
		const sortedSpeakers = Object.entries(durations)
			.sort(([, a], [, b]) => b - a)
			.map(([id]) => id);

		// Create mapping from original ID to letter
		// Starting from 'A' (charcode 65)
		return sortedSpeakers.reduce(
			(acc, id, index) => {
				acc[id] = String.fromCharCode(65 + index);
				return acc;
			},
			{} as Record<string, string>
		);
	}

	const turns = data.trnscript.turns || [];
	const maxTime = Math.max(...turns.map((turn) => turn?.turn?.end || 0)) + 100;

	// Calculate durations and create mapping
	const speakerDurations = calculateSpeakerDurations(turns);
	const speakerLetterMapping = createSpeakerMapping(speakerDurations);

	const speakerStats = Object.entries(speakerDurations)
		.sort(([, a], [, b]) => b - a)
		.map(([id, duration]) => ({
			originalId: id,
			letter: speakerLetterMapping[id],
			duration: duration.toFixed(1),
			percentage: ((duration / maxTime) * 100).toFixed(1)
		}));

	// Scale factor for visualization (px per second)
	const SCALE = 180;

	// Process turns data
	const processedTurns = turns.map((turn) => ({
		speaker_int: parseInt(turn.label),
		speaker_letter: speakerLetterMapping[turn.label],
		start: turn.turn.start * SCALE,
		width: (turn.turn.end - turn.turn.start) * SCALE,
		hasData: turn?.turn?.start !== undefined && turn?.turn?.end !== undefined
	}));

	// Process utterances data with exact positioning
	const processedUtterances = turns
		.flatMap((turn) =>
			(turn?.utterances || []).map((utterance) => ({
				text: utterance?.text,
				start: convertTimestampToSeconds(utterance?.timestamps?.from) * SCALE,
				width:
					(convertTimestampToSeconds(utterance?.timestamps?.to) -
						convertTimestampToSeconds(utterance?.timestamps?.from)) *
					SCALE,
				hasData: utterance?.timestamps?.from && utterance?.timestamps?.to
			}))
		)
		.filter((u) => u.hasData && u.width > 0);

	function combineConsecutiveSpeakerTurns(turns: any[]) {
		if (!turns.length) return [];

		const combined = [];
		let currentGroup = null;

		for (const turn of turns) {
			if (!currentGroup) {
				// Start the first group
				currentGroup = { ...turn };
			} else if (currentGroup.speaker_id === turn.speaker_id) {
				// Same speaker, extend the current group
				currentGroup.end = turn.end;
				currentGroup.utterances = [...currentGroup.utterances, ...turn.utterances];
			} else {
				// New speaker, push the completed group and start a new one
				combined.push(currentGroup);
				currentGroup = { ...turn };
			}
		}

		// Don't forget to add the last group
		if (currentGroup) {
			combined.push(currentGroup);
		}

		return combined;
	}

	// Process tokens data with exact positioning
	const processedTokens = turns
		.flatMap((turn) =>
			(turn?.utterances || []).flatMap((utterance) =>
				(utterance?.tokens || []).map((token) => ({
					text: token?.text,
					start: convertTimestampToSeconds(token?.timestamps?.from) * SCALE,
					width:
						(convertTimestampToSeconds(token?.timestamps?.to) -
							convertTimestampToSeconds(token?.timestamps?.from)) *
						SCALE,
					hasData: token?.timestamps?.from && token?.timestamps?.to
				}))
			)
		)
		.filter((t) => t.hasData && t.width > 0);

	const displayTurns = combineConsecutiveSpeakerTurns(
		turns
			.filter(
				(turn) =>
					turn?.utterances?.length > 0 &&
					turn.utterances.some(
						(utterance) => utterance?.text && stripHiddenTokens(utterance.text).trim().length > 0
					)
			)
			.map((turn) => ({
				start: turn.turn.start,
				end: turn.turn.end,
				speaker_id: parseInt(turn.label),
				speaker_letter: speakerLetterMapping[turn.label],
				hasData: turn?.turn?.start !== undefined && turn?.turn?.end !== undefined,
				utterances: turn.utterances.filter(
					(utterance) => utterance?.text && stripHiddenTokens(utterance.text).trim().length > 0
				)
			}))
	);

	// These should be separate state variables, not derived values
	let activeSpeakerIndex = $state(-1);
	let activeUtteranceIndex = $state(-1);
	let activeTokenIndices = $state([]);

	// Update the active elements based on the current position
	$effect(() => {
		// Find active speaker turn
		activeSpeakerIndex = displayTurns.findIndex(
			(turn, i) => pos >= turn.start && (pos < turn.end || i === displayTurns.length - 1)
		);

		// Find active utterance
		if (activeSpeakerIndex === -1) {
			activeUtteranceIndex = -1;
			activeTokenIndices = [];
			return;
		}

		const speakerTurn = displayTurns[activeSpeakerIndex];
		activeUtteranceIndex = speakerTurn.utterances.findIndex((utterance, i) => {
			const fromSecs = convertTimestampToSeconds(utterance.timestamps.from);
			const toSecs = convertTimestampToSeconds(utterance.timestamps.to);
			return pos >= fromSecs && (pos < toSecs || i === speakerTurn.utterances.length - 1);
		});

		// Find active tokens
		if (activeUtteranceIndex === -1) {
			activeTokenIndices = [];
			return;
		}

		const utterance = speakerTurn.utterances[activeUtteranceIndex];
		activeTokenIndices = utterance.tokens
			.map((token, index) => {
				const fromSecs = convertTimestampToSeconds(token.timestamps.from);
				const toSecs = convertTimestampToSeconds(token.timestamps.to);
				if (pos >= fromSecs && pos < toSecs) {
					return index;
				}
				return -1;
			})
			.filter((index) => index !== -1);
	});

	// Debug log
	// $effect(() => {
	// 	console.log("Position:", pos);
	// 	console.log("Active speaker:", activeSpeakerIndex);
	// 	console.log("Active utterance:", activeUtteranceIndex);
	// 	console.log("Active tokens:", activeTokenIndices);
	// });

	console.log("+page.svelte / audiowave.version", data.audioWave.version)
    console.log("+page.svelte / audiowave.channels", data.audioWave.channels)
    console.log("+page.svelte / audiowave.sample_rate", data.audioWave.sample_rate)
    console.log("+page.svelte / audiowave.samples_per_pixel", data.audioWave.samples_per_pixel)
    console.log("+page.svelte / audiowave.bits", data.audioWave.bits)
    console.log("+page.svelte / audiowave.length", data.audioWave.length)
    console.log("+page.svelte / data.audioId", data.audioId)

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


	let thisPodcast = podcastsData.find(podcast => podcast.podid == data.audioId);
    console.log("+page.svelte / thisPodcast", thisPodcast)
	console.log("+page.svelte / thisPodcast.name", thisPodcast.name)
	console.log("+page.svelte / thisPodcast.date", thisPodcast.date)
	console.log("+page.svelte / thisPodcast.subject", thisPodcast.subject)


</script>

<Sidebar.Inset>
	<header class="top-0 z-50 flex shrink-0 items-center gap-2 border-b bg-background p-4">
		<Sidebar.Trigger class="-ml-1" />
		<Separator orientation="vertical" class="mr-2 h-4" />
		<Breadcrumb.Root>
			<Breadcrumb.List>
				<Breadcrumb.Item>
					<Breadcrumb.Page>Haastattelut</Breadcrumb.Page>
				</Breadcrumb.Item>
			</Breadcrumb.List>
		</Breadcrumb.Root>
	</header>

	<div class="container mx-auto p-4">
		<WavesurferControl data={data}></WavesurferControl>
	</div>

	<div class="container mx-auto p-4 mt-0 pt-0">
		<p class="text-sm">{thisPodcast.date} </p>
		<h1 class="text-2xl">{thisPodcast.name}</h1>
		<p class="text-md">{thisPodcast.subject} </p>
	</div>

	<div class="container mx-auto p-4">
		{#each displayTurns as speakerTurn, i}
			<div
				style="z-index: {200 - 2 * i}"
				class="relative box-border flex items-baseline gap-2 rounded-xl border border-neutral-50 bg-[#fEfEfE] p-4 hover:border-neutral-300 hover:bg-white hover:shadow-md {i === activeSpeakerIndex ? 'border-blue-300' : ''}"
			>
				<div
					style="z-index: {200 - 2 * i + 1}; background-color: {speaker_colours_light[
						speakerTurn.speaker_id
					]}"
					class="absolute bottom-2 left-2 top-2 z-0 w-12 rounded-lg bg-neutral-300 text-right font-mono text-sm text-neutral-500"
				></div>
				<div
					style="z-index: {200 - 2 * i + 2}"
					class="ml-[-0.25rem] w-12 shrink-0 text-right font-mono text-xl text-neutral-500"
				>
					<Avatar.Root>
						<Avatar.Fallback>{speakerTurn.speaker_letter}</Avatar.Fallback>
					</Avatar.Root>
				</div>

				<div class="flex-1">
					{#each speakerTurn.utterances as utterance, j}
						<div
							class="mb-0 flex items-baseline gap-2 last:mb-0 {i === activeSpeakerIndex &&
							j === activeUtteranceIndex
								? 'rounded'
								: ''}"
							style="background-color: {i === activeSpeakerIndex &&
							j === activeUtteranceIndex
								? speaker_colours_light_alpha[speakerTurn.speaker_id]
								: 'inherit'}"
						>
						<div
						class="w-[12ch] text-center font-mono text-sm xl:w-[25ch] cursor-pointer"
						style="color: {speaker_colours_medium[speakerTurn.speaker_id]}"
						onclick={() => positioner.set(convertTimestampToSeconds(utterance.timestamps.from))}
						role="button"
						tabindex="0"
						aria-label="Seek to {dropMilliseconds(utterance.timestamps.from)}"
					  >
						<p class="m-0 hover:underline underline-offset-2">
						  [{dropMilliseconds(utterance.timestamps.from)}<span class="hidden xl:inline"
							>&nbsp;- {dropMilliseconds(utterance.timestamps.to)}</span
						  >]
						</p>
					  </div>

							<div class="flex-1">
								<p class="text-neutral-800">
									{#if i === activeSpeakerIndex && j === activeUtteranceIndex && utterance.tokens}
										{#each utterance.tokens as token, k}
											<span
												class={activeTokenIndices.includes(k)
													? ' text-white'
													: ''}
												style="background-color: {activeTokenIndices.includes(k)
													? speaker_colours_medium_alpha[speakerTurn.speaker_id]
													: 'inherit'}"
											>
												{stripHiddenTokens(token.text)}
											</span>
										{/each}
									{:else}
										{stripHiddenTokens(utterance.text)}
									{/if}
								</p>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/each}
	</div>

	<!-- Debug info -->
	<details class="mt-4">
		<summary class="cursor-pointer">Debug Info</summary>
		<div class="font-mono text-xs">
			<p>Scale: {SCALE}px/second</p>
			<p>Total duration: {maxTime}s</p>
			<p>Total width: {maxTime * SCALE}px</p>
			<p>Turns: {processedTurns.length}</p>
			<p>Utterances: {processedUtterances.length}</p>
			<p>Tokens: {processedTokens.length}</p>
			<p>Current position: {pos}</p>
			<p>Active speaker: {activeSpeakerIndex}</p>
			<p>Active utterance: {activeUtteranceIndex}</p>
		</div>
	</details>
</Sidebar.Inset>

