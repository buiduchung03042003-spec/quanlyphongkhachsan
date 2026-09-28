import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# -----------------------------------------------------------------------------
# CONFIG & PAGE SETUP
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Hệ Thống Quản Lý Khách Sạn SmartStay",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện hiện đại
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INITIALIZE SESSION STATE (DATA DUMMY)
# -----------------------------------------------------------------------------
if 'rooms' not in st.session_state:
    st.session_state.rooms = pd.DataFrame([
        {"Số phòng": "101", "Loại phòng": "Standard Single", "Tầng": 1, "Giá/đêm (VNĐ)": 500000, "Trạng thái": "Trống"},
        {"Số phòng": "102", "Loại phòng": "Standard Double", "Tầng": 1, "Giá/đêm (VNĐ)": 750000, "Trạng thái": "Đã đặt"},
        {"Số phòng": "201", "Loại phòng": "Deluxe Sea View", "Tầng": 2, "Giá/đêm (VNĐ)": 1200000, "Trạng thái": "Trống"},
        {"Số phòng": "202", "Loại phòng": "Deluxe Sea View", "Tầng": 2, "Giá/đêm (VNĐ)": 1200000, "Trạng thái": "Bảo trì"},
        {"Số phòng": "301", "Loại phòng": "VIP Suite", "Tầng": 3, "Giá/đêm (VNĐ)": 2500000, "Trạng thái": "Đã đặt"},
    ])

if 'bookings' not in st.session_state:
    st.session_state.bookings = pd.DataFrame([
        {
            "Mã Đặt Phòng": "BK001",
            "Tên Khách Hàng": "Nguyễn Văn A",
            "Số Điện Thoại": "0901234567",
            "Số phòng": "102",
            "Ngày nhận": date(2026, 10, 1),
            "Ngày trả": date(2026, 10, 5),
            "Tổng tiền (VNĐ)": 3000000,
            "Trạng thái": "Xác nhận"
        },
        {
            "Mã Đặt Phòng": "BK002",
            "Tên Khách Hàng": "Trần Thị B",
            "Số Điện Thoại": "0987654321",
            "Số phòng": "301",
            "Ngày nhận": date(2026, 10, 2),
            "Ngày trả": date(2026, 10, 4),
            "Tổng tiền (VNĐ)": 5000000,
            "Trạng thái": "Xác nhận"
        }
    ])

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2983/2983780.png", width=70)
st.sidebar.title("SmartStay PMS")
st.sidebar.caption("Chuyên nghiệp • Tối ưu • Hiệu quả")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Danh mục quản lý",
    ["📊 Báo Cáo Tổng Quan", "🛏️ Sơ Đồ & Trạng Thái Phòng", "➕ Đặt Phòng Mới", "📋 Quản Lý Đặt Phòng", "⚙️ Cấu Hình Danh Sách Phòng"]
)

# -----------------------------------------------------------------------------
# 1. BÁO CÁO TỔNG QUAN
# -----------------------------------------------------------------------------
if menu == "📊 Báo Cáo Tổng Quan":
    st.markdown('<div class="main-header">📊 Báo Cáo Tổng Quan</div>', unsafe_allow_html=True)
    st.caption("Thống kê tình trạng kinh doanh và công suất phòng thực tế")
    
    total_rooms = len(st.session_state.rooms)
    available_rooms = len(st.session_state.rooms[st.session_state.rooms["Trạng thái"] == "Trống"])
    booked_rooms = len(st.session_state.rooms[st.session_state.rooms["Trạng thái"] == "Đã đặt"])
    maint_rooms = len(st.session_state.rooms[st.session_state.rooms["Trạng thái"] == "Bảo trì"])
    occupancy_rate = (booked_rooms / total_rooms) * 100 if total_rooms > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tổng Số Phòng", total_rooms)
    with col2:
        st.metric("Phòng Sẵn Sàng", available_rooms, delta=f"{available_rooms} phòng trống")
    with col3:
        st.metric("Phòng Đang Có Khách", booked_rooms)
    with col4:
        st.metric("Tỷ Lệ Lấp Đầy", f"{occupancy_rate:.1f}%")

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Trạng Thái Phòng Hiện Tại")
        status_counts = st.session_state.rooms["Trạng thái"].value_counts().reset_index()
        status_counts.columns = ["Trạng thái", "Số lượng"]
        fig_pie = px.pie(
            status_counts, 
            names="Trạng thái", 
            values="Số lượng", 
            hole=0.4,
            color="Trạng thái",
            color_discrete_map={"Trống": "#22C55E", "Đã đặt": "#3B82F6", "Bảo trì": "#EF4444"}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_chart2:
        st.subheader("Cơ Cấu Loại Phòng")
        type_counts = st.session_state.rooms["Loại phòng"].value_counts().reset_index()
        type_counts.columns = ["Loại phòng", "Số lượng"]
        fig_bar = px.bar(
            type_counts, 
            x="Loại phòng", 
            y="Số lượng",
            color="Loại phòng",
            text_auto=True
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# 2. SƠ ĐỒ & TRẠNG THÁI PHÒNG
# -----------------------------------------------------------------------------
elif menu == "🛏️ Sơ Đồ & Trạng Thái Phòng":
    st.markdown('<div class="main-header">🛏️ Sơ Đồ & Trạng Thái Phòng</div>', unsafe_allow_html=True)
    st.caption("Trực quan hóa danh sách phòng theo tầng")

    floors = sorted(st.session_state.rooms["Tầng"].unique())
    
    for floor in floors:
        st.subheader(f"🏢 Tầng {floor}")
        floor_rooms = st.session_state.rooms[st.session_state.rooms["Tầng"] == floor]
        
        cols = st.columns(4)
        for idx, (_, room) in enumerate(floor_rooms.iterrows()):
            col = cols[idx % 4]
            status = room["Trạng thái"]
            
            # Đổi màu card theo trạng thái
            if status == "Trống":
                color_code = "#22C55E"
                bg_color = "#F0FDF4"
            elif status == "Đã đặt":
                color_code = "#3B82F6"
                bg_color = "#EFF6FF"
            else:
                color_code = "#EF4444"
                bg_color = "#FEF2F2"

            with col:
                st.markdown(f"""
                    <div style="
                        background-color: {bg_color}; 
                        border-left: 5px solid {color_code}; 
                        padding: 12px; 
                        border-radius: 8px; 
                        margin-bottom: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    ">
                        <h4 style="margin: 0; color: #1E293B;">Phòng {room['Số phòng']}</h4>
                        <p style="margin: 4px 0; font-size: 0.85rem; color: #64748B;"><b>Loại:</b> {room['Loại phòng']}</p>
                        <p style="margin: 4px 0; font-size: 0.85rem; color: #64748B;"><b>Giá:</b> {room['Giá/đêm (VNĐ)']:,.0f} đ</p>
                        <span style="
                            background-color: {color_code}; 
                            color: white; 
                            padding: 2px 8px; 
                            border-radius: 12px; 
                            font-size: 0.75rem; 
                            font-weight: 600;
                        ">{status}</span>
                    </div>
                """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. ĐẶT PHÒNG MỚI
# -----------------------------------------------------------------------------
elif menu == "➕ Đặt Phòng Mới":
    st.markdown('<div class="main-header">➕ Tạo Đặt Phòng Mới</div>', unsafe_allow_html=True)

    available_rooms_df = st.session_state.rooms[st.session_state.rooms["Trạng thái"] == "Trống"]
    
    if available_rooms_df.empty:
        st.warning("Hiện tại không còn phòng trống nào khả dụng để đặt!")
    else:
        with st.form("booking_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            
            with col_a:
                guest_name = st.text_input("Họ tên khách hàng *", placeholder="Nhập tên đầy đủ")
                phone = st.text_input("Số điện thoại *", placeholder="Nhập số điện thoại")
                selected_room_no = st.selectbox(
                    "Chọn phòng trống *",
                    options=available_rooms_df["Số phòng"].tolist(),
                    format_func=lambda x: f"Phòng {x} - {available_rooms_df[available_rooms_df['Số phòng']==x]['Loại phòng'].values[0]} ({available_rooms_df[available_rooms_df['Số phòng']==x]['Giá/đêm (VNĐ)'].values[0]:,.0f}đ/đêm)"
                )
                
            with col_b:
                check_in = st.date_input("Ngày nhận phòng", value=datetime.today())
                check_out = st.date_input("Ngày trả phòng", value=datetime.today())
                
                room_price = available_rooms_df[available_rooms_df["Số phòng"] == selected_room_no]["Giá/đêm (VNĐ)"].values[0]
                num_nights = (check_out - check_in).days
                total_price = max(num_nights, 1) * room_price
                
                st.info(f"⏱️ **Số đêm:** {max(num_nights, 1)} đêm | 💰 **Tổng chi phí dự kiến:** {total_price:,.0f} VNĐ")

            submit_btn = st.form_submit_button("Lưu Đặt Phòng", use_container_width=True)

            if submit_btn:
                if not guest_name or not phone:
                    st.error("Vui lòng điền đầy đủ họ tên và số điện thoại khách hàng!")
                elif check_out <= check_in:
                    st.error("Ngày trả phòng phải sau ngày nhận phòng!")
                else:
                    new_id = f"BK{len(st.session_state.bookings) + 1:03d}"
                    new_booking = {
                        "Mã Đặt Phòng": new_id,
                        "Tên Khách Hàng": guest_name,
                        "Số Điện Thoại": phone,
                        "Số phòng": selected_room_no,
                        "Ngày nhận": check_in,
                        "Ngày trả": check_out,
                        "Tổng tiền (VNĐ)": total_price,
                        "Trạng thái": "Xác nhận"
                    }
                    st.session_state.bookings = pd.concat([st.session_state.bookings, pd.DataFrame([new_booking])], ignore_index=True)
                    
                    # Cập nhật trạng thái phòng thành Đã đặt
                    st.session_state.rooms.loc[st.session_state.rooms["Số phòng"] == selected_room_no, "Trạng thái"] = "Đã đặt"
                    st.success(f"Tạo phiếu đặt phòng {new_id} cho phòng {selected_room_no} thành công!")
                    st.rerun()

# -----------------------------------------------------------------------------
# 4. QUẢN LÝ ĐẶT PHÒNG
# -----------------------------------------------------------------------------
elif menu == "📋 Quản Lý Đặt Phòng":
    st.markdown('<div class="main-header">📋 Danh Sách Phiếu Đặt Phòng</div>', unsafe_allow_html=True)

    if st.session_state.bookings.empty:
        st.info("Chưa có phiếu đặt phòng nào trong hệ thống.")
    else:
        st.dataframe(
            st.session_state.bookings.style.format({"Tổng tiền (VNĐ)": "{:,.0f} VNĐ"}),
            use_container_width=True
        )

        st.subheader("Cập Nhật / Checkout Đặt Phòng")
        selected_bk = st.selectbox(
            "Chọn mã phiếu để xử lý",
            options=st.session_state.bookings["Mã Đặt Phòng"].tolist()
        )
        
        bk_data = st.session_state.bookings[st.session_state.bookings["Mã Đặt Phòng"] == selected_bk].iloc[0]
        col_act1, col_act2 = st.columns(2)
        
        with col_act1:
            if st.button("Trả Phòng (Check-out)", type="primary", use_container_width=True):
                # Đổi trạng thái phiếu đặt và phòng về Trống
                room_no = bk_data["Số phòng"]
                st.session_state.rooms.loc[st.session_state.rooms["Số phòng"] == room_no, "Trạng thái"] = "Trống"
                st.session_state.bookings.loc[st.session_state.bookings["Mã Đặt Phòng"] == selected_bk, "Trạng thái"] = "Đã trả phòng"
                st.success(f"Khách đã trả phòng {room_no} thành công!")
                st.rerun()

# -----------------------------------------------------------------------------
# 5. CẤU HÌNH DANH SÁCH PHÒNG
# -----------------------------------------------------------------------------
elif menu == "⚙️ Cấu Hình Danh Sách Phòng":
    st.markdown('<div class="main-header">⚙️ Cấu Hình & Quản Lý Phòng</div>', unsafe_allow_html=True)
    st.caption("Thêm phòng mới hoặc chỉnh sửa trực tiếp danh sách phòng hiện có")

    tab1, tab2 = st.tabs(["Chỉnh Sửa Trực Tiếp", "Thêm Phòng Mới"])

    with tab1:
        edited_rooms = st.data_editor(
            st.session_state.rooms,
            num_rows="dynamic",
            use_container_width=True,
            key="room_editor"
        )
        if st.button("Lưu Thay Đổi Cấu Hình", type="primary"):
            st.session_state.rooms = edited_rooms
            st.success("Cập nhật danh sách phòng thành công!")
            st.rerun()

    with tab2:
        with st.form("add_room_form"):
            r_number = st.text_input("Số phòng", placeholder="Ví dụ: 302")
            r_type = st.selectbox("Loại phòng", ["Standard Single", "Standard Double", "Deluxe Sea View", "VIP Suite"])
            r_floor = st.number_input("Tầng", min_value=1, max_value=20, value=1)
            r_price = st.number_input("Giá/đêm (VNĐ)", min_value=100000, step=50000, value=500000)
            
            if st.form_submit_button("Thêm Phòng"):
                if r_number in st.session_state.rooms["Số phòng"].values:
                    st.error("Số phòng này đã tồn tại trong hệ thống!")
                else:
                    new_room = {
                        "Số phòng": r_number,
                        "Loại phòng": r_type,
                        "Tầng": r_floor,
                        "Giá/đêm (VNĐ)": r_price,
                        "Trạng thái": "Trống"
                    }
                    st.session_state.rooms = pd.concat([st.session_state.rooms, pd.DataFrame([new_room])], ignore_index=True)
                    st.success(f"Thêm thành công phòng {r_number}!")
                    st.rerun()
