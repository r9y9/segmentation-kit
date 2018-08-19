#!/bin/bash

set -e

dst_dir=$(python -c "from params import dst_dir;print(dst_dir)")

# 読みの推定
python a.py

# 16kHzの音声ファイルを準備
python b.py

# 音素アライメント
perl ./segment_julius.pl $dst_dir

# 失敗したテキストの数をチェック
python c.py

# JSUTのwavディレクトリと同じ階層に、labディレクトリをコピー
# ラベルは HTS style
python d.py
