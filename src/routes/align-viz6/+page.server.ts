import { error } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';

export function load() {
    const filePath = path.resolve('static/1000690745960-aligned.json');
    
    try {
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const trnscript = JSON.parse(fileContent);
        return { trnscript };
    } catch (err) {
        throw error(404, `Problem loading file: ${err.message}`);
    }
}