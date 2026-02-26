#!/bin/bash -eu

# build project
python3 -m pip install -r requirements.txt
python3 -m pip install -r install_cornucopia_deps.txt

# Build fuzzers into $OUT. These could be detected in other ways.
for fuzzer in $(find "$SRC/cornucopia/tests/scripts" -name '*_fuzzer.py'); do
    fuzzer_basename=$(basename -s .py "$fuzzer")
    fuzzer_package=${fuzzer_basename}.pkg

    python3 -m PyInstaller --distpath "$OUT" --onefile --exclude IPython --paths "$SRC"/cornucopia:"$SRC"/cornucopia/scripts:"$SRC"/cornucopia/tests/test-files --hidden-import scripts --collect-submodules scripts --name "$fuzzer_package" "$fuzzer"

    echo "#!/bin/sh
# LLVMFuzzerTestOneInput for fuzzer detection.
echo "fuzzing now, this is what is here"
this_dir=\$(dirname \"\$0\")
ASAN_OPTIONS=\$ASAN_OPTIONS:symbolize=1:external_symbolizer_path=\$this_dir/llvm-symbolizer:detect_leaks=0 \
\$this_dir/$fuzzer_package \$@" > "$OUT"/"$fuzzer_basename"
    chmod +x "$OUT/$fuzzer_basename"
done
