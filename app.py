import streamlit as st
from PIL import Image
import os

# Define the Car class
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

# Define the Customer class
class Customer:
    def __init__(self, name, car, days):
        self.name = name
        self.car = car
        self.days = days

    def __str__(self):
        return f"{self.name} rented {self.car.get_display_name()} for {self.days} days."

# Initialize session state for cars and rental history
if 'car_list' not in st.session_state:
    st.session_state.car_list = [
        Car("C001", "Toyota", "Camry", 60.0),
        Car("C002", "Honda", "Accord", 70.0),
        Car("C003", "Mahindra", "Thar", 150.0)
    ]

if 'rental_history' not in st.session_state:
    st.session_state.rental_history = []

# Streamlit app layout
st.title("🚗 Car Rental System")

# Customer name input
name = st.text_input("Customer Name")

# Car selection
car_options = [car.get_display_name() for car in st.session_state.car_list]
selected_car_name = st.selectbox("Select Car", car_options)
selected_car = next((car for car in st.session_state.car_list if car.get_display_name() == selected_car_name), None)

# Rental days input
days = st.number_input("Rental Days", min_value=1, step=1)

# Display car image
if selected_car:
    image_path = os.path.join("images", f"{selected_car.car_id}.jpg")
    if os.path.exists(image_path):
        st.image(image_path, width=300)
    else:
        st.warning("Image not found for the selected car.")

# Rent button functionality
if st.button("Rent"):
    if not name:
        st.error("Please enter the customer name.")
    elif not selected_car.available:
        st.error("Selected car is not available.")
    else:
        selected_car.available = False
        customer = Customer(name, selected_car, days)
        st.session_state.rental_history.append(customer)
        total_cost = selected_car.calculate_total(days)
        st.success(f"✅ {customer} | Total: ${total_cost}")

# Return button functionality
if st.button("Return"):
    if selected_car.available:
        st.info("Car is already returned.")
    else:
        selected_car.available = True
        st.success(f"🔁 {selected_car.get_display_name()} returned.")

# Display rental history
st.subheader("Rental History")
for record in st.session_state.rental_history:
    st.write(str(record))
