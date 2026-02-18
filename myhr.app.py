import streamlit as st
import pandas as pd
import os
from datetime import date

# --- Configuration ---
st.set_page_config(
    page_title="MYHR Portal",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed" # Starts collapsed, expands after login
)

# --- Custom CSS for Blue & White Theme ---
st.markdown("""
<style>
    /* Main background color */
    .stApp {
        background-color: #f4f7f9;
    }
    
    /* Sidebar color */
    [data-testid="stSidebar"] {
        background-color: #003366;
        color: white;
    }
    
    /* Sidebar text color */
    [data-testid="stSidebar"] * {
        color: white;
    }
    
    /* Titles and Headers */
    h1, h2, h3 {
        color: #003366;
    }
    
    /* Metrics box styling */
    div[data-testid="stMetricValue"] {
        color: #0066cc;
    }
    
    /* Buttons */
    div.stButton > button:first-child {
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
# Tracks if the user is logged in and their role
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None

# --- Login Function ---
def login():
    st.title("🏢 MYHR Portal Login")
    st.markdown("---")
    
    with st.form("login_form"):
        st.subheader("Sign In")
        username = st.text_input("Username", placeholder="Enter username (emp/admin)")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submit = st.form_submit_button("Login")
        
        if submit:
            # --- MOCK AUTHENTICATION LOGIC ---
            # Replace with database verification in production
            if username == "emp" and password == "emp123":
                st.session_state['logged_in'] = True
                st.session_state['role'] = "employee"
                st.rerun() # Refresh to show dashboard
            elif username == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.session_state['role'] = "admin"
                st.rerun()
            else:
                st.error("Invalid username or password")

# --- Logout Function ---
def logout():
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.rerun()

# ==========================================
# --- Main Application Logic ---
# ==========================================
if not st.session_state['logged_in']:
    login()
else:
    # --- Sidebar Navigation ---
    st.sidebar.title("MYHR Control Menu")
    st.sidebar.write(f"Logged in as: **{st.session_state['role'].capitalize()}**")
    st.sidebar.markdown("---")
    
    # Dynamic navigation based on role
    if st.session_state['role'] == "admin":
        pages = ["Admin Dashboard", "Manage Employees", "Payroll Processing"]
    else:
        pages = ["Dashboard", "Employee Details", "Payslips", "Leave Application"]
        
    page = st.sidebar.radio("Navigation", pages)
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        logout()

    # ==========================================
    # --- EMPLOYEE PAGES ---
    # ==========================================
    if page == "Dashboard":
        st.title("Welcome back, Mohd Ridzuan bin Ab Rahim 👋")
        st.markdown("---")
        
        # Metrics from original code
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Annual Leave Balance", "18 Days")
            st.metric("Medical Leave Balance", "12 Days")
            st.metric("Paternity Leave Balance", "12 Days")
        with col2:
            st.metric("Hospitalization Leave Balance", "60 Days")
            st.metric("Maternity Leave Balance", "98 Days")
            st.metric("Carry Forward Leave Balance", "4 Days")
        with col3:
            st.metric("Next Pay Date", "Mar 31, 2026")

    elif page == "Payslips":
        st.title("📄 Payslip Management")
        st.markdown("### Payroll History")
        
        # Mock Data from original code
        payslip_data = pd.DataFrame({
            "Month": ["January 2026", "February 2026", "March 2026", "April 2026", "May 2026", "June 2026"],
            "Net Pay": ["$9,500", "$9,500","$9,500", "$9,500","$9,500", "$9,500"],
            "Status": ["Paid", "Paid", "Paid", "Paid", "Paid", "Paid"]
        })
        st.dataframe(payslip_data, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Actions")
        selected_month = st.selectbox("Select Month", payslip_data["Month"])
        
        if st.button("View/Print Payslip"):
            st.success(f"Generating PDF for {selected_month}...")

    elif page == "Employee Details":
        st.title("👤 My Profile")
        st.markdown("### Personal Information")
        st.write("**Name:** Mohd Ridzuan bin Ab Rahim")
        st.write("**Employee ID:** DY202")
        st.write("**IC No:** 850620-14-1111")
        st.write("**Date of Birth:** 20/06/1985")
        st.write("**Mobile Number:** 013-4567890")
        st.write("**Address:** 1-G, JALAN SERI PUTRA 1/1F, BANDAR SERI PUTRA,43000 KAJANG, SELANGOR")
        st.write("**Work Email:** ridzuan.rahim@diyanas.com")
        st.write("**Personal Email:** ridzuan.rahim85@gmail.com")
        st.write("**Joined Date:** 05/01/2023")
        st.write("**Position:** Sr Software Test Engineer")
        st.write("**Contract Type:** Full-Time Employee")
        st.write("**Reporting Manager:** Wong Fei Hong")
        
        st.markdown("### Benefits")
        st.write("- Health Insurance: **Active**")
        st.write("- Dental Plan: **RM 500**")
        st.write("- Optical Plan: **RM 300**")
        st.write("- Medical Claim: **RM 1000**")
        st.write("- Parking Claim: **RM 100**")
        st.write("- Internet Plan: **RM 200**")
        
    elif page == "Leave Application":
        st.title("🌴 Leave Application")
        st.markdown("---")
        
        with st.form("leave_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                leave_type = st.selectbox("Leave Type", ["Annual Leave", "Medical Leave", "Paternity Leave", "Hospitalization Leave", "Maternity Leave", "Carry Forward Leave" ])
                start_date = st.date_input("Start Date", date.today())
                end_date = st.date_input("End Date", date.today())
            with col2:
                reason = st.text_area("Reason for Leave")
                
            submit_button = st.form_submit_button(label="Submit Application")
            
            if submit_button:
                st.success(f"Application for {leave_type} submitted successfully!")
                st.info(f"Dates: {start_date} to {end_date}")

    # ==========================================
    # --- ADMIN PAGES ---
    # ==========================================
    elif page == "Admin Dashboard":
        st.title("📊 Admin Panel - Overview")
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Employees", "150", "+2")
        col2.metric("Pending Leaves", "12", "-3")
        col3.metric("Payroll Status", "Processed")
        col4.metric("Avg Salary", "RM 7,500")

        st.markdown("---")
        st.subheader("Recent Leave Requests")
        
        leave_data = pd.DataFrame({
            "Employee": ["Ahmad", "Siti", "John", "Raju"],
            "Type": ["Annual", "Medical", "Annual", "Sick"],
            "Status": ["Pending", "Approved", "Pending", "Approved"]
        })
        st.dataframe(leave_data, use_container_width=True)

    elif page == "Manage Employees":
        st.title("👥 Employee Management")
        st.markdown("---")
        
        emp_data = pd.DataFrame({
            "ID": ["DY201", "DY202", "DY203"],
            "Name": ["Ahmad", "Ridzuan", "Siti"],
            "Position": ["Developer", "QA", "Manager"],
            "Department": ["IT", "IT", "HR"]
        })
        
        st.subheader("Current Employee List")
        st.dataframe(emp_data, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Add New Employee")
        with st.form("add_emp"):
            col1, col2 = st.columns(2)
            col1.text_input("Name")
            col2.text_input("Position")
            col1.text_input("Department")
            st.form_submit_button("Add Employee")

    elif page == "Payroll Processing":
        st.title("💰 Payroll Processing")
        st.markdown("---")
        
        payroll_data = pd.DataFrame({
            "Month": ["January", "February", "March"],
            "Total Amount": ["RM 1,125,000", "RM 1,125,000", "RM 1,130,000"],
            "Status": ["Paid", "Paid", "Pending"]
        })
        
        st.subheader("Payroll Summary")
        st.dataframe(payroll_data, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Process Current Month")
        if st.button("Calculate & Process March Payroll"):
            st.success("March Payroll Processed Successfully!")