<script lang="ts">
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Avatar from '$lib/components/ui/avatar/index.js';
	import WavesurferControl from '$lib/components/wavesurfer_control.svelte';
	import * as Breadcrumb from '$lib/components/ui/breadcrumb/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import Button from '$lib/components/ui/button/button.svelte';
	import { useSidebar } from '$lib/components/ui/sidebar/index.js';
	import ColoredTags from '$lib/components/ColoredTags.svelte';

	// toggle code

	import * as ToggleGroup from '$lib/components/ui/toggle-group/index.js';

	export let data;

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

	console.log(displayTurns)
	// toggle code

	// Get unique speakers from the filtered turns
	const uniqueSpeakers = [...new Set(displayTurns.map((turn) => turn.speaker_letter))];

	// Set up speaker filter state (initially all speakers visible)
	let selectedSpeakers = new Set(uniqueSpeakers);
	let toggleState = 'all'; // Can be "all", "none", or "custom"

	// Filter the turns based on selected speakers
	$: filteredDisplayTurns = displayTurns.filter((turn) =>
		selectedSpeakers.has(turn.speaker_letter)
	);

	// Handle toggle selection
	function handleToggle(value: string) {
		if (value === 'all') {
			selectedSpeakers = new Set(uniqueSpeakers);
			toggleState = 'all';
		} else if (value === 'none') {
			selectedSpeakers = new Set();
			toggleState = 'none';
		} else {
			// Individual speaker toggle - CORRECTED LOGIC
			const newSelectedSpeakers = new Set(selectedSpeakers);

			if (newSelectedSpeakers.has(value)) {
				// If already selected, remove it (unselect the speaker)
				newSelectedSpeakers.delete(value);
			} else {
				// If not selected, add it (select the speaker)
				newSelectedSpeakers.add(value);
			}

			selectedSpeakers = newSelectedSpeakers;

			// Update toggle state based on selection
			if (newSelectedSpeakers.size === uniqueSpeakers.length) {
				toggleState = 'all';
			} else if (newSelectedSpeakers.size === 0) {
				toggleState = 'none';
			} else {
				toggleState = 'custom';
			}
		}
	}

	// Tags / regex search
	let tags = [];
	function poistaKorostukset(event) {
    tags = [];
}
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

	<WavesurferControl></WavesurferControl>

	<Button onclick={poistaKorostukset}>Poista korostukset</Button>
	<ColoredTags 
		bind:tags={tags}
		highlightColours={speaker_colours}
		placeholder="Add search terms..."
		onlyUnique={true}
  />

	<!-- Add this at the top of your component, before the timeline -->
	<div class="mb-4">
		<div class="mb-2 font-medium">Suodata</div>
		<div class="flex items-center gap-2">
			<ToggleGroup.Root type="multiple" class="flex flex-wrap gap-2">
				<ToggleGroup.Item
					value="all"
					variant={toggleState === 'all' ? 'default' : 'outline'}
					size="sm"
					class="px-3"
					onclick={() => handleToggle('all')}
				>
					Kaikki
				</ToggleGroup.Item>
				<ToggleGroup.Item
					value="none"
					variant={toggleState === 'none' ? 'default' : 'outline'}
					size="sm"
					class="px-3"
					onclick={() => handleToggle('none')}
				>
					Tyhjennä
				</ToggleGroup.Item>

				{#each uniqueSpeakers as speaker}
					<ToggleGroup.Item
						value={speaker}
						variant={selectedSpeakers.has(speaker) ? 'default' : 'outline'}
						size="sm"
						class="px-3"
						onclick={() => handleToggle(speaker)}
					>
						{speaker}
					</ToggleGroup.Item>
				{/each}
			</ToggleGroup.Root>
		</div>
	</div>

	<div class="container mx-auto p-4">
		{#each filteredDisplayTurns as speakerTurn, i}
			<div
				style="z-index: {200 - 2 * i}"
				class="relative box-border flex items-baseline gap-2 rounded-xl border border-white p-4 hover:border-slate-300 hover:shadow-md"
			>
				<div
					style="z-index: {200 - 2 * i + 1}; background-color: {speaker_colours[
						speakerTurn.speaker_id
					]}"
					class="absolute bottom-2 left-2 top-2 z-0 w-12 rounded-lg bg-slate-300 text-right font-mono text-sm text-gray-500"
				></div>
				<div
					style="z-index: {200 - 2 * i + 2}"
					class="ml-[-0.25rem] w-12 shrink-0 text-right font-mono text-xl text-gray-500"
				>
					<Avatar.Root>
						<Avatar.Fallback>{speakerTurn.speaker_letter}</Avatar.Fallback>
					</Avatar.Root>
				</div>

				<div class="flex-1">
					{#each speakerTurn.utterances as utterance}
						<div class="mb-0 flex items-baseline gap-2 last:mb-0">
							<div
								class="w-[12ch] text-center font-mono text-sm xl:w-[25ch]"
								style="color: {speaker_colours[speakerTurn.speaker_id]}"
							>
								<p class="m-0">
									[{dropMilliseconds(utterance.timestamps.from)}<span class="hidden xl:inline"
										>&nbsp;- {dropMilliseconds(utterance.timestamps.to)}</span
									>]
								</p>
							</div>

							<div class="flex-1">
								<p class="text-gray-800">{stripHiddenTokens(utterance.text)}</p>
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
		</div>
	</details>
</Sidebar.Inset>
