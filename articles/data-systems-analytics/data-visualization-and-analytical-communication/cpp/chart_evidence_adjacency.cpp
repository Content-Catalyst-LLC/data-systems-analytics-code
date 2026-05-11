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
    std::ifstream in("data/evidence_links.csv");
    if (!in) {
        std::cerr << "Unable to open data/evidence_links.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int visual_idx = -1;
    int source_idx = -1;
    int method_idx = -1;
    int trace_idx = -1;
    int review_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "visual_id") visual_idx = i;
        if (header[i] == "source_asset") source_idx = i;
        if (header[i] == "method_reference") method_idx = i;
        if (header[i] == "traceability_status") trace_idx = i;
        if (header[i] == "review_status") review_idx = i;
    }

    std::cout << "Visualization evidence adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[visual_idx] << " -> "
                  << cols[source_idx] << " -> "
                  << cols[method_idx]
                  << " [traceability=" << cols[trace_idx]
                  << ", review=" << cols[review_idx] << "]\n";
    }

    return 0;
}
