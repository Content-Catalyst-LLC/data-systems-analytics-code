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
    std::ifstream in("data/orchestration_runs.csv");
    if (!in) {
        std::cerr << "Unable to open data/orchestration_runs.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int run_idx = -1, pipeline_idx = -1, batch_idx = -1, code_idx = -1, loaded_idx = -1, rejected_idx = -1, status_idx = -1;
    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "run_id") run_idx = i;
        if (header[i] == "pipeline_name") pipeline_idx = i;
        if (header[i] == "source_batch_id") batch_idx = i;
        if (header[i] == "code_version") code_idx = i;
        if (header[i] == "loaded_rows") loaded_idx = i;
        if (header[i] == "rejected_rows") rejected_idx = i;
        if (header[i] == "status") status_idx = i;
    }

    std::cout << "Transformation lineage adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[run_idx] << " -> "
                  << cols[pipeline_idx] << " -> "
                  << cols[batch_idx] << " code=" << cols[code_idx]
                  << " loaded=" << cols[loaded_idx]
                  << " rejected=" << cols[rejected_idx]
                  << " [status=" << cols[status_idx] << "]\n";
    }
    return 0;
}
