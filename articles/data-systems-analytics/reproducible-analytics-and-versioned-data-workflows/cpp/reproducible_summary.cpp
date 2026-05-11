#include <algorithm>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

struct Summary {
    int records = 0;
    int total = 0;
};

std::vector<std::string> split_csv_line(const std::string& line) {
    std::vector<std::string> out;
    std::stringstream ss(line);
    std::string item;

    while (std::getline(ss, item, ',')) {
        out.push_back(item);
    }

    return out;
}

int main() {
    std::string input_path = "data/sample_events.csv";
    std::string output_path = "outputs/run_summary_cpp.csv";

    std::ifstream in(input_path);
    if (!in) {
        std::cerr << "Unable to open " << input_path << "\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int system_idx = -1;
    int value_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "system") system_idx = i;
        if (header[i] == "value") value_idx = i;
    }

    std::map<std::string, Summary> summaries;

    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        auto& s = summaries[cols[system_idx]];
        s.records += 1;
        s.total += std::stoi(cols[value_idx]);
    }

    std::ofstream out(output_path);
    out << "system,records,total_value,average_value\n";

    for (const auto& [system, summary] : summaries) {
        double average = static_cast<double>(summary.total) / summary.records;
        out << system << "," << summary.records << "," << summary.total << ","
            << std::fixed << std::setprecision(2) << average << "\n";
    }

    std::cout << "C++ workflow complete: " << output_path << "\n";
    return 0;
}
