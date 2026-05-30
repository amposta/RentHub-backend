# RentHub - Modern Rental Marketplace MVP

A production-ready frontend-first rental marketplace built with Django, inspired by Lazada, Shopee, and Airbnb.

## Features

✅ **Modern Responsive UI** - Mobile-first design  
✅ **Floating Auth Modal** - Non-intrusive login/register  
✅ **Verification Flow** - ID + Selfie verification  
✅ **Rental Cards** - E-commerce style listings  
✅ **Smooth Animations** - Hover effects & transitions  
✅ **Production CSS** - Tailwind-inspired custom styles  
✅ **Static Data** - No database needed  

## Quick Start

The repository now uses a separate React + Tailwind frontend and a Django backend API.

```bash
# Clone & setup Python backend
git clone <repo>
cd RentHub
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

In a second terminal, start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open the frontend at `http://localhost:3000` and the backend API at `http://localhost:8000/api/`.
