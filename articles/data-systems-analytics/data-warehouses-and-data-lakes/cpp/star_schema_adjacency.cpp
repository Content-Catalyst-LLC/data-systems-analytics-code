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
    std::ifstream in("data/dimensional_model_tables.csv");
    if (!in) {
        std::cerr << "Unable to open data/dimensional_model_tables.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);

    std::cout << "Dimensional model adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::string table_name = cols[1];
        std::string role = cols[2];
        std::string grain = cols[3];
        std::string foreign_keys = cols[8].empty() ? "none" : cols[8];

        std::cout << table_name << " role=" << role
                  << " grain=\"" << grain << "\""
                  << " foreign_keys=" << foreign_keys << "\n";
    }

    return 0;
}
