<script lang="ts">
	import AppSidebar from '$lib/components/app-sidebar.svelte';
	import * as Breadcrumb from '$lib/components/ui/breadcrumb/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import * as Card from "$lib/components/ui/card/index.js";


	export let data;

	let utteranceBlocks = data.trnscript.diarization_enhanced.results;
	// console.log(typeof utteranceBlocks);

	let värit = [
		'#78e9ff55',
		'#b3000055',
		'#00ffd255',
		'#e3008755',
		'#00720055',
		'#ff6fff55',
		'#c6bb0055',
		'#22006d55',
		'#95a72955',
		'#a871ff55',
		'#00a97355',
		'#ff79ff55',
		'#64a15555',
		'#db63db55',
		'#00360755',
		'#ff7be555',
		'#002e0055',
		'#c30b4f55',
		'#00ecff55',
		'#bc2f0055',
		'#8ef8ff55',
		'#bc0a2b55',
		'#00b4c555',
		'#ff783955',
		'#00409fff',
		'#726600ff',
		'#003381ff',
		'#ffebc0ff',
		'#003f78ff',
		'#efd5a6ff',
		'#764ea1ff',
		'#711800ff',
		'#00acc4ff',
		'#50121aff',
		'#00a0bdff',
		'#ff9296ff',
		'#001d1aff',
		'#00769aff',
		'#006256ff',
		'#005471ff'
	];

	interface Word {
  word: string;
  start: number;
  end: number;
  confidence: number;
}

interface Utterance {
  words: Word[];
  text: string;
  language: string;
  start: number;
  end: number;
  speaker: number;
  channel: number;
  confidence: number;
}

interface SpeakerTurn {
  speaker: number;
  "speaker-turn": string;
  "speaker-turn-start": number;
  "speaker-turn-end": number;
  utterances: Utterance[];
}

interface TranscriptOutput {
  turns: SpeakerTurn[];
}


function processTranscript(transcript: Utterance[]): TranscriptOutput {
  const turns: SpeakerTurn[] = [];
  let currentTurn: SpeakerTurn | null = null;

  for (const utterance of transcript) {
    if (!currentTurn || currentTurn.speaker !== utterance.speaker) {
      // If there's a current turn, push it to turns array before starting new one
      if (currentTurn) {
        turns.push(currentTurn);
      }

      // Start a new turn
      currentTurn = {
        speaker: utterance.speaker,
        "speaker-turn": utterance.text,
        "speaker-turn-start": utterance.start,
        "speaker-turn-end": utterance.end,
        utterances: [utterance]
      };
    } else {
      // Add to current turn
      currentTurn["speaker-turn"] = `${currentTurn["speaker-turn"]} ${utterance.text}`;
      currentTurn["speaker-turn-end"] = utterance.end;
      currentTurn.utterances.push(utterance);
    }
  }

  // Push the last turn if it exists
  if (currentTurn) {
    turns.push(currentTurn);
  }

  return { turns };
}

const processedUtteranceBlocks = processTranscript(utteranceBlocks);

// console.log(JSON.stringify(processedUtteranceBlocks, null, 2));



</script>


	<Sidebar.Inset>
		<header class="bg-background sticky top-0 flex shrink-0 items-center gap-2 border-b p-4">
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




	<pre>{JSON.stringify(data.trnscript.metadata)}</pre>



	<div class="flex flex-col supercontainer">
		<!-- <div><p contenteditable="true">{utter.text}</p></div> -->
		{#each utteranceBlocks as utter}
		<Card.Root>
			<p>
				<span style="background-color:{värit[utter.speaker]}">
				{#each utter.words as urd}
				<span style="color:rgb(0,0,0,{urd.confidence})">{urd.word}</span>
				{/each}
				<!-- {utter.words[0].word} -->
			</span>
			</p>
			<div class="mt-20"></div>

		</Card.Root>
		{/each}
		<br>

		<!-- <div>{#each utter.words.word as wrd}<span class="tiiiny">{wrd}!!!</span>{/each}</div> -->
	</div>
	
	
	
</Sidebar.Inset>

	<style>
		.supercontainer {
			max-width: 100vw;
		}
		/* .tiiiny {
			font-size:0.5em;
		} */
	
	</style>

