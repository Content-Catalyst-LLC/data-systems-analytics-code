#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> split_csv_line(const std::string& line) {
    std::stringstream ss(line);
    std::string item;
    std::vector<std::string> out;
    while (std::getline(ss, item, ',')) {
        out.push_back(item);
    }
    return out;
}

int main() {
    std::ifstream in("data/inference_claims.csv");
    if (!in) {
        std::cerr << "Unable to open data/inference_claims.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int claim_idx = -1, model_idx = -1, type_idx = -1, effect_idx = -1, p_idx = -1, status_idx = -1;
    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "claim_id") claim_idx = i;
        if (header[i] == "model_id") model_idx = i;
        if (header[i] == "claim_type") type_idx = i;
        if (header[i] == "effect_size") effect_idx = i;
        if (header[i] == "p_value") p_idx = i;
        if (header[i] == "claim_status") status_idx = i;
    }

    std::cout << "Inference claim adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[claim_idx] << " -> "
                  << cols[model_idx] << " -> "
                  << cols[type_idx] << " effect=" << cols[effect_idx]
                  << " p=" << cols[p_idx]
                  << " [status=" << cols[status_idx] << "]\n";
    }
    return 0;
}
