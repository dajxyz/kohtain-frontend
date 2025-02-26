<!-- +page.svelte -->
<script lang="ts">

let scalingFactor = 30;
    import { onMount } from 'svelte';
    export let data;


    // console.log("Turns array:", data.trnscript.turns);
    
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
    const maxTime = Math.max(...turns.map(turn => turn?.turn?.end || 0)) + 100;


    const utteranceTimestamps = turns
        .flatMap(turn => turn?.utterances || [])
        .filter(utterance => utterance?.timestamps?.from && utterance?.timestamps?.to)
        .map(utterance => utterance.timestamps);


    const tokenTimestamps = turns
        .flatMap(turn => turn?.utterances || [])
        .flatMap(utterance => utterance?.tokens || [])
        .filter(token => token?.timestamps?.from && token?.timestamps?.to)
        .map(token => token.timestamps);

// Helper function to calculate width safely
function calculateWidth(from: string | undefined, to: string | undefined): number {
        if (!from || !to) return 0;
        return (convertTimestampToSeconds(to) - convertTimestampToSeconds(from)) * scalingFactor;
    }



// {turn.turn.end - turn.turn.start}
</script>

<div class="w-full h-96 overflow-x-auto bg-gray-100 p-5">
    <!-- Turns Timeline -->
    <div id="turns" class="h-32 mb-20 flex flex-row" style="width: {maxTime * scalingFactor}px">
        {#each turns as turn}
            <div
                class="p-0 m-0 h-32 bg-slate-600"
                style="box-sizing: border-box; width: { (turn.turn.end - turn.turn.start) * scalingFactor}px; height: 100px; border-width: 1px;border-color: #164367; background-color: #80a8c5"
            > </div>
        {/each}
    </div>
    <div id="utterances" class="h-32 mb-20 flex flex-row" style="width: {maxTime * scalingFactor}px">
        {#each utteranceTimestamps as utteranceTimestamp}
            <div
                class="p-0 box-border m-0 h-32 bg-slate-600"
                style="box-sizing: border-box; width: {(convertTimestampToSeconds(utteranceTimestamp.to) - convertTimestampToSeconds(utteranceTimestamp.from)) * scalingFactor }px; height: 100px; border-width: 1px;border-color: #436344; background-color: #8ab68e;"
            ></div>
        {/each}
    </div>
    <div id="tokens" class="h-32 mb-20 flex flex-row" style="width: {maxTime * scalingFactor}px">
        {#each tokenTimestamps as tokenTimestamp}
            <div
                class="p-0 box-border m-0 h-32 bg-slate-600"
                style="box-sizing: border-box; width: {(convertTimestampToSeconds(tokenTimestamps.to) - convertTimestampToSeconds(tokenTimestamps.from)) * scalingFactor }px; height: 100px; border-width: 1px;border-color: #6f652a;  background-color: #d8c86f;"
            ></div>
        {/each}
    </div>

</div>

<pre>

</pre>


