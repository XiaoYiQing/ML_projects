
#include <iostream>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <algorithm>

// ============================================================================
//      Implementation 1: Original Truncating Version
// ============================================================================
int32_t exp_decay_q16_tableless(int32_t x_q16) {
    if (x_q16 < 0) return 0;

    int64_t z_64 = (static_cast<int64_t>(x_q16) * 94548) >> 16;
    int32_t z = static_cast<int32_t>(z_64);

    int32_t z_int = z >> 16;
    int32_t z_frac = z & 0xFFFF;

    if (z_int >= 31) return 0;

    int64_t f1 = z_frac;
    int64_t f2 = (f1 * f1) >> 16;
    int64_t f3 = (f2 * f1) >> 16;
    int64_t f4 = (f3 * f1) >> 16;

    int32_t exp_frac = 65536
        - ((45417 * f1) >> 16)
        + ((15738 * f2) >> 16)
        - ((3622 * f3) >> 16)
        + ((533 * f4) >> 16);

    return exp_frac >> z_int;
}

// ============================================================================
//      Implementation 2: New Rounded Version
// ============================================================================
int32_t exp_decay_q16_tableless_rounded(int32_t x_q16) {
    if (x_q16 < 0) return 0;

    // Shift with rounding offset (+32768)
    int64_t z_64 = (static_cast<int64_t>(x_q16) * 94548 + 32768) >> 16;
    int32_t z = static_cast<int32_t>(z_64);

    int32_t z_int = z >> 16;
    int32_t z_frac = z & 0xFFFF;

    if (z_int >= 31) return 0;

    int64_t f1 = z_frac;
    int64_t f2 = ((f1 * f1) + 32768) >> 16;
    int64_t f3 = ((f2 * f1) + 32768) >> 16;
    int64_t f4 = ((f3 * f1) + 32768) >> 16;

    int32_t exp_frac = 65536
        - (((45417 * f1) + 32768) >> 16)
        + (((15738 * f2) + 32768) >> 16)
        - (((3622 * f3)  + 32768) >> 16)
        + (((533 * f4)   + 32768) >> 16);

    // Dynamic rounding based on variable shift amount
    if (z_int > 0) {
        int32_t final_rounding_offset = 1 << (z_int - 1);
        return (exp_frac + final_rounding_offset) >> z_int;
    }
   
    return exp_frac;
}

// ============================================================================
//      Main Benchmarking & Comparison Block
// ============================================================================
int main() {
    // Stats for original version
    double orig_max_abs_error = 0.0;
    double orig_total_squared_error = 0.0;
   
    // Stats for rounded version
    double round_max_abs_error = 0.0;
    double round_total_squared_error = 0.0;

    uint64_t count = 0;
    int32_t max_test_range = 25 * 65536; // Range covers non-zero inputs until total underflow

    std::cout << "Running side-by-side exhaustive error comparison..." << std::endl;

    for (int32_t x_q16 = 0; x_q16 <= max_test_range; ++x_q16) {
        double x_float = static_cast<double>(x_q16) / 65536.0;
        double expected_q16 = std::exp(-x_float) * 65536.0;

        // Evaluate Original
        int32_t orig_actual = exp_decay_q16_tableless(x_q16);
        double orig_error = std::abs(expected_q16 - orig_actual);
        orig_total_squared_error += orig_error * orig_error;
        orig_max_abs_error = std::max(orig_max_abs_error, orig_error);

        // Evaluate Rounded
        int32_t round_actual = exp_decay_q16_tableless_rounded(x_q16);
        double round_error = std::abs(expected_q16 - round_actual);
        round_total_squared_error += round_error * round_error;
        round_max_abs_error = std::max(round_max_abs_error, round_error);

        count++;
    }

    double orig_rmse = std::sqrt(orig_total_squared_error / count);
    double round_rmse = std::sqrt(round_total_squared_error / count);

    std::cout << std::fixed << std::setprecision(4);
    std::cout << "\n=================== BENCHMARK RESULTS ===================" << std::endl;
    std::cout << "Metric                 | Original (Truncated) | Rounded (Nearest)" << std::endl;
    std::cout << "-----------------------|----------------------|------------------" << std::endl;
    std::cout << "Max Absolute Error     | " << std::setw(12) << orig_max_abs_error << " LSBs | " << std::setw(12) << round_max_abs_error << " LSBs" << std::endl;
    std::cout << "Root Mean Sq Error     | " << std::setw(12) << orig_rmse         << " LSBs | " << std::setw(12) << round_rmse         << " LSBs" << std::endl;
    std::cout << "=========================================================" << std::endl;

    // Show percentage improvements
    double max_err_imp = ((orig_max_abs_error - round_max_abs_error) / orig_max_abs_error) * 100.0;
    double rmse_imp = ((orig_rmse - round_rmse) / orig_rmse) * 100.0;
   
    std::cout << "\nImprovement Summary:" << std::endl;
    std::cout << "* Worst-case LSB error reduced by: " << max_err_imp << "%" << std::endl;
    std::cout << "* Average error variance (RMSE) reduced by: " << rmse_imp << "%" << std::endl;

    return 0;
}
