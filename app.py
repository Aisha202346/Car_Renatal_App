import streamlit as st
from PIL import Image
import os

# Define Car and Customer classes
class Car:
    def __init__(self, car_id, brand, model, price_per_day):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.price_per_day = price_per_day
        self.available = True

    def get_display_name(self):
        return f"{self.car_id} - {self.brand} {self.model}"

    def calculate_total(self, days):
        return self.price_per_day * days

class Customer:
    def __init__(self, name, car, days):
        self.name = name
        self.car = car
        self.days = days

    def __str__(self):
        return f"{self.name} rented {self.car.get_display_name()} for {self.days} days."

# Sample car list
car_list = [
    Car("C001", "Toyota", "Camry", 60.0),
    Car("C002", "Honda", "Accord", 70.0),
    Car("C003", "Mahindra", "Thar", 150.0)
]

# Session state to store history and availability
if "rental_history" not in st.session_state:
    st.session_state.rental_history = []
if "car_status" not in st.session_state:
    st.session_state.car_status = {car.car_id: car.available for car in car_list}

st.title("🚗 Car Rental System")

# Input form
with st.form("rental_form"):
    name = st.text_input("Customer Name")
    selected_car_display = st.selectbox("Select Car", [car.get_display_name() for car in car_list])
    days = st.number_input("Rental Days", min_value=1, step=1)
    submitted = st.form_submit_button("Rent Car")

    if submitted:
        selected_index = [car.get_display_name() for car in car_list].index(selected_car_display)
        selected_car = car_list[selected_index]

        if not st.session_state.car_status[selected_car.car_id]:
            st.warning("🚫 Car is not available.")
        else:
            st.session_state.car_status[selected_car.car_id] = False
            customer = Customer(name, selected_car, int(days))
            st.session_state.rental_history.append(customer)
            st.success(f"✅ {customer} | Total: ${selected_car.calculate_total(days):.2f}")

# Return car
st.subheader("🔁 Return a Car")
return_car_display = st.selectbox("Select Car to Return", [car.get_display_name() for car in car_list])
if st.button("Return Car"):
    selected_index = [car.get_display_name() for car in car_list].index(return_car_display)
    car_to_return = car_list[selected_index]
    if st.session_state.car_status[car_to_return.car_id]:
        st.info("Car is already returned.")
    else:
        st.session_state.car_status[car_to_return.car_id] = True
        st.success(f"🔁 {car_to_return.get_display_name()} returned.")

# Show car image
st.subheader("🚘 Car Preview")
selected_index = [car.get_display_name() for car in car_list].index(return_car_display)
image_path = f"images/{car_list[selected_index].car_id}.jpg"

if os.path.exists(image_path):
    st.image(Image.open(image_path), width=300)
else:
    st.info("No image available for this car.")

# Rental log
st.subheader("📜 Rental History")
if st.session_state.rental_history:
    for log in st.session_state.rental_history:
        st.text(str(log))
else:
    st.info("No rentals yet.")
