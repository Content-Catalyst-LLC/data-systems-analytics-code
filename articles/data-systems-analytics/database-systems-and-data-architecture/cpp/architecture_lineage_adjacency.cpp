#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> split_csv_line(const std::string& line) {
    std::stringstream ss(line);
    std::string item;
    std::vector<std::string> out;
    bool in_quotes = false;
    std::string current;

    for (char c : line) {
        if (c == '"') {
            in_quotes = !in_quotes;
        } else if (c == ',' && !in_quotes) {
            out.push_back(current);
            current.clear();
        } else {
            current.push_back(c);
        }
    }
    out.push_back(current);
    return out;
}

int main() {
    std::ifstream in("data/integration_lineage.csv");
    if (!in) {
        std::cerr << "Unable to open data/integration_lineage.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);

    std::cout << "Database architecture lineage adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[1] << " -> " << cols[2]
                  << " flow=" << cols[3]
                  << " lineage=" << cols[5]
                  << " quality_gate=" << cols[7]
                  << " status=" << cols[9] << "\n";
    }

    return 0;
}
