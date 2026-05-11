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
    std::ifstream in("data/semantic_lineage.csv");
    if (!in) {
        std::cerr << "Unable to open data/semantic_lineage.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int upstream_idx = -1;
    int downstream_idx = -1;
    int relation_idx = -1;
    int impact_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "upstream_model") upstream_idx = i;
        if (header[i] == "downstream_model") downstream_idx = i;
        if (header[i] == "relationship_type") relation_idx = i;
        if (header[i] == "impact_level") impact_idx = i;
    }

    std::cout << "Semantic lineage adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[upstream_idx] << " -> "
                  << cols[downstream_idx] << " ["
                  << cols[relation_idx] << ", impact=" << cols[impact_idx] << "]\n";
    }

    return 0;
}
