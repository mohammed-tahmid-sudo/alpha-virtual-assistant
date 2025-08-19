#include "whisper.h"
#include <iostream>
#include <vector>

int main() {
    // Load the model
    struct whisper_context *ctx = whisper_init_from_file("models/ggml-base.en.bin");
    if (!ctx) {
        std::cerr << "Failed to load model!\n";
        return 1;
    }

    // Whisper parameters
    whisper_full_params params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    params.translate = false;       // don't translate
    params.no_context = true;       // ignore previous context
    params.single_segment = true;   // flush after each chunk

    std::cout << "Listening... Speak into your mic.\n";

    while (true) {
        std::vector<float> pcmf32;
        int n_samples = whisper_pcm_capture_chunk(&pcmf32); // capture mic chunk
        if (n_samples > 0) {
            if (whisper_full(ctx, params, pcmf32.data(), pcmf32.size()) == 0) {
                int n = whisper_full_n_segments(ctx);
                for (int i = 0; i < n; i++) {
                    std::cout << whisper_full_get_segment_text(ctx, i) << std::flush;
                }
            }
        }
    }

    whisper_free(ctx);
    return 0;
}

