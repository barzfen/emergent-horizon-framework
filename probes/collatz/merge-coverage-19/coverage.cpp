#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>

namespace {

constexpr int max_depth = 32;
constexpr int max_run = 70;
using Count = std::uint64_t;

struct Prefix {
    std::int64_t x;
    std::int64_t z;
    int x_odds;
    int z_odds;
    int required_run;
};

class Census {
public:
    explicit Census(int horizon) : horizon_(horizon) {
        powers_of_three_[0] = 1;
        for (int k = 1; k <= max_depth + 1; ++k) {
            powers_of_three_[k] = 3 * powers_of_three_[k - 1];
        }

        for (int depth = 1; depth <= horizon_; ++depth) {
            for (int odds = 0; odds <= depth; ++odds) {
                // Find the least k with (3/2)^k * 3^odds / 2^depth >= 1.
                unsigned __int128 numerator = powers_of_three_[odds];
                unsigned __int128 denominator = Count{1} << depth;
                int run = 0;
                while (numerator < denominator) {
                    numerator *= 3;
                    denominator *= 2;
                    ++run;
                }
                required_run_[depth][odds] = run;
            }
        }
    }

    void run() {
        // z is even and x = 3z + 2. Both first suffix steps halve.
        visit(1, {1, 0, 0, 0, 1 + required_run_[1][0]});
    }

    void print() const {
        for (int depth = 1; depth <= horizon_; ++depth) {
            for (int run = 0; run < max_run; ++run) {
                if (first_hits_[depth][run] != 0) {
                    std::cout << "hit " << depth << ' ' << run << ' '
                              << first_hits_[depth][run] << '\n';
                }
            }
        }
        for (int run = 0; run < max_run; ++run) {
            if (live_[run] != 0) {
                std::cout << "live " << horizon_ << ' ' << run << ' '
                          << live_[run] << '\n';
            }
        }
    }

private:
    static std::int64_t step(std::int64_t value, int odd) {
        return odd ? (3 * value + 1) / 2 : value / 2;
    }

    void visit(int depth, const Prefix& prefix) {
        // The original run has a lead of one odd step before the suffixes.
        if (prefix.z_odds == prefix.x_odds + 1 && prefix.x == prefix.z) {
            ++first_hits_[depth][prefix.required_run];
            return;
        }
        if (depth == horizon_) {
            ++live_[prefix.required_run];
            return;
        }

        // Appending a one to the input residue adds 2^depth to its
        // representative z. The two affine output increments are odd.
        for (int bit = 0; bit <= 1; ++bit) {
            const auto x = prefix.x + bit * powers_of_three_[prefix.x_odds + 1];
            const auto z = prefix.z + bit * powers_of_three_[prefix.z_odds];
            const int x_odd = x % 2;
            const int z_odd = z % 2;
            const int x_odds = prefix.x_odds + x_odd;
            const int z_odds = prefix.z_odds + z_odd;
            const int run = std::max({
                prefix.required_run,
                required_run_[depth + 1][x_odds],
                1 + required_run_[depth + 1][z_odds],
            });
            visit(depth + 1, {step(x, x_odd), step(z, z_odd), x_odds, z_odds, run});
        }
    }

    int horizon_;
    std::int64_t powers_of_three_[max_depth + 2]{};
    int required_run_[max_depth + 1][max_depth + 1]{};
    Count first_hits_[max_depth + 1][max_run]{};
    Count live_[max_run]{};
};

}  // namespace

int main(int argc, char** argv) {
    int horizon = max_depth;
    if (argc == 2) {
        try {
            std::size_t consumed;
            const std::string argument = argv[1];
            horizon = std::stoi(argument, &consumed);
            if (consumed != argument.size()) {
                horizon = 0;
            }
        } catch (const std::exception&) {
            horizon = 0;
        }
    } else if (argc > 2) {
        horizon = 0;
    }
    if (horizon < 2 || horizon > max_depth) {
        std::cerr << "Usage: coverage [depth between 2 and 32]\n";
        return 1;
    }

    Census census(horizon);
    census.run();
    census.print();
}
