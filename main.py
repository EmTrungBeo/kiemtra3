"""
Chương trình Quản lý Thống kê Sinh viên Lớp học & Trực quan hóa Biểu đồ
Môi trường ảo Anaconda: kiemtra
Máy chủ Web chạy trên cổng: 5175
"""

import sys
import os
import io
import base64
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Cấu hình UTF-8 cho console Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Sử dụng backend Agg cho môi trường web server để đảm bảo an toàn luồng
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Cấu hình font chữ hỗ trợ tiếng Việt có dấu trong Matplotlib trên Windows
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Tahoma', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = Path(__file__).resolve().parent
IMG_PATH = BASE_DIR / 'bieu_do_sinh_vien.png'

# Bảng màu sắc hiện đại cho các phân loại
PALETTE_GENDER = ['#3b82f6', '#f43f5e']  # Xanh lam Nam, Hồng đỏ Nữ
PALETTE_GRADES = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ef4444']  # Xuất sắc, Giỏi, Khá, TB, Yếu
PALETTE_GROUPS = ['#06b6d4', '#8b5cf6', '#ec4899', '#f97316', '#10b981', '#6366f1']
PALETTE_SCORES = ['#6366f1', '#a855f7']


def ve_bieu_do_cot(ax, labels: List[str], values: List[int], colors: List[str], tong_sv: int, title: str):
    """Vẽ biểu đồ cột đứng hiện đại."""
    x = np.arange(len(labels))
    width = 0.48 if len(labels) <= 3 else 0.55
    bars = ax.bar(x, values, color=colors[:len(labels)], width=width, edgecolor='#ffffff', linewidth=1.2, zorder=3)

    # Hiển thị số lượng và % trên đầu mỗi cột
    for bar in bars:
        height = bar.get_height()
        pct = (height / tong_sv * 100) if tong_sv > 0 else 0
        ax.annotate(
            f'{int(height)} SV\n({pct:.1f}%)',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 6),
            textcoords="offset points",
            ha='center',
            va='bottom',
            fontsize=10.5,
            fontweight='bold',
            color='#1e293b'
        )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11, fontweight='600', color='#334155')
    max_val = max(values) if values else 0
    ax.set_ylim(0, max(max_val * 1.28, 5))
    ax.set_ylabel('Số lượng sinh viên', fontsize=11, fontweight='bold', labelpad=10, color='#334155')
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#cbd5e1', zorder=0)


def ve_bieu_do_tron(ax, labels: List[str], values: List[int], colors: List[str], tong_sv: int):
    """Vẽ biểu đồ tròn (Donut Chart) sang trọng."""
    if tong_sv == 0:
        ax.text(0.5, 0.5, "Chưa có dữ liệu sinh viên", ha='center', va='center', fontsize=14, color='#64748b')
        ax.axis('off')
        return

    # Lọc các mục có giá trị > 0
    filtered_labels = []
    filtered_vals = []
    filtered_colors = []
    for lb, val, col in zip(labels, values, colors):
        if val > 0:
            filtered_labels.append(f"{lb} ({val} SV)")
            filtered_vals.append(val)
            filtered_colors.append(col)

    wedges, texts, autotexts = ax.pie(
        filtered_vals,
        labels=filtered_labels,
        colors=filtered_colors,
        autopct='%1.1f%%',
        startangle=140,
        pctdistance=0.78,
        wedgeprops=dict(width=0.45, edgecolor='#ffffff', linewidth=2),
        textprops=dict(fontsize=10.5, color='#1e293b', fontweight='600')
    )

    for autotext in autotexts:
        autotext.set_color('#ffffff')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)

    # Thêm vòng tròn giữa để tạo Donut Chart
    centre_circle = plt.Circle((0, 0), 0.55, fc='white')
    ax.add_artist(centre_circle)
    ax.text(0, 0, f"Tổng số\n{tong_sv} SV", ha='center', va='center', fontsize=13, fontweight='bold', color='#0f172a')


def tao_bieu_do_chung(
    ten_lop: str,
    labels: List[str],
    values: List[int],
    colors: List[str],
    chart_type: str = 'bar',
    tieu_de_phu: str = '',
    luu_anh: bool = True
) -> Tuple[bytes, str]:
    """
    Hàm tạo biểu đồ linh hoạt theo loại (bar / pie) và lưu ra file bieu_do_sinh_vien.png.
    """
    tong_sv = sum(values)
    fig, ax = plt.subplots(figsize=(8, 5.8), dpi=140)

    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')

    title_text = f"THỐNG KÊ SINH VIÊN - {ten_lop.upper()}"
    if tieu_de_phu:
        title_text += f"\n({tieu_de_phu} • Tổng: {tong_sv} sinh viên)"
    else:
        title_text += f"\n(Tổng cộng: {tong_sv} sinh viên)"

    ax.set_title(title_text, fontsize=13.5, fontweight='bold', pad=18, color='#0f172a')

    if chart_type == 'pie':
        ve_bieu_do_tron(ax, labels, values, colors, tong_sv)
    else:
        ve_bieu_do_cot(ax, labels, values, colors, tong_sv, title_text)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#94a3b8')
        ax.spines['bottom'].set_color('#94a3b8')

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=160, bbox_inches='tight')
    buf.seek(0)
    image_bytes = buf.getvalue()

    if luu_anh:
        fig.savefig(IMG_PATH, dpi=300, bbox_inches='tight')

    plt.close(fig)

    image_base64 = "data:image/png;base64," + base64.b64encode(image_bytes).decode('utf-8')
    return image_bytes, image_base64


def xu_ly_du_lieu(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Phân tích payload và vẽ biểu đồ phù hợp."""
    che_do = payload.get('mode', 'gender')
    ten_lop = payload.get('ten_lop', 'Lớp 12A1').strip() or 'Lớp Học'
    chart_type = payload.get('chart_type', 'bar')

    if che_do == 'grade':
        # Thống kê theo học lực
        labels = ['Xuất sắc', 'Giỏi', 'Khá', 'Trung bình', 'Yếu']
        values = [
            max(0, int(payload.get('xuat_sac', 6))),
            max(0, int(payload.get('gioi', 14))),
            max(0, int(payload.get('kha', 16))),
            max(0, int(payload.get('trung_binh', 5))),
            max(0, int(payload.get('yeu', 2))),
        ]
        colors = PALETTE_GRADES
        sub_title = "Phân loại theo kết quả Học lực"

    elif che_do == 'group':
        # Thống kê theo tổ / nhóm
        raw_groups = payload.get('groups', [])
        if not raw_groups:
            raw_groups = [
                {'name': 'Tổ 1', 'count': 11},
                {'name': 'Tổ 2', 'count': 12},
                {'name': 'Tổ 3', 'count': 10},
                {'name': 'Tổ 4', 'count': 10},
            ]
        labels = [g.get('name', f'Tổ {i+1}') for i, g in enumerate(raw_groups)]
        values = [max(0, int(g.get('count', 0))) for g in raw_groups]
        colors = (PALETTE_GROUPS * 3)[:len(labels)]
        sub_title = "Phân chia theo Tổ / Nhóm học tập"

    elif che_do == 'scores':
        # Thống kê theo phổ điểm
        raw_scores_str = str(payload.get('scores_text', '8, 9, 7.5, 6, 8.5, 9, 10, 5, 7, 8, 9, 6.5, 7.5, 8, 4, 9.5'))
        # Parse danh sách điểm
        scores = []
        for part in raw_scores_str.replace(';', ',').split(','):
            part = part.strip()
            if part:
                try:
                    sc = float(part)
                    if 0 <= sc <= 10:
                        scores.append(sc)
                except ValueError:
                    pass

        if not scores:
            scores = [8.0, 7.5, 9.0, 6.5, 8.0, 9.5, 5.0, 7.0]

        # Chia dải điểm: [0-4], [4-6.5], [6.5-8], [8-9], [9-10]
        labels = ['< 5.0 (Yếu)', '5.0 - 6.4 (TB)', '6.5 - 7.9 (Khá)', '8.0 - 8.9 (Giỏi)', '9.0 - 10 (Xuất sắc)']
        c_yeu = sum(1 for s in scores if s < 5.0)
        c_tb = sum(1 for s in scores if 5.0 <= s < 6.5)
        c_kha = sum(1 for s in scores if 6.5 <= s < 8.0)
        c_gioi = sum(1 for s in scores if 8.0 <= s < 9.0)
        c_xs = sum(1 for s in scores if 9.0 <= s <= 10.0)

        values = [c_yeu, c_tb, c_kha, c_gioi, c_xs]
        colors = ['#ef4444', '#f59e0b', '#3b82f6', '#6366f1', '#10b981']
        avg_score = round(float(np.mean(scores)), 2)
        min_score = min(scores)
        max_score = max(scores)
        sub_title = f"Phổ điểm kiểm tra (ĐTB: {avg_score} • Cao: {max_score} • Thấp: {min_score})"

    else:
        # Mặc định: Giới tính Nam - Nữ
        nam = max(0, int(payload.get('nam', 25)))
        nu = max(0, int(payload.get('nu', 18)))
        labels = ['Nam', 'Nữ']
        values = [nam, nu]
        colors = PALETTE_GENDER
        sub_title = "Phân bố Giới tính (Nam - Nữ)"

    tong_sv = sum(values)
    items_stat = []
    for lb, val in zip(labels, values):
        pct = round((val / tong_sv * 100), 1) if tong_sv > 0 else 0
        items_stat.append({
            'label': lb,
            'count': val,
            'pct': pct
        })

    _, img_b64 = tao_bieu_do_chung(
        ten_lop=ten_lop,
        labels=labels,
        values=values,
        colors=colors,
        chart_type=chart_type,
        tieu_de_phu=sub_title,
        luu_anh=True
    )

    danh_gia = tinh_danh_gia_lop(che_do, items_stat, tong_sv, payload)

    return {
        'ten_lop': ten_lop,
        'mode': che_do,
        'chart_type': chart_type,
        'tong_sv': tong_sv,
        'items': items_stat,
        'evaluation': danh_gia,
        'image_base64': img_b64,
        'saved_file': 'bieu_do_sinh_vien.png'
    }


def tinh_danh_gia_lop(che_do: str, items: List[Dict[str, Any]], tong_sv: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tính năng mới: Đánh giá lớp học thông minh và đưa ra nhận xét sư phạm tự động.
    """
    if tong_sv == 0:
        return {
            'tieu_de': 'Đánh giá lớp học',
            'chi_so_chinh': '0%',
            'ten_chi_so': 'Chưa có sinh viên',
            'trang_thai': 'warning',
            'nhan_xet': 'Lớp học hiện chưa có dữ liệu sinh viên để đánh giá.'
        }

    if che_do == 'grade':
        # Thống kê theo học lực: Xuất sắc, Giỏi, Khá, TB, Yếu
        counts = {it['label']: it['count'] for it in items}
        kha_gioi = counts.get('Xuất sắc', 0) + counts.get('Giỏi', 0) + counts.get('Khá', 0)
        ty_le_dat = round((kha_gioi / tong_sv * 100), 1)
        yeu = counts.get('Yếu', 0)

        if ty_le_dat >= 80 and yeu == 0:
            trang_thai = 'excellent'
            nhan_xet = f"Chất lượng học tập xuất sắc! Có {ty_le_dat}% sinh viên đạt loại Khá - Giỏi trở lên, không có sinh viên yếu kém."
        elif ty_le_dat >= 65:
            trang_thai = 'good'
            nhan_xet = f"Mặt bằng học lực tốt ({ty_le_dat}% Khá - Giỏi). Cần quan tâm thêm {counts.get('Trung bình', 0) + yeu} sinh viên mức TB/Yếu."
        else:
            trang_thai = 'warning'
            nhan_xet = f"Tỷ lệ Khá - Giỏi đạt {ty_le_dat}%. Lớp cần tăng cường các buổi phụ đạo và hỗ trợ nhóm học tập."

        return {
            'tieu_de': 'Chất Lượng Học Lực',
            'chi_so_chinh': f'{ty_le_dat}%',
            'ten_chi_so': 'Tỷ lệ Khá - Giỏi trở lên',
            'trang_thai': trang_thai,
            'nhan_xet': nhan_xet
        }

    elif che_do == 'group':
        counts = [it['count'] for it in items if it['count'] > 0]
        avg_c = round(tong_sv / len(items), 1) if items else 0
        if counts:
            max_c = max(counts)
            min_c = min(counts)
            diff = max_c - min_c
            if diff <= 2:
                trang_thai = 'excellent'
                nhan_xet = f"Phân bổ sĩ số giữa các tổ rất đồng đều (chênh lệch chỉ {diff} SV, TB ~{avg_c} SV/tổ)."
            elif diff <= 5:
                trang_thai = 'good'
                nhan_xet = f"Sĩ số các tổ tương đối hợp lý (chênh lệch {diff} SV giữa tổ đông nhất và ít nhất)."
            else:
                trang_thai = 'warning'
                nhan_xet = f"Chênh lệch sĩ số giữa các tổ khá lớn ({diff} SV). Nên cân đối lại số lượng để hoạt động nhóm hiệu quả hơn."
        else:
            trang_thai = 'warning'
            nhan_xet = "Chưa có dữ liệu thành viên trong các tổ."

        return {
            'tieu_de': 'Độ Đồng Đều Các Tổ',
            'chi_so_chinh': f'{len(items)} Tổ',
            'ten_chi_so': f'TB ~{avg_c} SV/tổ',
            'trang_thai': trang_thai,
            'nhan_xet': nhan_xet
        }

    elif che_do == 'scores':
        counts = {it['label']: it['count'] for it in items}
        yeu = counts.get('< 5.0 (Yếu)', 0)
        tren_tb = tong_sv - yeu
        ty_le_pass = round((tren_tb / tong_sv * 100), 1)
        xs_gioi = counts.get('9.0 - 10 (Xuất sắc)', 0) + counts.get('8.0 - 8.9 (Giỏi)', 0)
        ty_le_xs_gioi = round((xs_gioi / tong_sv * 100), 1)

        if ty_le_pass >= 90 and ty_le_xs_gioi >= 50:
            trang_thai = 'excellent'
            nhan_xet = f"Kết quả bài kiểm tra rất cao: {ty_le_pass}% đạt yêu cầu (≥ 5.0), trong đó {ty_le_xs_gioi}% đạt điểm Giỏi & Xuất sắc."
        elif ty_le_pass >= 75:
            trang_thai = 'good'
            nhan_xet = f"Tỷ lệ bài thi đạt yêu cầu là {ty_le_pass}%. Còn {yeu} bài kiểm tra dưới trung bình cần ôn tập bổ sung kiến thức."
        else:
            trang_thai = 'warning'
            nhan_xet = f"Tỷ lệ đạt chỉ {ty_le_pass}%, có {yeu} bài kiểm tra dưới 5.0. Đề xuất tổ chức kiểm tra lại hoặc chữa bài chi tiết."

        return {
            'tieu_de': 'Tỷ Lệ Đạt Điểm Kiểm Tra',
            'chi_so_chinh': f'{ty_le_pass}%',
            'ten_chi_so': 'Bài kiểm tra ≥ 5.0',
            'trang_thai': trang_thai,
            'nhan_xet': nhan_xet
        }

    else:
        # Giới tính: Nam - Nữ
        counts = {it['label']: it['count'] for it in items}
        nam = counts.get('Nam', 0)
        nu = counts.get('Nữ', 0)
        diff_pct = abs(round((nam - nu) / tong_sv * 100, 1))

        if diff_pct <= 15:
            trang_thai = 'excellent'
            nhan_xet = f"Tỷ lệ giới tính rất cân bằng ({nam} Nam / {nu} Nữ, chênh lệch chỉ {diff_pct}%)."
        elif diff_pct <= 40:
            trang_thai = 'good'
            nhan_xet = f"Cơ cấu giới tính: {nam} Nam - {nu} Nữ (chênh lệch {diff_pct}%). Phù hợp cho các hoạt động phong trào và học tập."
        else:
            trang_thai = 'good'
            nhom_dong = "Nam" if nam > nu else "Nữ"
            nhan_xet = f"Lớp có cơ cấu thiên về sinh viên {nhom_dong} ({max(nam, nu)}/{tong_sv} SV, chiếm {max(round(nam/tong_sv*100,1), round(nu/tong_sv*100,1))}%)."

        ti_le_str = f"{round(nam/tong_sv*100, 1)}% : {round(nu/tong_sv*100, 1)}%" if tong_sv > 0 else "0 : 0"
        return {
            'tieu_de': 'Cân Bằng Giới Tính',
            'chi_so_chinh': ti_le_str,
            'ten_chi_so': 'Tỷ lệ Nam : Nữ',
            'trang_thai': trang_thai,
            'nhan_xet': nhan_xet
        }


def nhap_so_nguyen(thong_bao: str, min_val: int = 0) -> int:
    """Nhập số nguyên an toàn từ bàn phím."""
    while True:
        try:
            val = int(input(thong_bao))
            if val < min_val:
                print(f">> Giá trị phải >= {min_val}. Vui lòng nhập lại!")
                continue
            return val
        except ValueError:
            print(">> Lỗi: Vui lòng nhập một số nguyên hợp lệ!")


def chay_che_do_cli():
    """Chế độ dòng lệnh Console CLI."""
    print("=" * 60)
    print("   CHƯƠNG TRÌNH NHẬP SỐ SINH VIÊN & XUẤT BIỂU ĐỒ (CLI)")
    print("=" * 60)

    ten_lop = input("Nhập tên lớp học (VD: Lớp 12A1): ").strip() or "Lớp 12A1"
    print("\nChọn chế độ thống kê:")
    print("  1. Thống kê Nam / Nữ")
    print("  2. Thống kê theo Học lực (Xuất sắc, Giỏi, Khá, TB, Yếu)")
    chon = input("Lựa chọn (1 hoặc 2, mặc định 1): ").strip()

    if chon == '2':
        xs = nhap_so_nguyen("- Số sinh viên Xuất sắc: ")
        gioi = nhap_so_nguyen("- Số sinh viên Giỏi     : ")
        kha = nhap_so_nguyen("- Số sinh viên Khá      : ")
        tb = nhap_so_nguyen("- Số sinh viên TB       : ")
        yeu = nhap_so_nguyen("- Số sinh viên Yếu      : ")
        payload = {
            'mode': 'grade',
            'ten_lop': ten_lop,
            'chart_type': 'bar',
            'xuat_sac': xs,
            'gioi': gioi,
            'kha': kha,
            'trung_binh': tb,
            'yeu': yeu
        }
    else:
        nam = nhap_so_nguyen("- Số sinh viên Nam: ")
        nu = nhap_so_nguyen("- Số sinh viên Nữ : ")
        payload = {
            'mode': 'gender',
            'ten_lop': ten_lop,
            'chart_type': 'bar',
            'nam': nam,
            'nu': nu
        }

    res = xu_ly_du_lieu(payload)
    print("\n" + "-" * 40)
    print(f"KẾT QUẢ THỐNG KÊ - {res['ten_lop'].upper()}")
    print(f"Tổng sĩ số lớp: {res['tong_sv']} sinh viên")
    for item in res['items']:
        print(f"  • {item['label']:<15}: {item['count']:>3} SV ({item['pct']:>5.1f}%)")
    print("-" * 40)
    print(f"[OK] Đã xuất và lưu biểu đồ vào tệp: {IMG_PATH}")


def tao_web_app():
    """Khởi tạo ứng dụng Flask."""
    from flask import Flask, render_template, request, jsonify, send_file

    app = Flask(__name__, template_folder=str(BASE_DIR / 'templates'))

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/chart', methods=['GET', 'POST'])
    def api_chart():
        if request.method == 'POST':
            data = request.get_json(silent=True) or {}
        else:
            data = request.args.to_dict()

        result = xu_ly_du_lieu(data)
        return jsonify(result)

    @app.route('/api/image')
    def api_image():
        if not IMG_PATH.exists():
            xu_ly_du_lieu({'mode': 'gender', 'nam': 25, 'nu': 18, 'ten_lop': 'Lớp 12A1'})
        return send_file(str(IMG_PATH), mimetype='image/png')

    @app.route('/download')
    def download_file():
        if not IMG_PATH.exists():
            xu_ly_du_lieu({'mode': 'gender', 'nam': 25, 'nu': 18, 'ten_lop': 'Lớp 12A1'})
        return send_file(str(IMG_PATH), as_attachment=True, download_name='bieu_do_sinh_vien.png')

    return app


def main():
    parser = argparse.ArgumentParser(description="Chương trình Thống kê Sinh viên & Vẽ Biểu đồ")
    parser.add_argument('--cli', action='store_true', help="Chạy ở chế độ dòng lệnh Console")
    parser.add_argument('--port', type=int, default=5175, help="Cổng chạy Web App (mặc định: 5175)")
    parser.add_argument('--host', type=str, default="0.0.0.0", help="Địa chỉ host (mặc định: 0.0.0.0)")
    args = parser.parse_args()

    if args.cli:
        chay_che_do_cli()
    else:
        # Tạo biểu đồ ban đầu
        xu_ly_du_lieu({'mode': 'gender', 'nam': 25, 'nu': 18, 'ten_lop': 'Lớp 12A1'})

        app = tao_web_app()
        port = args.port
        host = args.host
        print("=" * 68)
        print("   CHƯƠNG TRÌNH THỐNG KÊ SINH VIÊN LỚP HỌC & XUẤT BIỂU ĐỒ")
        print("=" * 68)
        print(f"🐍 Môi trường ảo Conda : kiemtra")
        print(f"🌐 Máy chủ Web chạy tại : http://localhost:{port}")
        print(f"   (Mạng nội bộ         : http://{host}:{port})")
        print("   Nhấn Ctrl+C để dừng máy chủ")
        print("=" * 68)
        app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    main()
