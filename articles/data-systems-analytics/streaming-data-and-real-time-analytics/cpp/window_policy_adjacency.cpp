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
    std::ifstream in("data/window_definitions.csv");
    if (!in) {
        std::cerr << "Unable to open data/window_definitions.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int window_idx = -1, type_idx = -1, size_idx = -1, lateness_idx = -1, trigger_idx = -1, mode_idx = -1, status_idx = -1;
    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "window_id") window_idx = i;
        if (header[i] == "window_type") type_idx = i;
        if (header[i] == "size_seconds") size_idx = i;
        if (header[i] == "allowed_lateness_seconds") lateness_idx = i;
        if (header[i] == "trigger_policy") trigger_idx = i;
        if (header[i] == "output_mode") mode_idx = i;
        if (header[i] == "status") status_idx = i;
    }

    std::cout << "Window policy adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[window_idx] << " -> "
                  << cols[type_idx] << " size=" << cols[size_idx]
                  << " lateness=" << cols[lateness_idx]
                  << " trigger=" << cols[trigger_idx]
                  << " output=" << cols[mode_idx]
                  << " [status=" << cols[status_idx] << "]\n";
    }
    return 0;
}
