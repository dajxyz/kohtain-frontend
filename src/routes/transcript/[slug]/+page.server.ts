import { error } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';

export function load({ params }) {
    
    const audioId = params.slug;

    const filePathTranscript = path.resolve(`transcripts/${audioId}-aligned.json`);
    const filePathWaveform = path.resolve(`waveforms/${audioId}.json`);

    try {
        const fileContentTranscript = fs.readFileSync(filePathTranscript, 'utf-8');
        const trnscript = JSON.parse(fileContentTranscript);

        const fileContentWaveform  = fs.readFileSync(filePathWaveform, 'utf-8');
        const audioWave = JSON.parse(fileContentWaveform);

        console.log("+page.server.ts / audiowave.version", audioWave.version)
        console.log("+page.server.ts / audiowave.channels", audioWave.channels)
        console.log("+page.server.ts / audiowave.sample_rate", audioWave.sample_rate)
        console.log("+page.server.ts / audiowave.samples_per_pixel", audioWave.samples_per_pixel)
        console.log("+page.server.ts / audiowave.bits", audioWave.bits)
        console.log("+page.server.ts / audiowave.length", audioWave.length)

        return { trnscript, audioId, audioWave };
    } catch (err) {
        throw error(404, `Problem loading file: ${err.message}`);
    }
}

