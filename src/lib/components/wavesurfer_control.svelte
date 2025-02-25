<script lang="ts">
    import * as bbcAudioWaveform from '$lib/components/waveforms/1000690745960.json';
    import { getPositioner } from '$lib/slider.svelte.js';
    
    /** @type {{ data: string }} */
    let data = $props();
    
    let wavesurfer;
    let currentPlaybackPosition = $state(0);
    const positioner = getPositioner();
    const kuuid = data.data;
    const bbcAudiowf = bbcAudioWaveform.data;
    const audioSrc = "/audio-wav/1000690745960.wav"; // Define the audio source
  
    async function waveform(node) {
      try {
        const { default: WaveSurfer } = await import('wavesurfer.js');
  
        wavesurfer = WaveSurfer.create({
          container: node, // Use the actual DOM node
          height: 150,
          waveColor: '#cdcdcd',
          progressColor: '#639DA8',
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
  
    function playTrack() {
      if (wavesurfer) wavesurfer.play();
    }
  
    function pauseTrack() {
      if (wavesurfer) wavesurfer.pause();
    }
  </script>
  
  <div class="flex-col gap-y-8">
    <div class="mb-4 rounded-lg bg-black">
      <audio
        class="rounded-lg"
        src={audioSrc}
      ></audio>
    </div>
    
    <div class="shrink rounded-lg bg-black" id="waveform" use:waveform></div>
  </div>
  <hr />
  
  <div class="flex gap-2 mt-4">
    <button class="px-4 py-2 bg-blue-500 text-white rounded" onclick={playTrack}>Play</button>
    <button class="px-4 py-2 bg-red-500 text-white rounded" onclick={pauseTrack}>Pause</button>
  </div>
  