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
    std::ifstream in("data/causal_study_registry.csv");
    if (!in) {
        std::cerr << "Unable to open data/causal_study_registry.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int study_idx = -1, intervention_idx = -1, comparison_idx = -1, outcome_idx = -1, design_idx = -1, estimand_idx = -1;
    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "study_id") study_idx = i;
        if (header[i] == "intervention") intervention_idx = i;
        if (header[i] == "comparison") comparison_idx = i;
        if (header[i] == "outcome") outcome_idx = i;
        if (header[i] == "design_type") design_idx = i;
        if (header[i] == "estimand") estimand_idx = i;
    }

    std::cout << "Causal design adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[study_idx] << " -> "
                  << cols[intervention_idx] << " vs " << cols[comparison_idx]
                  << " -> " << cols[outcome_idx]
                  << " [design=" << cols[design_idx]
                  << ", estimand=" << cols[estimand_idx] << "]\n";
    }
    return 0;
}
