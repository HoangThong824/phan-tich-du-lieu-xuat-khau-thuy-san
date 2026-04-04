import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# ĐỌC DỮ LIỆU
# =========================================================
file_name = 'data.xlsx'

try:
    if file_name.endswith('.csv'):
        df = pd.read_csv(file_name)
    else:
        df = pd.read_excel(file_name)
    print("Đọc dữ liệu thành công")
except Exception as e:
    print(f"Lỗi: {e}")
    exit()

# =========================================================
# XỬ LÝ SỐ LIỆU
# =========================================================
df['Export_Billion'] = df['Export_Seafood_HS03'] / 1e9
df['Share_Percentage'] = (df['Export_Seafood_HS03'] / df['Total_Export']) * 100

# Thiết lập giao diện chung
sns.set_theme(style="whitegrid", font_scale=1.2)
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'Tahoma'] 
colors = {'Việt Nam': '#E31A1C', 'Indonesia': '#1F78B4'}

# Hàm hỗ trợ lưu ảnh 
def save_chart(filename):
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Đã lưu: {filename}")
    plt.show()

# =========================================================
# XUẤT BIỂU ĐỒ
# =========================================================

# --- BIỂU ĐỒ 1: KIM NGẠCH (QUY MÔ) ---
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='Year', y='Export_Billion', hue='Country', palette=colors)
plt.title('KIM NGẠCH XUẤT KHẨU THỦY SẢN (TỶ USD)', fontweight='bold')
plt.ylabel('Giá trị (Tỷ USD)')
plt.xlabel('Năm')
plt.xticks(rotation=45)
save_chart('1_kim_ngach_xuat_khau.png')

# --- BIỂU ĐỒ 2: TỶ TRỌNG (%) ---
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Year', y='Share_Percentage', hue='Country', palette=colors, 
             linewidth=3, marker='o', markersize=8)
plt.title('TỶ TRỌNG THỦY SẢN TRONG TỔNG XUẤT KHẨU (%)', fontweight='bold')
plt.ylabel('Tỷ trọng (%)')
plt.xlabel('Năm')
plt.xticks(df['Year'].unique(), rotation=45)
save_chart('2_ty_trong_xuat_khau.png')

# --- BIỂU ĐỒ 3: CHỈ SỐ RCA ---
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Year', y='RCA', hue='Country', palette=colors, 
             linewidth=3, marker='D', markersize=8)
plt.axhline(1, color='black', linestyle='--', alpha=0.7, label='Ngưỡng RCA = 1')
plt.title('CHỈ SỐ LỢI THẾ SO SÁNH LỘ DIỆN (RCA)', fontweight='bold')
plt.ylabel('Chỉ số RCA')
plt.xlabel('Năm')
plt.xticks(df['Year'].unique(), rotation=45)
plt.legend()
save_chart('3_chi_so_RCA.png')

# --- BIỂU ĐỒ 4: CHỈ SỐ RSCA ---
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Year', y='RSCA', hue='Country', palette=colors, 
             linewidth=3, marker='s', markersize=8)
plt.axhline(0, color='black', linestyle='--', alpha=0.7, label='Điểm cân bằng (0)')
plt.title('CHỈ SỐ LỢI THẾ ĐỐI XỨNG (RSCA)', fontweight='bold')
plt.ylabel('Chỉ số RSCA')
plt.xlabel('Năm')
plt.ylim(-1, 1)
plt.xticks(df['Year'].unique(), rotation=45)
plt.legend()
save_chart('4_chi_so_RSCA.png')