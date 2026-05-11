#include <fstream>
#include <functional>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Shard {
    std::string shard_id;
    int start;
    int end;
    std::string leader;
    std::string replicas;
};

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
    std::ifstream in("data/shard_map.csv");
    if (!in) {
        std::cerr << "Unable to open data/shard_map.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);

    std::vector<Shard> shards;
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        shards.push_back({cols[0], std::stoi(cols[1]), std::stoi(cols[2]), cols[3], cols[4]});
    }

    std::vector<std::string> keys = {"user:1001", "order:2050", "cart:9188", "session:8801", "ledger:4555"};
    std::hash<std::string> hasher;

    std::cout << "C++ shard routing examples:\n";
    for (const auto& key : keys) {
        int bucket = static_cast<int>(hasher(key) % 10000);
        for (const auto& shard : shards) {
            if (bucket >= shard.start && bucket <= shard.end) {
                std::cout << key << " bucket=" << bucket
                          << " -> " << shard.shard_id
                          << " leader=" << shard.leader
                          << " replicas=" << shard.replicas << "\n";
                break;
            }
        }
    }

    return 0;
}
