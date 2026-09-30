import streamlit as st
st.image("logo.jpg")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 Ứng dụng tính lãi tiền gửi tiết kiệm_Huong")
st.write("Tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép**.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================

# Số tiền gửi
so_tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

# Kỳ hạn
ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    max_value=240,
    value=12,
    step=1
)

# Hình thức tính lãi
loai_lai = st.selectbox(
    "📈 Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

# Hình thức lãnh lãi
hinh_thuc_lanh_lai = st.selectbox(
    "💳 Hình thức lãnh lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# Lãi suất
lai_suat = st.number_input(
    "📊 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
    elif lai_suat < 0:
        st.error("Lãi suất không hợp lệ.")
    else:

        # Chuyển lãi suất năm sang lãi suất tháng
        lai_suat_thang = lai_suat / 100 / 12

        # Số tháng
        so_thang = ky_han

        # =========================
        # LÃI ĐƠN
        # =========================
        if loai_lai == "Lãi đơn":

            # Tiền lãi toàn kỳ
            tong_tien_lai = (
                so_tien_gui
                * (lai_suat / 100)
                * (so_thang / 12)
            )

            tong_tien = so_tien_gui + tong_tien_lai

            # Tiền lãi định kỳ
            if hinh_thuc_lanh_lai == "Lãnh lãi theo tháng":
                tien_lai_dinh_ky = so_tien_gui * lai_suat_thang

            elif hinh_thuc_lanh_lai == "Lãnh lãi theo quý":
                tien_lai_dinh_ky = so_tien_gui * lai_suat_thang * 3

            else:
                tien_lai_dinh_ky = tong_tien_lai

        # =========================
        # LÃI KÉP
        # =========================
        else:

            # Số lần nhập lãi tùy theo hình thức
            if hinh_thuc_lanh_lai == "Lãnh lãi theo tháng":

                so_ky = so_thang
                lai_suat_ky = lai_suat_thang

            elif hinh_thuc_lanh_lai == "Lãnh lãi theo quý":

                so_ky = so_thang / 3
                lai_suat_ky = lai_suat / 100 / 4

            else:
                # Cuối kỳ: tính theo tháng để phản ánh lãi kép
                so_ky = so_thang
                lai_suat_ky = lai_suat_thang

            # Công thức lãi kép
            tong_tien = (
                so_tien_gui
                * (1 + lai_suat_ky) ** so_ky
            )

            tong_tien_lai = tong_tien - so_tien_gui

            # Tiền lãi của một kỳ
            if hinh_thuc_lanh_lai == "Lãnh lãi theo tháng":

                tien_lai_dinh_ky = (
                    so_tien_gui
                    * lai_suat_thang
                )

            elif hinh_thuc_lanh_lai == "Lãnh lãi theo quý":

                tien_lai_dinh_ky = (
                    so_tien_gui
                    * (1 + lai_suat / 100 / 4)
                    - so_tien_gui
                )

            else:

                tien_lai_dinh_ky = tong_tien_lai

        # =========================
        # HIỂN THỊ KẾT QUẢ
        # =========================

        st.success("✅ Tính toán thành công!")

        st.subheader("📊 KẾT QUẢ")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💵 Tiền gốc",
                dinh_dang_tien(so_tien_gui)
            )

        with col2:
            st.metric(
                "📈 Lãi suất",
                f"{lai_suat:.2f}%/năm"
            )

        st.divider()

        # Tiền lãi định kỳ
        st.info(
            f"💰 **Tiền lãi định kỳ:** "
            f"{dinh_dang_tien(tien_lai_dinh_ky)}"
        )

        # Tổng tiền lãi
        st.warning(
            f"📈 **Tổng tiền lãi:** "
            f"{dinh_dang_tien(tong_tien_lai)}"
        )

        # Tổng tiền gốc + lãi
        st.success(
            f"🏦 **Tổng tiền gốc và lãi:** "
            f"{dinh_dang_tien(tong_tien)}"
        )

        st.divider()

        # =========================
        # THÔNG TIN GỬI
        # =========================
        st.subheader("📋 Thông tin khoản tiền gửi")

        st.write(
            f"**Số tiền gửi:** {dinh_dang_tien(so_tien_gui)}"
        )

        st.write(
            f"**Kỳ hạn:** {so_thang} tháng"
        )

        st.write(
            f"**Hình thức tính:** {loai_lai}"
        )

        st.write(
            f"**Hình thức lãnh lãi:** {hinh_thuc_lanh_lai}"
        )

        st.write(
            f"**Lãi suất:** {lai_suat:.2f}%/năm"
        )
