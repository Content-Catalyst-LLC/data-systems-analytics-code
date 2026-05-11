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
    std::ifstream in("data/story_points.csv");
    if (!in) {
        std::cerr << "Unable to open data/story_points.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int dash_idx = -1;
    int sequence_idx = -1;
    int title_idx = -1;
    int claim_idx = -1;
    int view_idx = -1;

    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "dashboard_id") dash_idx = i;
        if (header[i] == "sequence_order") sequence_idx = i;
        if (header[i] == "story_title") title_idx = i;
        if (header[i] == "claim_id") claim_idx = i;
        if (header[i] == "linked_view_id") view_idx = i;
    }

    std::cout << "Story point evidence adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[dash_idx] << " story_point_" << cols[sequence_idx]
                  << " -> " << cols[claim_idx]
                  << " -> view=" << cols[view_idx]
                  << " [" << cols[title_idx] << "]\n";
    }

    return 0;
}
