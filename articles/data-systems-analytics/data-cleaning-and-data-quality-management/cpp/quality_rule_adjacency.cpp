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
    std::ifstream in("data/quality_rules.csv");
    if (!in) {
        std::cerr << "Unable to open data/quality_rules.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int rule_idx = -1, dimension_idx = -1, name_idx = -1, field_idx = -1, severity_idx = -1, owner_idx = -1, status_idx = -1;
    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "rule_id") rule_idx = i;
        if (header[i] == "dimension") dimension_idx = i;
        if (header[i] == "rule_name") name_idx = i;
        if (header[i] == "field_name") field_idx = i;
        if (header[i] == "severity") severity_idx = i;
        if (header[i] == "owner") owner_idx = i;
        if (header[i] == "status") status_idx = i;
    }

    std::cout << "Quality rule adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[rule_idx] << " -> "
                  << cols[dimension_idx] << " -> "
                  << cols[field_idx] << " rule=" << cols[name_idx]
                  << " severity=" << cols[severity_idx]
                  << " owner=" << cols[owner_idx]
                  << " [status=" << cols[status_idx] << "]\n";
    }
    return 0;
}
