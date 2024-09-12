const fs = require('fs').promises;
const path = require('path');
const { faker } = require('@faker-js/faker');

// Utility functions
const isSaturday = (dateString) => new Date(dateString).getDay() === 6;

const roundToTwoDecimals = (num) => Math.round(num * 100) / 100;

const writeToFile = async (filename, content) => {
    const filePath = path.join(__dirname, '..', 'text_files', filename);
    await fs.writeFile(filePath, content);
};

// Core functions
const processScores = (inputText, cutoffDate) => {
    return inputText.split('\n')
        .map(line => line.split(',').map(item => item.trim()))
        .filter(([, date, time]) => date >= cutoffDate && parseInt(time) <= 1200)
        .map(([name, date, time]) => [name, date, parseInt(time)])
        .sort((a, b) => a[1].localeCompare(b[1]));
};

const anonymizeNames = (sortedList) => {
    faker.seed(1);
    const nameMap = new Map();
    return sortedList.map(([name, date, time]) => [
        nameMap.get(name) || nameMap.set(name, faker.name.fullName()).get(name),
        date,
        time
    ]);
};

const calculateAverageTimes = (scores) => {
    const timeData = scores.reduce((acc, [name, date, time]) => {
        if (!acc[name]) acc[name] = { regular: [], saturday: [] };
        (isSaturday(date) ? acc[name].saturday : acc[name].regular).push(time);
        return acc;
    }, {});

    return Object.entries(timeData).map(([name, { regular, saturday }]) => ({
        name,
        regularAvg: regular.length ? roundToTwoDecimals(regular.reduce((a, b) => a + b) / regular.length) : -1,
        regularCount: regular.length,
        saturdayAvg: saturday.length ? roundToTwoDecimals(saturday.reduce((a, b) => a + b) / saturday.length) : -1,
        saturdayCount: saturday.length
    }));
};

const analyzeAverageTimes = async (averageTimes, cutoffDate) => {
    const regularSorted = averageTimes.sort((a, b) => a.regularAvg - b.regularAvg);
    const saturdaySorted = averageTimes.sort((a, b) => a.saturdayAvg - b.saturdayAvg);

    const output = `Cutoff day: ${cutoffDate}
Name, Average Time, Number of Times
${regularSorted.map(({ name, regularAvg, regularCount }) => `${name}, ${regularAvg}, ${regularCount}`).join('\n')}

Saturdays:
${saturdaySorted.map(({ name, saturdayAvg, saturdayCount }) => `${name}, ${saturdayAvg}, ${saturdayCount}`).join('\n')}`;

    await writeToFile('averages.txt', output);
};

const analyzePlacementInfo = (scores) => {
    const placements = scores.reduce((acc, [name, date, time], _, arr) => {
        if (!acc[date]) acc[date] = arr.filter(score => score[1] === date).sort((a, b) => a[2] - b[2]);
        const place = acc[date].findIndex(score => score[2] === time) + 1;
        if (!acc.individuals[name]) acc.individuals[name] = [];
        acc.individuals[name].push(place);
        return acc;
    }, { individuals: {} });

    return placements.individuals;
};

const findAveragePlace = async (individualsDict) => {
    const averagePlacements = Object.entries(individualsDict).map(([person, places]) => ({
        person,
        average: roundToTwoDecimals(places.reduce((a, b) => a + b) / places.length)
    })).sort((a, b) => a.average - b.average);

    const output = `Average placements per person:
${averagePlacements.map(({ person, average }) => `${person}, ${average}`).join('\n')}`;

    await writeToFile('average_placements.txt', output);
};

const findNumberOfFirsts = async (individualsDict) => {
    const firstPlaces = Object.entries(individualsDict).map(([person, places]) => ({
        person,
        firsts: places.filter(place => place === 1).length
    })).sort((a, b) => b.firsts - a.firsts);

    const output = `Number of first place finishes per person:
${firstPlaces.map(({ person, firsts }) => `${person}, ${firsts}`).join('\n')}`;

    await writeToFile('first_places.txt', output);
};

const countTimesOccurrences = async (sortedScores, cutoffDate) => {
    const occurrences = sortedScores.reduce((acc, [, , time]) => {
        acc[time] = (acc[time] || 0) + 1;
        return acc;
    }, {});

    const byTime = Object.entries(occurrences)
        .sort(([a], [b]) => parseInt(a) - parseInt(b))
        .map(([time, count]) => `Time: ${time}   Occurrence: ${count}`)
        .join('\n');

    const byOccurrence = Object.entries(occurrences)
        .sort(([a, aCount], [b, bCount]) => bCount - aCount || parseInt(a) - parseInt(b))
        .map(([time, count]) => `Occurrence: ${count}    Time: ${time}`)
        .join('\n');

    await writeToFile('time_occurrences.txt', `Number of occurrences for each time (cutoff date is ${cutoffDate}):\n${byTime}`);
    await writeToFile('most_common_times.txt', `Times sorted by which is most common (cutoff date is ${cutoffDate}):\n${byOccurrence}`);
};

const main = async (cutoffDate = '2023-02-21') => {
    try {
        const filePath = path.join(__dirname, '..', 'text_files', 'cleaned_data.txt');
        const text = await fs.readFile(filePath, 'utf8');
        const sortedScores = processScores(text, cutoffDate);
        const anonSortedScores = anonymizeNames(sortedScores);
        const averageTimes = calculateAverageTimes(anonSortedScores);
        await analyzeAverageTimes(averageTimes, cutoffDate);
        const placements = analyzePlacementInfo(anonSortedScores);
        await findAveragePlace(placements);
        await findNumberOfFirsts(placements);
        await countTimesOccurrences(anonSortedScores, cutoffDate);
        console.log('Analysis complete. Check the text_files directory for results.');
    } catch (error) {
        console.error('An error occurred:', error);
    }
};

if (require.main === module) {
    const cutoffDate = process.argv[2] || undefined;
    main(cutoffDate);
}

module.exports = { main };  // Export for potential use in other modules