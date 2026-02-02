import streamlit as st
import math

# 1. ฟังก์ชันสำหรับแสดงหน้าต่างสรุปผล (Pop-up)
@st.dialog("ใบสรุปรายการประมาณการ")
def show_summary_dialog(final_billed, selected_items):
    st.write("### รายการอุปกรณ์และบริการ:")
    if selected_items:
        for item in selected_items:
            # แสดงเฉพาะชื่อและจำนวนตามที่ตกลงกันไว้
            st.write(f"✅ {item['name']} จำนวน {item['qty']} รายการ")
    else:
        st.write("ยังไม่ได้เลือกรายการอุปกรณ์")
    
    st.divider()
    # แสดงราคาสุทธิที่ปัดเศษแล้ว
    st.info(f"## ราคาที่เสนอผู้ใช้ไฟ: {final_billed:,.0f} บาท")
    st.write("*(ราคานี้รวมค่าแรง ค่าปลดสับ และอุปกรณ์เรียบร้อยแล้ว)*")

def main():
    st.set_page_config(page_title="ระบบคำนวณค่าบริการ", layout="wide")
    
    # เปลี่ยนชื่อหัวข้อหลักตามที่คุณต้องการ
    st.title("ประมาณการติดตั้งอุปกรณ์ป้องกันและบำรุงรักษาหม้อแปลง")
    st.divider()

    # --- ส่วนที่ 1: ค่าแรงพนักงาน ---
    st.header("ค่าแรงพนักงาน")
    staff_data = [
        {"level": "พชง.3", "rate": 87.77},
        {"level": "พชง.4", "rate": 103.48},
        {"level": "พชง.5", "rate": 125.30},
        {"level": "พชง.6", "rate": 164.19},
    ]
    total_wage = 0
    cols_h = st.columns([2, 2, 2, 2, 2])
    cols_h[0].write("**ระดับ**"); cols_h[1].write("**ราคา/ชม**")
    cols_h[2].write("**ชั่วโมง**"); cols_h[3].write("**จำนวนคน**"); cols_h[4].write("**รวม**")

    for s in staff_data:
        c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 2])
        c1.text(s["level"])
        c2.text(f"{s['rate']:.2f}")
        hr = c3.number_input("ชม", value=1, key=f"h_{s['level']}", label_visibility="collapsed")
        qty = c4.number_input("คน", value=0, key=f"q_{s['level']}", label_visibility="collapsed")
        row_w = s['rate'] * hr * qty
        total_wage += row_w
        c5.text(f"{row_w:,.2f}")

    st.divider()

    # --- ส่วนที่ 2: ค่าปลดสับ (ล็อคราคา) ---
    st.header("ค่าปลดสับ")
    cs1, cs2, cs3 = st.columns([4, 4, 2])
    # ล็อคราคาต่อครั้งที่ 570
    cs1.number_input("ราคาต่อครั้ง", value=570.0, disabled=True) 
    s_qty = cs2.number_input("จำนวนครั้ง", value=0)
    total_switch = 570.0 * s_qty
    cs3.metric("รวมค่าปลดสับ", f"{total_switch:,.2f}")
    
    st.divider()

    # --- ส่วนที่ 3: รายการอุปกรณ์และบำรุงรักษา (ล็อคราคาหน่วย) ---
    st.header("รายการอุปกรณ์และบริการ")
    items_list = [
        {"name": "Bird Spikes", "price": 325.0},
        {"name": "LIGHTNING ARRESTER COVERS", "price": 110.0},
        {"name": "DROPOUT FUSE CUTOUT COVERS", "price": 670.0},
        {"name": "TRANSFORMER BUSHING COVERS", "price": 294.0},
        {"name": "บำรุงรักษาหม้อแปลง ไม่เกิน 250(kVA)", "price": 3000.0},
        {"name": "บำรุงรักษาหม้อแปลง 250(kVA)-1,500(kVA)", "price": 7000.0},
        {"name": "บำรุงรักษาหม้อแปลง มากกว่า 1,500(kVA)", "price": 9000.0}
    ]
    total_items = 0
    selected_items = []
    
    ih = st.columns([4, 2, 2, 2])
    ih[0].write("**รายการ**"); ih[1].write("**ราคา/หน่วย**")
    ih[2].write("**จำนวน**"); ih[3].write("**รวม**")

    for i, item in enumerate(items_list):
        ic1, ic2, ic3, ic4 = st.columns([4, 2, 2, 2])
        ic1.text(item["name"]) 
        # ล็อคราคาหน่วยไม่ให้แก้ไข
        ic2.number_input("ราคา", value=item["price"], key=f"p_{i}", disabled=True, label_visibility="collapsed")
        q = ic3.number_input("จำนวน", value=0, key=f"qty_{i}", label_visibility="collapsed")
        
        row_p = item["price"] * q
        total_items += row_p
        ic4.text(f"{row_p:,.2f}")
        
        if q > 0:
            selected_items.append({"name": item["name"], "qty": q})

    st.divider()

    # --- ส่วนที่ 4: สรุปงบประมาณ ---
    raw_total = total_wage + total_switch + total_items
    # ปัดเศษขึ้นหลักร้อยอัตโนมัติ
    final_billed = math.ceil(raw_total / 100) * 100 if raw_total > 0 else 0
    
    st.subheader("📊 สรุปงบประมาณ")
    st.write(f"ราคารวมคำนวณจริง: {raw_total:,.2f} บาท")
    st.info(f"### ราคาที่เสนอผู้ใช้ไฟ: {final_billed:,.0f} บาท")

    # --- ปุ่มกดสำหรับเปิดหน้าต่างใหม่ (Pop-up) ---
    st.write("")
    if st.button("📱 แสดงหน้าสรุปสำหรับแจ้งลูกค้า (แคปหน้าจอ)", type="primary", use_container_width=True):
        show_summary_dialog(final_billed, selected_items)

if __name__ == "__main__":
    main()