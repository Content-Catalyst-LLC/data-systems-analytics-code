#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/*
 * Lightweight FNV-1a fingerprint for governance registers.
 * Use SHA-256 for formal provenance, but this deterministic example is
 * portable and useful for teaching governance state fingerprints.
 */

int main(int argc, char **argv) {
    const char *path = argc > 1 ? argv[1] : "data/policy_register.csv";
    FILE *file = fopen(path, "rb");

    if (!file) {
        perror("Unable to open input file");
        return 1;
    }

    uint64_t hash = 1469598103934665603ULL;
    int byte;

    while ((byte = fgetc(file)) != EOF) {
        hash ^= (unsigned char) byte;
        hash *= 1099511628211ULL;
    }

    fclose(file);
    printf("file=%s\nfnv1a64=%llx\n", path, (unsigned long long) hash);
    return 0;
}
