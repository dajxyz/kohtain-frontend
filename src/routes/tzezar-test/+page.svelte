<script lang="ts">
	import { CodeSnippet } from '$lib/components/tzezars-enhancements/code-snippet';
    import { FileDropzone } from '$lib/components/tzezars-enhancements/file-dropzone';

</script>

<CodeSnippet content="
./build/bin/whisper-cli -m models/ggml-large-v2.bin -f ../kohtain-demo-audio/1000694012385.wav --print-colors --output-json-full --output-file 1000694012385-v2 --print-special --language fi --print-progress;

./build/bin/whisper-cli -m models/ggml-large-v2.bin -f ../kohtain-demo-audio/1000693832063.wav --print-colors --output-json-full --output-file 1000693832063-v2 --print-special --language fi --print-progress;

./build/bin/whisper-cli -m models/ggml-large-v2.bin -f ../kohtain-demo-audio/1000689442113.wav --print-colors --output-json-full --output-file 1000689442113-v2 --print-special --language fi --print-progress;

./build/bin/whisper-cli -m models/ggml-large-v2.bin -f ../kohtain-demo-audio/1000694721078.wav --print-colors --output-json-full --output-file 1000694721078-v2 --print-special --language fi --print-progress

./build/bin/whisper-cli -m models/ggml-large-v2.bin -f ../kohtain-demo-audio/1000694507711.wav --print-colors --output-json-full --output-file 1000694507711-v2 --print-special --language fi --print-progress;

./build/bin/whisper-cli -m models/ggml-large-v2.bin -f ../kohtain-demo-audio/1000689947691.wav --print-colors --output-json-full --output-file 1000689947691-v2 --print-special --language fi --print-progress;

./build/bin/whisper-cli -m models/ggml-large-v2.bin -f ../kohtain-demo-audio/1000690745960.wav --print-colors --output-json-full --output-file 1000690745960-v2 --print-special --language fi --print-progress;

./build/bin/whisper-cli -m models/ggml-large-v2.bin -f ../kohtain-demo-audio/1000694237224.wav --print-colors --output-json-full --output-file 1000694237224-v2 --print-special --language fi --print-progress;
" />


<FileDropzone></FileDropzone>