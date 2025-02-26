import { error } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';


export function load() {
	const filePath = path.resolve('static/gladia_output.json');
    console.log(filePath)
    let fileContent = fs.readFileSync(filePath, 'utf-8');
    let jsonData = JSON.parse(fileContent);
    // console.log(jsonData.metadata)

	try {
        // Read the JSON file
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const trnscript = JSON.parse(fileContent);

        // console.log(trnscript.metadata)

        return {
            trnscript
        };

    } catch (err) {
        // If the file doesn't exist or there is an error, throw an error
        throw error(404, `Problem loading file or smth`);
    }
}
