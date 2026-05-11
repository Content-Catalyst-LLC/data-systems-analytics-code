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
    std::ifstream in("data/hierarchy_edges.csv");
    if (!in) {
        std::cerr << "Unable to open data/hierarchy_edges.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int parent_idx = -1;
    int child_idx = -1;
    int relation_idx = -1;
    int view_idx = -1;
    int confidence_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "parent_entity_id") parent_idx = i;
        if (header[i] == "child_entity_id") child_idx = i;
        if (header[i] == "relationship_type") relation_idx = i;
        if (header[i] == "relationship_view") view_idx = i;
        if (header[i] == "confidence") confidence_idx = i;
    }

    std::cout << "Entity hierarchy adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[parent_idx] << " -> "
                  << cols[child_idx] << " ["
                  << cols[relation_idx] << ", view=" << cols[view_idx]
                  << ", confidence=" << cols[confidence_idx] << "]\n";
    }

    return 0;
}
