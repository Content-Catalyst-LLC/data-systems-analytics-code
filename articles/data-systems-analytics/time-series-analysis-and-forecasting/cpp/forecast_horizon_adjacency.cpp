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
    std::ifstream in("data/forecast_horizons.csv");
    if (!in) {
        std::cerr << "Unable to open data/forecast_horizons.csv\n";
        return 1;
    }

    std::string line;
    std::getline(in, line);
    auto header = split_csv_line(line);

    int model_idx = -1, origin_idx = -1, horizon_idx = -1, forecast_idx = -1, status_idx = -1;
    for (int i = 0; i < static_cast<int>(header.size()); ++i) {
        if (header[i] == "model_id") model_idx = i;
        if (header[i] == "origin_date") origin_idx = i;
        if (header[i] == "horizon") horizon_idx = i;
        if (header[i] == "forecast") forecast_idx = i;
        if (header[i] == "release_status") status_idx = i;
    }

    std::cout << "Forecast horizon adjacency:\n";
    while (std::getline(in, line)) {
        auto cols = split_csv_line(line);
        std::cout << cols[model_idx] << " @ " << cols[origin_idx]
                  << " -> h=" << cols[horizon_idx]
                  << " forecast=" << cols[forecast_idx]
                  << " [status=" << cols[status_idx] << "]\n";
    }
    return 0;
}
