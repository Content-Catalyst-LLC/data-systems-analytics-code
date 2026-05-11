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
    std::ifstream in("data/constraint_inventory.csv");
    if (!in) {
        std::cerr << "Unable to open data/constraint_inventory.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int table_idx = -1, col_idx = -1, type_idx = -1, ref_table_idx = -1, ref_col_idx = -1, status_idx = -1;
    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "table_name") table_idx = i;
        if (header[i] == "column_name") col_idx = i;
        if (header[i] == "constraint_type") type_idx = i;
        if (header[i] == "referenced_table") ref_table_idx = i;
        if (header[i] == "referenced_column") ref_col_idx = i;
        if (header[i] == "status") status_idx = i;
    }

    std::cout << "Relational constraint graph:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        if (cols[type_idx] == "foreign_key") {
            std::cout << cols[table_idx] << "." << cols[col_idx]
                      << " -> " << cols[ref_table_idx] << "." << cols[ref_col_idx]
                      << " [status=" << cols[status_idx] << "]\n";
        }
    }

    return 0;
}
