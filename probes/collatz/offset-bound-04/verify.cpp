// Verify the finite candidate range from bounds.py using a parity residue sieve.

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

using u64 = std::uint64_t;

struct Prefix {
    unsigned depth;
    unsigned odds;
    u64 residue;
    u64 multiplier;
    u64 offset;
};

struct Certificate {
    unsigned depth, sieve_depth, verify_depth;
    u64 early_bound, candidate_bound;
    unsigned record_depth;
    std::vector<unsigned> required_odds;
};

Certificate read_certificate() {
    Certificate certificate{};
    auto& [depth, sieve, verify, early, bound, record, required] = certificate;
    if (!(std::cin >> depth >> sieve >> verify >> early >> bound >> record)
        || sieve < 1 || sieve > 24 || verify < sieve || verify > depth
        || early > bound || bound == std::numeric_limits<u64>::max()
        || record == 0 || record > depth) {
        throw std::runtime_error("invalid certificate header");
    }
    required.resize(static_cast<std::size_t>(verify) + 1);
    for (unsigned d = 0; d <= verify; ++d) {
        if (!(std::cin >> required[d]) || required[d] > d
            || (d > 0 && (required[d] < required[d - 1]
                          || required[d] > required[d - 1] + 1))) {
            throw std::runtime_error("invalid odd-count thresholds");
        }
    }
    return certificate;
}

unsigned check_start(u64 start, u64 value, unsigned depth, unsigned odds,
                     const Certificate& cert) {
    while (depth < cert.verify_depth) {
        if (value & 1) {
            if (value > (std::numeric_limits<u64>::max() - 1) / 3) {
                throw std::runtime_error("integer overflow in direct iteration");
            }
            value = (3 * value + 1) / 2;
            ++odds;
        } else {
            value /= 2;
        }
        ++depth;
        if (odds < cert.required_odds[depth]) {
            if (value >= start) {
                throw std::runtime_error("offset exception at start " + std::to_string(start));
            }
            return depth;
        }
        if (value < start) {
            throw std::runtime_error("descent before coefficient contraction");
        }
    }
    throw std::runtime_error("verification depth exhausted at start " + std::to_string(start));
}

int main() {
    try {
        const auto cert = read_certificate();
        u64 sieve_classes = 0;
        u64 directly_checked = 0;
        unsigned maximum_depth = 0;
        u64 depth_witness = 0;
        auto update_max = [&](u64 start, unsigned d) {
            if (d > maximum_depth || (d == maximum_depth && start < depth_witness)) {
                maximum_depth = d;
                depth_witness = start;
            }
        };

        for (u64 n = 2; n <= cert.early_bound; ++n) {
            update_max(n, check_start(n, n, 0, 0, cert));
            ++directly_checked;
        }

        const u64 first = std::max<u64>(2, cert.early_bound + 1);
        std::vector<Prefix> stack{{0, 0, 0, 1, 0}};
        while (!stack.empty()) {
            const auto [d, odds, residue, multiplier, offset] = stack.back();
            stack.pop_back();
            if (odds < cert.required_odds[d]) {
                continue;
            }
            const u64 modulus = u64{1} << d;
            // For d <= 24, the numerator is below 6^24, which fits in u64.
            const u64 endpoint = (multiplier * residue + offset) >> d;
            if (d == cert.sieve_depth) {
                ++sieve_classes;
                const u64 lift = first > residue ? (first - residue - 1) / modulus + 1 : 0;
                if (residue > cert.candidate_bound
                    || lift > (cert.candidate_bound - residue) / modulus) {
                    continue;
                }
                u64 start = residue + lift * modulus;
                if (lift > (std::numeric_limits<u64>::max() - endpoint) / multiplier) {
                    throw std::runtime_error("integer overflow lifting a residue");
                }
                u64 value = endpoint + lift * multiplier;
                while (true) {
                    update_max(start, check_start(start, value, d, odds, cert));
                    ++directly_checked;
                    if (cert.candidate_bound - start < modulus) {
                        break;
                    }
                    if (value > std::numeric_limits<u64>::max() - multiplier) {
                        throw std::runtime_error("integer overflow advancing a residue");
                    }
                    start += modulus;
                    value += multiplier;
                }
                continue;
            }
            const u64 odd_residue = residue + ((endpoint & 1) ? 0 : modulus);
            const u64 even_residue = residue + ((endpoint & 1) ? modulus : 0);
            stack.push_back({d + 1, odds, even_residue, multiplier, offset});
            stack.push_back({d + 1, odds + 1, odd_residue, 3 * multiplier, 3 * offset + modulus});
        }

        std::cout << "{\n"
                  << "  \"certificate_depth\": " << cert.depth << ",\n"
                  << "  \"record_depth\": " << cert.record_depth << ",\n"
                  << "  \"largest_possible_exception\": " << cert.candidate_bound << ",\n"
                  << "  \"sieve_depth\": " << cert.sieve_depth << ",\n"
                  << "  \"sieve_cutoff\": " << cert.early_bound << ",\n"
                  << "  \"sieve_surviving_residue_classes\": " << sieve_classes << ",\n"
                  << "  \"starts_directly_checked\": " << directly_checked << ",\n"
                  << "  \"max_first_contraction\": " << maximum_depth << ",\n"
                  << "  \"least_start_at_max_first_contraction\": " << depth_witness << ",\n"
                  << "  \"offset_exceptions\": 0\n}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
