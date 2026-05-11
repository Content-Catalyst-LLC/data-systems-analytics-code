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
    std::ifstream in("data/feature_registry.csv");
    if (!in) {
        std::cerr << "Unable to open data/feature_registry.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int feature_idx = -1;
    int source_idx = -1;
    int transformation_idx = -1;
    int leakage_idx = -1;
    int status_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "feature_name") feature_idx = i;
        if (header[i] == "source_field") source_idx = i;
        if (header[i] == "transformation") transformation_idx = i;
        if (header[i] == "leakage_risk") leakage_idx = i;
        if (header[i] == "status") status_idx = i;
    }

    std::cout << "Feature-to-source adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[source_idx] << " -> "
                  << cols[transformation_idx] << " -> "
                  << cols[feature_idx]
                  << " [leakage=" << cols[leakage_idx]
                  << ", status=" << cols[status_idx] << "]\n";
    }

    return 0;
}
