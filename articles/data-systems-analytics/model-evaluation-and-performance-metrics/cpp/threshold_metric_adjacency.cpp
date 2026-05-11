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
    std::ifstream in("data/threshold_policies.csv");
    if (!in) {
        std::cerr << "Unable to open data/threshold_policies.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int model_idx = -1;
    int policy_idx = -1;
    int threshold_idx = -1;
    int owner_idx = -1;
    int status_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "model_id") model_idx = i;
        if (header[i] == "policy_name") policy_idx = i;
        if (header[i] == "threshold") threshold_idx = i;
        if (header[i] == "decision_owner") owner_idx = i;
        if (header[i] == "review_status") status_idx = i;
    }

    std::cout << "Threshold policy adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[model_idx] << " -> "
                  << cols[policy_idx]
                  << " [threshold=" << cols[threshold_idx]
                  << ", owner=" << cols[owner_idx]
                  << ", status=" << cols[status_idx] << "]\n";
    }

    return 0;
}
