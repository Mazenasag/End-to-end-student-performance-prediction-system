# --------- Base Image ---------
FROM python:3.11-slim

# --------- Set working directory ---------
WORKDIR /app

# --------- Copy project files ---------
COPY . /app

# --------- Upgrade pip and install dependencies ---------
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir \
    flask \
    numpy \
    pandas \
    scikit-learn

# --------- Expose Flask port ---------
EXPOSE 5000

# --------- Run the Flask app ---------
CMD ["python", "application.py"]
