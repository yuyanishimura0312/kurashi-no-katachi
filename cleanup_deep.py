#!/usr/bin/env python3
"""
academic_deep の英字濃度を下げて読みやすくするクリーンアップスクリプト
- 英文書籍タイトル『English Title』 → 削除（コンテキストに応じて言い換え）
- インライン英語著者引用（Author, X. Y. YEAR, Journal）→ 削除
- 連続英字パターンの平準化
"""
import re
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

# 処理対象ファイル
TARGETS = [
    'articles_data.py',
    'articles_batch1.py',
    'articles_batch2.py',
    'articles_batch3.py',
    'articles_batch4.py',
    'articles_batch5.py',
    'articles_batch6.py',
    'articles_batch7.py',
    'articles_batch8.py',
    'articles_batch9.py',
    'articles_batch10.py',
    'articles_batch11.py',
    'articles_batch12.py',
    'articles_batch13.py',
    'articles_batch14.py',
    'articles_batch15.py',
    'articles_batch16.py',
    'articles_batch17.py',
    'articles_batch18.py',
]

def is_mostly_english(s: str, threshold: float = 0.5) -> bool:
    if not s: return False
    eng = sum(1 for c in s if c.isascii() and c.isalpha())
    return eng / len(s) > threshold

def clean_deep_text(text: str) -> str:
    """academic_deep の英字を減らして読みやすくする"""

    # 1. 『English Title』（YYYY年, [option]）→（YYYY年）
    def replace_eng_title(m):
        title = m.group(1)
        year = m.group(2)
        if is_mostly_english(title):
            return f'（{year}年）'
        return m.group(0)
    text = re.sub(r'『([^』]+)』（(\d{4})年[^）]*）', replace_eng_title, text)

    # 2. 『English Title』 alone (no year follows) → delete
    def maybe_delete(m):
        title = m.group(1)
        if is_mostly_english(title):
            return ''
        return m.group(0)
    text = re.sub(r'『([^』]+)』', maybe_delete, text)

    # 3. インライン著者英語引用：
    #   （Smith, J. A. & Jones, B. C. 2020, Journal Name）
    #   （Smith, J. et al. 2020, Journal）
    text = re.sub(
        r'（[A-Z][a-zA-Z]+(?:[,\s]+[A-Z]\.\s*)+'  # 著者名 + initials
        r'(?:&\s*[A-Z][a-zA-Z]+(?:[,\s]+[A-Z]\.\s*)+)?'  # 共著者
        r'(?:et\s*al\.\s*)?'  # et al.
        r'\d{4}'  # 年
        r'[^）]*'  # 残り（誌名・ボリュームなど）
        r'）',
        '',
        text
    )

    # 4. 著者名と年だけのパターン：（Author, F. 2020）も削除
    text = re.sub(
        r'（[A-Z][a-zA-Z]+(?:[,\s]+[A-Z]\.\s*)+\d{4}）',
        '',
        text
    )

    # 5. 雑誌名・ジャーナル名のみのパターン：（Journal Name 2020）→ 削除
    text = re.sub(
        r'（(?:[A-Z][a-zA-Z]+\s*)+\d{4}\s*[）)]',
        '',
        text
    )

    # 6. 文末整理：。、 → 。、 、、 → 、、 など
    text = re.sub(r'、\s*、', '、', text)
    text = re.sub(r'、\s*。', '。', text)
    text = re.sub(r'。、', '。', text)
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\s+([、。])', r'\1', text)

    # 7. 「」内の英語表記を整理：「concept (concept_in_english)」→「concept」
    # 但し短い英語タームは維持（例：「サイコバイオティクス（psychobiotics）」）
    # 完全に英文字のみの「」内は削除
    def maybe_clean_quote(m):
        content = m.group(1)
        if is_mostly_english(content) and len(content) > 30:
            return ''  # 長い英文の引用を削除
        return m.group(0)
    text = re.sub(r'「([^」]+)」', maybe_clean_quote, text)

    # 8. 連続する空白を整理
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def process_file(filepath: Path) -> int:
    """ファイル内のすべての'academic_deep': '...'を処理"""
    content = filepath.read_text(encoding='utf-8')
    changes = 0

    # 'academic_deep': '...' パターンを検出（マルチライン未対応のシンプル版）
    # Python リテラル文字列なので、エスケープに注意
    def replace_deep(m):
        nonlocal changes
        prefix = m.group(1)
        quote = m.group(2)
        original = m.group(3)
        cleaned = clean_deep_text(original)
        if cleaned != original:
            changes += 1
        return f"{prefix}{quote}{cleaned}{quote}"

    # 'academic_deep':\s*'...' パターン（シングルクオート、エスケープ未考慮の単純版）
    pattern = re.compile(
        r"('academic_deep':\s*)(['\"])((?:(?!\2).)*)\2",
        re.DOTALL
    )
    new_content = pattern.sub(replace_deep, content)

    if changes > 0:
        filepath.write_text(new_content, encoding='utf-8')
    return changes


def main():
    # バックアップ
    backup_dir = ROOT / '_backup_pre_cleanup'
    backup_dir.mkdir(exist_ok=True)
    for t in TARGETS:
        src = ROOT / t
        if src.exists():
            shutil.copy(src, backup_dir / t)

    total_changes = 0
    print('=== academic_deep クリーンアップ ===')
    for t in TARGETS:
        path = ROOT / t
        if not path.exists(): continue
        n = process_file(path)
        if n > 0:
            print(f'  {t}: {n}件修正')
        total_changes += n
    print(f'\n合計: {total_changes}件修正')


if __name__ == '__main__':
    main()
