"use strict";

// CROSS-62 exact census and blind growth estimates. Run with Node.js.
function verify() {
    function check(condition, message) {
        if (!condition) throw new Error(message);
    }

    function gcd(a, b) {
        while (b !== 0n) [a, b] = [b, a % b];
        return a < 0n ? -a : a;
    }

    function addFraction([a, b], c, d) {
        const numerator = a * d + b * c;
        const denominator = b * d;
        const divisor = gcd(numerator, denominator);
        return [numerator / divisor, denominator / divisor];
    }

    function verifyExact() {
        const initialSigns = [1, -1, 1, -1, 1, -1];
        const initial = initialSigns.map((sign, root) => ({ sign, root, watched: true }));
        const schedules = [
            [[1, 1], [1, 1], [1, 1], [1, 1]],
            [[2, 1], [2, 1], [2, 1], [2, 1]],
            [[2, 1], [2, 1], [1, 2], [1, 2]],
            [[3, 2], [1, 4], [5, 1], [1, 2]],
        ];
        let histories = 0;
        let inexactReadings = 0;
        for (const schedule of schedules) {
            const differences = [[0n, 1n], [0n, 1n]];

            function visit(slots, depth, flips, numerator, denominator) {
                if (depth === schedule.length) {
                    const leaves = initialSigns.map(() => 0);
                    for (const { root } of slots) leaves[root]++;
                    let observed = 0;
                    for (const [root, sign] of initialSigns.entries()) {
                        const estimate = 2 ** flips[root];
                        const cohort = sign === 1 ? 0 : 1;
                        const difference = BigInt(estimate - leaves[root]);
                        differences[cohort] = addFraction(differences[cohort], numerator * difference, denominator);
                        observed += estimate;
                    }
                    if (observed !== slots.length) inexactReadings++;
                    histories++;
                    return;
                }

                const [plus, minus] = schedule[depth];
                const weights = slots.map(({ sign }) => sign === 1 ? plus : minus);
                const total = weights.reduce((sum, weight) => sum + weight, 0);
                for (const [index, slot] of slots.entries()) {
                    const first = { ...slot, sign: -slot.sign };
                    const second = { ...first, watched: false };
                    const child = [...slots.slice(0, index), first, second, ...slots.slice(index + 1)];
                    if (slot.watched) flips[slot.root]++;
                    visit(child, depth + 1, flips, numerator * BigInt(weights[index]), denominator * BigInt(total));
                    if (slot.watched) flips[slot.root]--;
                }
            }

            visit(initial, 0, initialSigns.map(() => 0), 1n, 1n);
            check(differences.every(([num]) => num === 0n), "Exact cohort means disagree with descendant counts");
        }
        check(histories === 12096 && inexactReadings > 0, "Exact census or single-run control failed");
        return { histories, inexactReadings };
    }

    function randomSource(seed) {
        return function () {
            seed = (seed + 0x6D2B79F5) | 0;
            let value = Math.imul(seed ^ (seed >>> 15), 1 | seed);
            value ^= value + Math.imul(value ^ (value >>> 7), 61 | value);
            return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
        };
    }

    function simulate(n, plusCount, schedule, ports, random) {
        const flips = Array(ports).fill(0);
        const trackedPlus = [];
        const trackedMinus = [];
        let unseenPlus = plusCount;
        for (let port = 0; port < ports; port++) {
            if (random() * (n - port) < unseenPlus) {
                trackedPlus.push(port);
                unseenPlus--;
            } else {
                trackedMinus.push(port);
            }
        }
        let count = plusCount;
        for (const [step, [u, v]] of schedule.entries()) {
            const size = n + step;
            const positive = random() * (u * count + v * (size - count)) < u * count;
            const current = positive ? trackedPlus : trackedMinus;
            const other = positive ? trackedMinus : trackedPlus;
            const ordinal = Math.floor(random() * (positive ? count : size - count));
            if (ordinal < current.length) {
                const port = current[ordinal];
                current[ordinal] = current[current.length - 1];
                current.pop();
                other.push(port);
                flips[port]++;
            }
            count += positive ? -1 : 2;
        }
        return flips;
    }

    function estimate(flips) {
        return flips.reduce((sum, count) => sum + 2 ** count, 0) / flips.length;
    }

    function verifyBlind() {
        const n = 3072;
        const rounds = 2048;
        const counters = [32, 128, 512];
        const random = randomSource(612026);
        const cases = [
            { name: "uniform", plus: 1536, plan: [[3072, 1, 1]] },
            { name: "fixed 5:1", plus: 2304, plan: [[1536, 5, 1]] },
            { name: "midpoint reversal", plus: 1143, plan: [[1536, 2, 1], [1536, 1, 2]] },
            { name: "three stages", plus: 768, plan: [[1152, 1, 4], [2304, 3, 1], [1152, 2, 5]] },
        ];
        const results = [];
        for (const { name, plus, plan } of cases) {
            check((2 * plus - n) % 3 === 0, "The initial signs cannot close a proper three-colour ring");
            const schedule = plan.flatMap(([steps, u, v]) => Array(steps).fill([u, v]));
            const growth = 1 + schedule.length / n;
            const totals = counters.map(() => ({ error: 0, squared: 0 }));
            for (let run = 0; run < rounds; run++) {
                const flips = simulate(n, plus, schedule, counters[counters.length - 1], random);
                for (const [index, count] of counters.entries()) {
                    const error = estimate(flips.slice(0, count)) - growth;
                    totals[index].error += error;
                    totals[index].squared += error * error;
                }
            }
            const estimates = totals.map(({ error, squared }, index) => {
                const bias = error / rounds;
                const rmse = Math.sqrt(squared / rounds);
                check(Math.abs(bias) < 5 * rmse / Math.sqrt(rounds), "Blind mean missed its expected value");
                return { counters: counters[index], mean: growth + bias, rmse };
            });
            results.push({ name, growth, estimates });
        }
        return { n, rounds, results };
    }

    function hiddenMixExample() {
        const exposure = 0.5;
        const gap = Math.sqrt(33);
        const larger = (-3 + gap) / 2;
        const smaller = (-3 - gap) / 2;
        function growthFor(plusFraction) {
            const coefficient = (1 + plusFraction - smaller) / gap;
            return coefficient * Math.exp(larger * exposure) + (1 - coefficient) * Math.exp(smaller * exposure);
        }
        return [0.25, 0.75].map(plusFraction => ({ plusFraction, growth: growthFor(plusFraction) }));
    }

    return { exact: verifyExact(), blind: verifyBlind(), hiddenMix: hiddenMixExample() };
}

console.log(JSON.stringify(verify(), null, 2));
