<script lang="ts">
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Avatar from '$lib/components/ui/avatar/index.js';
	import WavesurferControl from '$lib/components/wavesurfer_control.svelte';

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

	const displayTurns = turns
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
		}));

	// console.log(displayTurns);
</script>

<div class="w-full overflow-x-auto bg-gray-100 p-5">
	<!-- Container sized to match timeline -->
	<div class="relative" style="width: {maxTime * SCALE}px">
		<!-- Turns Timeline -->
		<div class="turns relative mb-20 h-32">
			{#each processedTurns as turn}
				{#if turn.hasData}
					<div
						class="turns absolute h-32 rounded border border-[#164367] bg-[#80a8c5]"
						style="left: {turn.start}px; width: {turn.width}px; top: 16px; background-color: {speaker_colours[
							turn.speaker_int
						]}"
					>
						{turn.speaker_letter}
					</div>
				{/if}
			{/each}
		</div>

		<!-- Utterances Timeline -->
		<div class="utterances relative mb-20 h-32">
			{#each processedUtterances as utterance}
				<div
					class="utterance absolute h-32 rounded border border-[#436344] bg-[#8ab68e]"
					style="left: {utterance.start}px; width: {utterance.width}px; top: 16px;"
				>
					{utterance.text}
				</div>
			{/each}
		</div>

		<!-- Tokens Timeline -->
		<div class="tokens relative mb-20 h-32">
			{#each processedTokens as token}
				<div
					class="tokens absolute h-32 rounded border border-[#6f652a] bg-[#d8c86f]"
					style="left: {token.start}px; width: {token.width}px; top: 24px;"
				>
					{token.text}
				</div>
			{/each}
		</div>

		<!-- Time markers -->
		<div class="absolute left-0 top-0 h-8 w-full border-t border-gray-300">
			{#each Array(Math.ceil(maxTime / 10)) as _, i}
				<div class="absolute text-xs text-gray-500" style="left: {i * 10 * SCALE}px">
					{i * 10}s
				</div>
			{/each}
		</div>
	</div>
</div>

<WavesurferControl></WavesurferControl>

<div class="container mx-auto p-4">
	{#each displayTurns as speakerTurn}
		<div class="p-4 flex items-baseline gap-2 shadow-lg rounded-xl">
			<div class="w-12 shrink-0 text-right font-mono text-sm text-gray-500">
				<Avatar.Root>
					<Avatar.Fallback>{speakerTurn.speaker_letter}</Avatar.Fallback>
				</Avatar.Root>
			</div>

			<div class="flex-1">
				{#each speakerTurn.utterances as utterance}
					<div class="mb-0 flex items-baseline gap-2 last:mb-0">
						<div class="w-[25ch] shrink-0 text-center font-mono text-sm" style="color: {speaker_colours[speakerTurn.speaker_id]}">
							<p class="m-0">
								[{dropMilliseconds(utterance.timestamps.from)} - {dropMilliseconds(
									utterance.timestamps.to
								)}]
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
