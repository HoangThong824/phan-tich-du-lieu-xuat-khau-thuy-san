import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")

# ================== ĐỌC FILE ==================
file_path = "data_filtered_attributes.csv"
df = pd.read_csv(file_path)

print("Đọc file:", df.shape)
print(df.head())

# ================== CHUẨN HÓA ==================
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Value'] = pd.to_numeric(df['Value'], errors='coerce') / 1_000_000_000

# FIX HS CODE (303 → 0303)
df['HS_Code'] = df['HS_Code'].astype(str).str.zfill(4)

# FIX COUNTRY (chuẩn hóa tên)
df['Country'] = df['Country'].replace({
    'Viet Nam': 'Vietnam',
    'VN': 'Vietnam',
    'VNM': 'Vietnam',
    'IDN': 'Indonesia'
})

print("Quốc gia:", df['Country'].unique())
print("HS codes:", df['HS_Code'].unique())

# ================== LỌC ==================
df = df[
    (df['Flow'] == 'Export') &
    (df['Partner'] == 'World') &
    (df['Country'].isin(['Vietnam', 'Indonesia']))
]

print("Sau lọc:", df.shape)

# ================== THƯ MỤC LƯU ==================
output_folder = "charts"
os.makedirs(output_folder, exist_ok=True)

# ================== HÀM VẼ ==================
def plot_compare(code, title):
    temp = df[df['HS_Code'] == code]

    if temp.empty:
        print(f"Không có dữ liệu {code}")
        return

    pivot = temp.pivot_table(
        index='Year',
        columns='Country',
        values='Value',
        aggfunc='sum'
    )

    print(f"\n Dữ liệu {code}:")
    print(pivot.head())

    plt.figure(figsize=(12,6))

    if 'Vietnam' in pivot.columns:
        plt.plot(pivot.index, pivot['Vietnam'], marker='o', linewidth=2.5, label='Vietnam')

    if 'Indonesia' in pivot.columns:
        plt.plot(pivot.index, pivot['Indonesia'], marker='s', linewidth=2.5, label='Indonesia')

    plt.title(title, fontsize=14)
    plt.xlabel("Năm")
    plt.ylabel("Tỷ USD")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()

    # ================== LƯU ẢNH ==================
    file_name = f"{output_folder}/{code}_comparison.png"
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    print(f"Đã lưu: {file_name}")

    plt.show()

# ================== VẼ BIỂU ĐỒ ==================
plot_compare('0303', 'So sánh Cá đông lạnh (HS0303)')
plot_compare('0304', 'So sánh Cá phi lê (HS0304)')
plot_compare('0306', 'So sánh Tôm & giáp xác (HS0306)')

print("\n KIỂM TRA THƯ MỤC 'charts'")