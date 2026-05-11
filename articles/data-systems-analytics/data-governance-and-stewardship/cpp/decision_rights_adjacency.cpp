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
    std::ifstream in("data/decision_rights.csv");
    if (!in) {
        std::cerr << "Unable to open data/decision_rights.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int domain_idx = -1;
    int area_idx = -1;
    int approver_idx = -1;
    int escalation_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "domain") domain_idx = i;
        if (header[i] == "decision_area") area_idx = i;
        if (header[i] == "approver_role") approver_idx = i;
        if (header[i] == "escalation_path") escalation_idx = i;
    }

    std::cout << "Decision-rights escalation adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[domain_idx] << ":" << cols[area_idx]
                  << " -> approver=" << cols[approver_idx]
                  << " -> escalation=" << cols[escalation_idx] << "\n";
    }

    return 0;
}
