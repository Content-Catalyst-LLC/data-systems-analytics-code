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
    std::ifstream in("data/lineage_events.csv");
    if (!in) {
        std::cerr << "Unable to open data/lineage_events.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int source_idx = -1;
    int target_idx = -1;
    int job_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "source_system") source_idx = i;
        if (header[i] == "target_asset") target_idx = i;
        if (header[i] == "job_name") job_idx = i;
    }

    std::cout << "Integration lineage adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[source_idx] << " -> "
                  << cols[job_idx] << " -> "
                  << cols[target_idx] << "\n";
    }

    return 0;
}
