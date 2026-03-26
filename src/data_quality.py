import pandas as pd
import os


def check_data_quality():
    # --- 1. 自动导航：定位项目根目录 ---
    current_file = os.path.abspath(__file__)
    src_dir = os.path.dirname(current_file)
    project_root = os.path.dirname(src_dir)

    # 路径拼接
    raw_path = os.path.join(project_root, 'data', 'raw', 'lens-llm-agents-raw.csv')

    print(f"🚀 正在重新运行质检程序...")
    print(f"📍 目标文件: {raw_path}\n")

    if not os.path.exists(raw_path):
        print(f"❌ 找不到文件！请确认文件是否在 data/raw 文件夹下。")
        return

    # --- 2. 读取并清洗数据 ---
    try:
        # 读取数据
        df = pd.read_csv(raw_path)
        # 去掉列名空格（Lens 导出有时会有不可见空格）
        df.columns = df.columns.str.strip()
        total = len(df)

        # 基于 DOI 和 Title 去重
        df_cleaned = df.copy()
        if 'DOI' in df.columns:
            df_cleaned = df_cleaned.drop_duplicates(subset=['DOI'])
        if 'Title' in df.columns:
            df_cleaned = df_cleaned.drop_duplicates(subset=['Title'])

        cleaned_total = len(df_cleaned)

        # --- 3. 打印完美的质检报告 ---
        # 修正了作者列名为 'Author/s'
        check_fields = ['Title', 'Author/s', 'Abstract', 'References', 'DOI']

        print("=" * 40)
        print("📋 大模型智能体文献质量自检报告 (Final)")
        print("=" * 40)
        print(f"原始记录总数: {total}")
        print(f"去重后记录数: {cleaned_total}")
        print(f"重复记录比例: {((total - cleaned_total) / total) * 100:.2f}%")
        print("-" * 40)
        print("关键字段缺失率统计:")

        for field in check_fields:
            if field in df_cleaned.columns:
                missing = df_cleaned[field].isna().sum()
                print(f" - {field:15}: {(missing / cleaned_total) * 100:>6.2f}%")
            else:
                # 备选方案：如果找不到 Author/s，尝试找 Authors
                print(f" - {field:15}: ⚠️ 列名不匹配 (请检查 CSV 表头)")

        # --- 4. 重新保存清洗后的数据 ---
        processed_dir = os.path.join(project_root, 'data', 'processed')
        os.makedirs(processed_dir, exist_ok=True)
        output_file = os.path.join(processed_dir, 'cleaned_data.csv')

        df_cleaned.to_csv(output_file, index=False)
        print("=" * 40)
        print(f"✅ 洁净数据已重新生成并存至:\n{output_file}")

    except Exception as e:
        print(f"❌ 运行出错了: {e}")


if __name__ == "__main__":
    check_data_quality()