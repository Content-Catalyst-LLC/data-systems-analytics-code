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
    std::ifstream in("data/decision_thresholds.csv");
    if (!in) {
        std::cerr << "Unable to open data/decision_thresholds.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int metric_idx = -1;
    int owner_idx = -1;
    int path_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "metric_id") metric_idx = i;
        if (header[i] == "decision_owner") owner_idx = i;
        if (header[i] == "escalation_path") path_idx = i;
    }

    std::cout << "BI alert-to-decision pathways:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[metric_idx] << " -> "
                  << cols[owner_idx] << " -> "
                  << cols[path_idx] << "\n";
    }

    return 0;
}
