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
    std::ifstream in("data/exploration_questions.csv");
    if (!in) {
        std::cerr << "Unable to open data/exploration_questions.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int q_idx = -1, mode_idx = -1, priority_idx = -1, status_idx = -1;
    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "question_id") q_idx = i;
        if (header[i] == "analysis_mode") mode_idx = i;
        if (header[i] == "priority") priority_idx = i;
        if (header[i] == "status") status_idx = i;
    }

    std::cout << "Exploration question adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[q_idx] << " -> "
                  << cols[mode_idx]
                  << " [priority=" << cols[priority_idx]
                  << ", status=" << cols[status_idx] << "]\n";
    }
    return 0;
}
