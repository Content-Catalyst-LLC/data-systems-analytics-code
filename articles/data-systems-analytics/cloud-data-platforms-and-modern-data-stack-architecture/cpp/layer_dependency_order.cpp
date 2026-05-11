#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <set>
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
    std::ifstream in("data/pipeline_catalog.csv");
    if (!in) {
        std::cerr << "Unable to open data/pipeline_catalog.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int source_idx = -1;
    int target_idx = -1;
    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "source_layer") source_idx = i;
        if (header[i] == "target_layer") target_idx = i;
    }

    std::map<std::string, std::set<std::string>> graph;
    std::map<std::string, int> indegree;

    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::string source = cols[source_idx];
        std::string target = cols[target_idx];
        graph[source].insert(target);
        if (!indegree.count(source)) indegree[source] = 0;
        indegree[target] += 1;
    }

    std::queue<std::string> q;
    for (const auto& pair : indegree) {
        if (pair.second == 0) q.push(pair.first);
    }

    std::cout << "Approximate layer dependency order:\n";
    while (!q.empty()) {
        auto node = q.front();
        q.pop();
        std::cout << "- " << node << "\n";
        for (const auto& next : graph[node]) {
            indegree[next] -= 1;
            if (indegree[next] == 0) q.push(next);
        }
    }

    return 0;
}
