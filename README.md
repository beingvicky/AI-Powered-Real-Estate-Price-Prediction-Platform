# AI-Powered Real Estate Price Prediction Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-FF9900?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

</div>

An AI-powered real estate valuation platform that predicts property prices using machine learning and provides a user-friendly web interface for homeowners, buyers, and real-estate analysts.

## Overview

This project combines:
- a React frontend for property input
- a FastAPI backend for prediction APIs
- machine learning regression models for valuation
- a comparison dashboard for model performance metrics
- market-aware pricing logic for cities like Bengaluru and Mysuru

Users enter property details such as:
- city/location
- area in sq.ft
- bedrooms
- bathrooms
- property type
- floor
- parking
- property age

The system estimates the market price in Indian Rupees and returns a price range in lakhs.

## Project Architecture

- Frontend: React + Vite
- Backend: FastAPI
- ML: scikit-learn regression models
- Model comparison: Linear Regression, Random Forest, Gradient Boosting
- Data: market-aware real-estate pricing patterns for Indian cities

## Features

- Real estate price prediction in ₹ lakhs
- City-based pricing support including Mysuru and Bengaluru
- Property input form with validation
- Model performance comparison (R², MAE, RMSE)
- Estimated price range output
- Fast API-based backend integration
- Easy local setup and run instructions

## Screenshots

### Prediction Form

![Prediction Form](screenshots/prediction-form.png)

### Price Result

![Prediction Result](screenshots/prediction-result.png)

## Tech Stack

- React
- Vite
- FastAPI
- Python
- scikit-learn
- Pandas
- NumPy
- Joblib
- Pydantic

## Model Comparison

This project evaluates multiple regression models:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

The app compares model quality using:
- R² score
- MAE
- RMSE

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/beingvicky/AI-Powered-Real-Estate-Price-Prediction-Platform.git
cd AI-Powered-Real-Estate-Price-Prediction-Platform
```

### 2. Backend setup

```bash
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python train_model.py
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Frontend setup

```bash
cd ../frontend
npm install
npm run dev -- --host 0.0.0.0 --port 4173
```

Open the app in your browser:

```text
http://localhost:4173
```

## API Endpoint

### Prediction

```http
POST http://localhost:8000/predict
```

Sample JSON body:

```json
{
  "location": "Mysuru",
  "area": 1200,
  "bedrooms": 2,
  "bathrooms": 2,
  "property_type": "Apartment",
  "floor": 2,
  "parking": 1,
  "age": 5
}
```

## Project Goals

This project is designed to showcase:
- full-stack application development
- ML model training and evaluation
- real-estate pricing estimation
- AI product thinking for a business use case

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Vicky Singh

## Contact

For questions or collaboration, reach out via GitHub: [@beingvicky](https://github.com/beingvicky)
