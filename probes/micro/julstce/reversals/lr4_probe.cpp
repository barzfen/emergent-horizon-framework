// Propagate the difference of two Julstce shape distributions.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include <gmpxx.h>

using Runs = std::array<int, 6>;
using Shape = std::uint64_t;
using Integer = mpz_class;
using Distribution = std::unordered_map<Shape, Integer>;
constexpr int initial_size = 16;
constexpr int max_steps = 48;

Shape canonical(const Runs& runs) {
    Shape best = UINT64_MAX;
    for (int start = 0; start < 6; start += 2) {
        for (int direction : {1, -1}) {
            Shape key = 0;
            for (int pos = 0; pos < 6; ++pos) {
                key = (key << 8) | runs[(start + 6 + direction * pos) % 6];
            }
            best = std::min(best, key);
        }
    }
    return best;
}

Runs decode(Shape key) {
    Runs runs{};
    for (int pos = 5; pos >= 0; --pos) {
        runs[pos] = key & 255;
        key >>= 8;
    }
    return runs;
}

Distribution grow(const Distribution& current) {
    Distribution next;
    next.reserve(current.size() * 2);
    for (const auto& [shape, difference] : current) {
        Runs runs = decode(shape);
        for (int i = 0; i < 6; ++i) {
            ++runs[i];
            next[canonical(runs)] += difference * runs[i];
            --runs[i];
        }
    }
    return next;
}

Distribution reverse(Distribution current, int size, int attempts, int scale) {
    if (!attempts) return current;

    Distribution next;
    next.reserve(current.size() * 2);
    for (const auto& [shape, difference] : current) {
        Runs runs = decode(shape);
        const Integer moved_mass = difference * attempts;
        int legal_starts = 0;
        for (int i = 0; i < 6; ++i) {
            if (runs[i] > 3) continue;
            const int transfer = 4 - runs[i];
            int left = (i + 5) % 6;
            int right = (i + 1) % 6;
            for (const auto& [donor, receiver] : {std::pair{left, right}, std::pair{right, left}}) {
                if (runs[donor] < 2 + transfer) continue;
                ++legal_starts;
                runs[donor] -= transfer;
                runs[receiver] += transfer;
                next[canonical(runs)] += moved_mass;
                runs[receiver] -= transfer;
                runs[donor] += transfer;
            }
        }
        next[shape] += difference * (size * scale - legal_starts * attempts);
    }
    return next;
}


using BinomialCdf = std::array<std::array<Integer, initial_size + max_steps + 3>,
                                initial_size + max_steps + 3>;

BinomialCdf fair_coin_counts() {
    BinomialCdf counts{};
    counts[0].fill(1);
    for (int trials = 1; trials < static_cast<int>(counts.size()); ++trials) {
        for (int heads = 0; heads < static_cast<int>(counts[trials].size()); ++heads) {
            counts[trials][heads] = counts[trials - 1][heads];
            if (heads > 0) counts[trials][heads] += counts[trials - 1][heads - 1];
        }
    }
    return counts;
}

double ratio(const Integer& numerator, const Integer& denominator) {
    mpq_class value(numerator, denominator);
    value.canonicalize();
    return value.get_d();
}

void evaluate(int attempts, int scale, int steps) {
    const auto counts = fair_coin_counts();
    Distribution difference{
        {canonical({2, 2, 2, 5, 3, 2}), 1},
        {canonical({2, 3, 2, 2, 3, 4}), -1}
    };
    Integer denominator = 1;
    const std::vector<int> checkpoints{1, 2, 4, 8, 16, 32, 48};
    for (int step = 1; step <= steps; ++step) {
        const int size = initial_size + step;
        difference = reverse(grow(difference), size, attempts, scale);
        denominator *= size + 5;
        if (attempts) denominator *= size * scale;
        if (step != steps && std::find(checkpoints.begin(), checkpoints.end(), step) == checkpoints.end()) {
            continue;
        }
        Integer total = 0;
        Integer absolute_total = 0;
        Integer majority_gap = 0;
        Integer future_gap = 0;
        Integer coupling_error = 0;
        const int error_denominator = 12 * scale * (size + 1);
        const Integer fair_denominator = Integer(1) << (size + 2);
        for (const auto& [shape, mass] : difference) {
            total += mass;
            absolute_total += abs(mass);
            const Runs runs = decode(shape);
            const int ones = runs[1] + runs[3] + runs[5];
            Integer majority_count = counts[ones + 2][runs[1]]
                + counts[ones + 2][runs[3]] + counts[ones + 2][runs[5]];
            majority_count <<= size - ones;
            future_gap += mass * majority_count;
            const int length_two = std::count(runs.begin(), runs.end(), 2);
            const int length_three = std::count(runs.begin(), runs.end(), 3);
            const int error_numerator = 2 * attempts * (size + 7)
                * (4 * length_two + 3 * (length_two + length_three));
            coupling_error += abs(mass) * std::min(error_denominator, error_numerator);
            if (2 * std::max({runs[1], runs[3], runs[5]}) > ones) majority_gap += mass;
        }
        if (total != 0) throw std::runtime_error("Difference mass must sum to zero");
        const Integer bound_denominator = 2 * denominator * fair_denominator * error_denominator;
        Integer gain = abs(future_gap) * error_denominator - coupling_error * fair_denominator;
        if (gain < 0) gain = 0;
        if (step == 48 && attempts == scale && 1000 * gain <= 7 * bound_denominator) {
            throw std::runtime_error("The exact lower bound must exceed 50.7%");
        }
        if (step == 48 && attempts == scale && 10000 * absolute_total >= 427 * 4 * denominator) {
            throw std::runtime_error("The exact upper bound must be below 54.27%");
        }
        std::cout << attempts << '/' << scale << ',' << step
                  << ',' << 0.5 + ratio(absolute_total, 4 * denominator)
                  << ',' << 0.5 + ratio(abs(majority_gap), 2 * denominator)
                  << ',' << 0.5 + ratio(gain, bound_denominator) << '\n';
    }
}

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "Usage: lr4_probe ATTEMPT_NUMERATOR ATTEMPT_DENOMINATOR GROWTH_STEPS\n";
        return 1;
    }
    const int attempts = std::stoi(argv[1]);
    const int scale = std::stoi(argv[2]);
    const int steps = std::stoi(argv[3]);
    if (scale < 1 || scale > 1000 || attempts < 0 || attempts > scale
            || steps < 1 || steps > max_steps) {
        std::cerr << "Use 0 <= numerator <= denominator <= 1000 and 1 to 48 growth steps.\n";
        return 1;
    }
    std::cout << std::setprecision(12);
    std::cout << "attempt_probability,insertions,optimal_accuracy,majority_one_run_accuracy,limiting_lower_bound\n";
    evaluate(attempts, scale, steps);
}
