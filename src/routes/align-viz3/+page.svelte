<script lang="ts">
	import { onMount } from 'svelte';
	export let data;

	let speaker_colours = [
		'#6060a6aa',
		'#bd824caa',
		'#b35f84aa',
		'#3d8d87aa',
		'#9797dbaa',
		'#e2bc0aaa',
		'#78146eaa',
		'#ff9296aa'
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

	const turns = data.trnscript.turns || [];
	const maxTime = Math.max(...turns.map((turn) => turn?.turn?.end || 0)) + 100;

	// Scale factor for visualization (px per second)
	const SCALE = 180;


	// Process turns data
	const processedTurns = turns.map((turn) => ({
		speaker_int: parseInt(turn.label),
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

	console.log(processedTurns);
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
						style="left: {turn.start}px; width: {turn.width}px; top: 16px; background-color: {speaker_colours[turn.speaker_int]}"
					>
						{turn.speaker_int}
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
