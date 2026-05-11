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
    std::ifstream in("data/product_lineage.csv");
    if (!in) {
        std::cerr << "Unable to open data/product_lineage.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int product_idx = -1;
    int source_idx = -1;
    int surface_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "product_id") product_idx = i;
        if (header[i] == "upstream_source") source_idx = i;
        if (header[i] == "consumption_surface") surface_idx = i;
    }

    std::cout << "Product lineage adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[source_idx] << " -> "
                  << cols[product_idx] << " -> "
                  << cols[surface_idx] << "\n";
    }

    return 0;
}
