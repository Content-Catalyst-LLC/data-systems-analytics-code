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
    std::ifstream in("data/model_registry.csv");
    if (!in) {
        std::cerr << "Unable to open data/model_registry.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int id_idx = -1;
    int task_idx = -1;
    int family_idx = -1;
    int target_idx = -1;
    int status_idx = -1;
    int risk_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "model_id") id_idx = i;
        if (header[i] == "task_type") task_idx = i;
        if (header[i] == "model_family") family_idx = i;
        if (header[i] == "prediction_target") target_idx = i;
        if (header[i] == "status") status_idx = i;
        if (header[i] == "risk_level") risk_idx = i;
    }

    std::cout << "Predictive model evidence adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[id_idx] << " -> "
                  << cols[task_idx] << " -> "
                  << cols[family_idx] << " -> "
                  << cols[target_idx]
                  << " [status=" << cols[status_idx]
                  << ", risk=" << cols[risk_idx] << "]\n";
    }

    return 0;
}
