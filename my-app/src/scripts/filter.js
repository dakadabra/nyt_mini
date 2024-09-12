import { promises as fs } from 'fs';
import { join } from 'path';

// Regular expressions
const REGEX = {
    timestamp: /\[(\d{4}-\d{2}-\d{2}, \d{1,2}:\d{2}:\d{2}\s*[\u202f ]?[AP]M)\]/g,
    urlSearch: /\[\d{4}-\d{2}-\d{2}, \d{1,2}:\d{2}:\d{2} (?:AM|PM)\] ~?\s*([^\s:]+(?: [^\s:]+)*)?:.*?d=(\d{4}-\d{2}-\d{2}).*?t=(\d+)&/,
    crosswordTime: /\[\d{4}-\d{2}-\d{2}, \d{1,2}:\d{2}:\d{2} (?:AM|PM)\] ~?\s*([^\s:]+(?: [^\s:]+)*)?:.*?I solved the (\d{1,2}\/\d{1,2}\/\d{4}) New York Times Mini Crossword in (\d+:\d{2})!/,
};

const CUSTOM_FORMATS = {
    URL: /.*https:\/\/www\.nytimes\.com\/badges.*/,
    Crossword: /.*I solved the (\d{1,2}\/\d{1,2}\/\d{4}) New York Times Mini Crossword in (\d+:\d{2})!.*/,
};

// Utility functions
const timeToSeconds = (timeStr) => {
    const [minutes, seconds] = timeStr.split(':').map(Number);
    return minutes * 60 + seconds;
};

const findSolveTime = (text) => {
    const match = text.match(REGEX.crosswordTime);
    if (!match) return null;

    const [, name, date, solveTime] = match;
    const formattedDate = new Date(date).toISOString().split('T')[0];
    const solveTimeInSeconds = timeToSeconds(solveTime);
    return [name, formattedDate, solveTimeInSeconds];
};

const checkFormat = (text, formatRegex) => formatRegex.test(text);

const processTextBetweenTimestamps = (text, outputStream) => {
    for (const [formatName, formatRegex] of Object.entries(CUSTOM_FORMATS)) {
        if (checkFormat(text, formatRegex)) {
            if (formatName === "URL") {
                const match = text.match(REGEX.urlSearch);
                if (match) {
                    const [, name, date, number] = match;
                    outputStream.write(`${name}, ${date}, ${number}\n`);
                }
            } else if (formatName === "Crossword") {
                const result = findSolveTime(text);
                if (result) {
                    const [name, date, solveTime] = result;
                    outputStream.write(`${name}, ${date}, ${solveTime}\n`);
                }
            }
            break;
        }
    }
};

const processFile = async () => {
    try {
        const inputPath = join(__dirname, '..', 'text_files', '_chat.txt');
        const outputPath = join(__dirname, '..', 'text_files', 'cleaned_data.txt');

        let text = await fs.readFile(inputPath, 'utf8');
        text = text.replace(/\u202F/g, ' ');

        const timestamps = text.match(REGEX.timestamp) || [];
        const outputStream = fs.createWriteStream(outputPath);

        for (let i = 0; i < timestamps.length - 1; i++) {
            const startIndex = text.indexOf(timestamps[i]) - 1;
            const endIndex = text.indexOf(timestamps[i+1]) - 1;
            const textBetweenTimestamps = text.slice(startIndex, endIndex).trim().replace(/\n/g, ' ');

            processTextBetweenTimestamps(textBetweenTimestamps, outputStream);
        }

        outputStream.end();
        console.log('Processing complete. Check cleaned_data.txt for results.');
    } catch (error) {
        console.error('An error occurred:', error);
    }
};

processFile();