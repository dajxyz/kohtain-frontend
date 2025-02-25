<script lang="ts">
    import { onMount } from 'svelte';
    export let data;

    let maxTime = 0;
    
    onMount(() => {
        // Access the correct data structure
        const turns = data.trnscript.turns;
        
        // Calculate maxTime
        turns.forEach((turn) => {
            maxTime = Math.max(maxTime, turn.turn.end);
        });

        // Set container width (1px per second)
        const timelineWidth = maxTime + 100; // Add padding
        document.querySelectorAll('.timeline').forEach((timeline) => {
            timeline.style.width = timelineWidth + 'px';
        });

        // Render turns
        const turnsContainer = document.getElementById('turns');
        turns.forEach((turn) => {
            const segment = document.createElement('div');
            segment.className = 'segment turn-segment';
            segment.style.left = turn.turn.start + 'px';
            segment.style.width = turn.turn.end - turn.turn.start + 'px';
            turnsContainer?.appendChild(segment);
        });

        // Render utterances
        const utterancesContainer = document.getElementById('utterances');
        turns.forEach((turn) => {
            turn.utterances.forEach((utterance) => {
                const startTime = convertTimestampToSeconds(utterance.timestamps.from);
                const endTime = convertTimestampToSeconds(utterance.timestamps.to);

                const segment = document.createElement('div');
                segment.className = 'segment utterance-segment';
                segment.style.left = startTime + 'px';
                segment.style.width = endTime - startTime + 'px';
                utterancesContainer?.appendChild(segment);
            });
        });

        // Render tokens
        const tokensContainer = document.getElementById('tokens');
        turns.forEach((turn) => {
            turn.utterances.forEach((utterance) => {
                utterance.tokens.forEach((token) => {
                    const startTime = convertTimestampToSeconds(token.timestamps.from);
                    const endTime = convertTimestampToSeconds(token.timestamps.to);

                    const segment = document.createElement('div');
                    segment.className = 'segment token-segment';
                    segment.style.left = startTime + 'px';
                    segment.style.width = endTime - startTime + 'px';
                    tokensContainer?.appendChild(segment);
                });
            });
        });
    });

    function convertTimestampToSeconds(timestamp) {
        const [hours, minutes, seconds] = timestamp.split(':');
        const [secs, ms] = seconds.split(',');
        return parseInt(hours) * 3600 + parseInt(minutes) * 60 + parseInt(secs) + parseInt(ms) / 1000;
    }
</script>



    <div class="timeline-container">
        <div class="timeline turns-timeline flex flex-row gap-2" id="turns"></div>
        <div class="timeline utterances-timeline" id="utterances"></div>
        <div class="timeline tokens-timeline" id="tokens"></div>
    </div>


<style>
    .timeline-container {
        width: 100%; 
        height: 450px;
        overflow-x: auto;
        padding: 20px;
        background: #f5f5f5;
    }

    .timeline {
        height: 130px;
        margin-bottom: 20px;
        position: relative;
    }

    .turns-timeline {
        background-color: #80a8c5;
    }

    .utterances-timeline {
        background-color: #8ab68e;
    }

    .tokens-timeline {
        background-color: hsl(51, 57%, 64%);
    }

    .segment {
        height: 80px;
        top: 25px;
		border-style: dashed;
		border-width: 3px;
        border-radius: 4px;
        opacity: 0.8;
		margin-right: 20px;
    }

    .turn-segment {
        background-color: #2196f3 !important;
		border-color: #06487d !important; 
    }

    .utterance-segment {
        background-color: #4caf50;
    }

    .token-segment {
        background-color: #ffd700;
        height: 40px;
        top: 45px;
    }
</style>