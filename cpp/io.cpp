#include <array>
#include <cstdio>
#include <iostream>
#include <memory>
#include <sstream>
#include <vector>

bool isprocessrunnig(std::string name) {

  std::string str = "pgrep " + name;
  FILE *is_running = popen(str.c_str(), "r");

  char buf[120];
  std::string output;
  while (fgets(buf, sizeof(buf), is_running)) {
    output += buf;
  }

  pclose(is_running);

  if (output.empty())
    return 0;
  else
    return 1;
}

std::vector<std::string> list_models() {
  std::vector<std::string> output_modesl;

  if (isprocessrunnig("ollama") == true) {

    FILE *models = popen("ollama list", "r");
    char buf[120];
    std::string output;

    while (fgets(buf, sizeof(buf), models)) {
      output += buf;
    }

    pclose(models);

    // Process output into a list
    std::istringstream iss(output);
    std::string line;
    bool first_line = true;
    while (std::getline(iss, line)) {
      if (first_line) {
        first_line = false;
        continue;
      } // skip header
      std::string model_name = line.substr(0, line.find(' '));

      output_modesl.push_back(model_name);
    }

    return output_modesl;
  } else {
    std::cout << "No models are found" << std::endl;
    return {};
  }
}

// int main(int argc, char *argv[]) {
//   // assign return value to a variable
//   std::vector<std::string> myModels = list_models();
//
//   // use it
//   for (const auto &model : myModels) {
//     std::cout << model << "\n";
//   }
//   return 0;
// }
