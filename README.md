# 🍽️ FinalMealMate (Meal Buddy)

> 🚀 A Full-Stack Online Food Ordering and Delivery Web Application built with **Django**, integrated with **Razorpay Payment Gateway**, and hosted on **GitHub Pages (Frontend)** with future backend deployment on **Render**.

---

## 🌐 **Live Demo**
🔗 **[Click Here to View the Website](https://jyothinadh025.github.io/FinalMealMate/)**  
*(Frontend live on GitHub Pages — Backend deployment coming soon!)*

---

## 🧠 **Overview**

**FinalMealMate (Meal Buddy)** is a full-stack food ordering and restaurant management web application.  
It allows users to browse restaurants, explore menus, add dishes to a dynamic cart, and securely complete payments through **Razorpay**.  

The project includes:
- A **customer-facing UI** for ordering meals  
- An **admin dashboard** to manage restaurants and menus  
- A **secure online payment flow** using Razorpay API  

---

## 🚀 **Features**

### 👤 User Authentication
- Secure **Signup** and **Login** system for customers  
- Separate **Admin access** for managing restaurants and menus  

### 🍴 Restaurant Management (Admin)
- Add, update, or delete restaurants and menu items  
- Upload restaurant pictures, cuisine type, and ratings  

### 🛒 Dynamic Cart System
- Add or remove items instantly using “+” and “−” buttons  
- Automatic total price calculation  
- Real-time cart updates with JavaScript interactivity  

### 💳 Razorpay Payment Integration
- Integrated **Razorpay Checkout API** for secure online payments  
- Test mode setup for safe payment simulation  
- Fixed demo contact number displayed in checkout (non-editable)  
- Automatic redirect to success or failure pages post-payment  

### 🧾 Order Summary
- View full order before payment  
- Cart automatically clears after successful payment  
- Displays order confirmation message  

---

## 🖥️ **Tech Stack**

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap |
| **Backend** | Django Framework (Python) |
| **Database** | SQLite |
| **Payment Gateway** | Razorpay API |
| **Version Control** | Git & GitHub |
| **Environment Management** | Python Dotenv |
| **Hosting (Frontend)** | GitHub Pages |
| **Hosting (Backend)** | Render / Railway / Heroku |

---

## 🔐 **Security**

- Razorpay keys are securely stored in `.env` (excluded from Git)  
- `.gitignore` ensures sensitive files and local data remain private  
- Payment requests are server-verified and protected  

---

## 🎨 **User Interface Highlights**

✨ Gradient backgrounds and smooth transitions  
📱 Fully responsive design for mobile and desktop  
🛍️ Interactive cart with live total updates  
💳 Razorpay checkout styled to match the theme  

---

## 📸 **Screenshots**

| Page | Preview |
|------|----------|
| 🏠 Home | ![Home](https://user-images.githubusercontent.com/placeholder/home.png) |
| 🍕 Menu | ![Menu](https://user-images.githubusercontent.com/placeholder/menu.png) |
| 🛒 Cart | ![Cart](https://user-images.githubusercontent.com/placeholder/cart.png) |
| 💳 Checkout | ![Checkout](https://user-images.githubusercontent.com/placeholder/checkout.png) |

> _(Replace these links with your own screenshots once hosted.)_

---

## ⚙️ **Installation & Setup**

Follow these steps to run the project locally:

```bash
# 1️⃣ Clone this repository
git clone https://github.com/jyothinadh025/FinalMealMate.git
cd FinalMealMate

# 2️⃣ Create a virtual environment
python -m venv env
env\Scripts\activate  # For Windows
source env/bin/activate  # For Mac/Linux

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Create a .env file and add your Razorpay keys

# 5️⃣ Run migrations
python manage.py migrate

# 6️⃣ Start the development server
python manage.py runserver
🧠 Learning Outcomes
Full-Stack Development using Django

Razorpay Payment Integration

Secure API Key Handling with .env

Interactive Frontend with JavaScript

Database management via Django ORM

Hosting and Version Control with GitHub

💡 Future Enhancements
Add user order history and tracking

Real-time delivery status updates

Email/SMS notifications for orders

Add restaurant reviews and ratings

Deploy full-stack version with backend API hosting

👨‍💻 Developer
JyothiNadh
🎓 B.E. in Computer Science and Engineering
💼 Full Stack Developer | Python | Django | React | SQL
🌐 Portfolio — jyothinadh025.github.io
📧 ajyothinadh@gmail.com

🪙 Acknowledgements
Django Documentation

Razorpay API Docs

Bootstrap Framework

Unsplash (for stock images)

⭐ If you like this project, give it a star!