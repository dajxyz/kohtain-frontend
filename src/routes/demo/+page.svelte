<script lang='ts'>
  

export let data
// console.log(data.trnscript)

let utteranceBlocks = data.trnscript.diarization_enhanced.results
// console.log(typeof(utteranceBlocks))

let värit = [
	"#78e9ff55",
	"#b3000055",
	"#00ffd255",
	"#e3008755",
	"#00720055",
	"#ff6fff55",
	"#c6bb0055",
	"#22006d55",
	"#95a72955",
	"#a871ff55",
	"#00a97355",
	"#ff79ff55",
	"#64a15555",
	"#db63db55",
	"#00360755",
	"#ff7be555",
	"#002e0055",
	"#c30b4f55",
	"#00ecff55",
	"#bc2f0055",
	"#8ef8ff55",
	"#bc0a2b55",
	"#00b4c555",
	"#ff783955",
	"#00409fff",
	"#726600ff",
	"#003381ff",
	"#ffebc0ff",
	"#003f78ff",
	"#efd5a6ff",
	"#764ea1ff",
	"#711800ff",
	"#00acc4ff",
	"#50121aff",
	"#00a0bdff",
	"#ff9296ff",
	"#001d1aff",
	"#00769aff",
	"#006256ff",
	"#005471ff"
]

</script>


<pre>{JSON.stringify(data.trnscript.metadata)}</pre>



<div class="flex supercontainer">
    <!-- <div><p contenteditable="true">{utter.text}</p></div> -->
    {#each utteranceBlocks as utter}
    <p><span style="background-color:{värit[utter.speaker]}"><span class="">
        {#each utter.words as urd}
        <span style="color:rgb(0,0,0,{urd.confidence})">{urd.word}</span>
        {/each}
        <!-- {utter.words[0].word} -->
    </span></span>
	</p>

    {/each}
	<br>
    <!-- <div>{#each utter.words.word as wrd}<span class="tiiiny">{wrd}!!!</span>{/each}</div> -->
</div>




<style>
    .supercontainer {
        max-width: 100vw;
    }
    .tiiiny {
        font-size:0.5em;
    }


    /* {#each utteranceBlocks as utter}
<div class="flex">
    <!-- <div><p contenteditable="true">{utter.text}</p></div> -->
    <div><p><span class="tiiiny">{utter.language} - {utter.start} - {utter.end} - {utter.confidence}</span></p></div>
    <div style="background-color:{värit[utter.speaker]}"><p><span class="">
        {#each utter.words as urd}
        <span style="color:rgb(0,0,0,{urd.confidence})">{urd.word}</span>
        {/each}
        <!-- {utter.words[0].word} -->
    </span></p></div>

    <!-- <div>{#each utter.words.word as wrd}<span class="tiiiny">{wrd}!!!</span>{/each}</div> -->
</div>
{/each} */

</style>