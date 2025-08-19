#include "io.h"
#include <cstdio>
#include <unistd.h>
#include <cstdlib>
#include <iostream>
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

std::vector<std::string> modelCheck() {
  std::vector<std::string> output_models;

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

    output_models.push_back(model_name);
  }

  return output_models;
}

std::vector<std::string> list_models() {
  std::vector<std::string> output_models;

  if (isprocessrunnig("ollama")) {
    std::cout << "debug info" << std::endl;
    return modelCheck();
  } else {
    system("nohup ollama serve > /dev/null 2>&1 &");

    std::cout << "Starting ollama..." << std::endl;

    // Wait until ollama is actually running
    int retries = 10;
    while (retries-- > 0) {
      if (isprocessrunnig("ollama")) {
        std::cout << "Ollama started successfully" << std::endl;
        output_models = modelCheck();
        break;
      }
      sleep(1); // wait 1 second before checking again
    }

    if (output_models.empty()) {
      std::cout << "Failed to start ollama or no models found" << std::endl;
    }

    return output_models;
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
