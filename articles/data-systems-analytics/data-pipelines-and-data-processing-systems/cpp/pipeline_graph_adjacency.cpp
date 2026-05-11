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
    std::ifstream in("data/pipeline_stages.csv");
    if (!in) {
        std::cerr << "Unable to open data/pipeline_stages.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int pipeline_idx = -1, stage_idx = -1, type_idx = -1, upstream_idx = -1, downstream_idx = -1, status_idx = -1;
    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "pipeline_name") pipeline_idx = i;
        if (header[i] == "stage_name") stage_idx = i;
        if (header[i] == "stage_type") type_idx = i;
        if (header[i] == "upstream_stage") upstream_idx = i;
        if (header[i] == "downstream_stage") downstream_idx = i;
        if (header[i] == "status") status_idx = i;
    }

    std::cout << "Pipeline graph adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[pipeline_idx] << ": "
                  << (cols[upstream_idx].empty() ? "SOURCE" : cols[upstream_idx])
                  << " -> " << cols[stage_idx]
                  << " -> " << (cols[downstream_idx].empty() ? "SINK" : cols[downstream_idx])
                  << " type=" << cols[type_idx]
                  << " [status=" << cols[status_idx] << "]\n";
    }
    return 0;
}
