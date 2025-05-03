# Use an official Miniconda image
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /app

# Copy environment setup files first
COPY requirements.txt .

# Create a new conda environment and install requirements
RUN conda create -n samih python=3.12 -y && \
    conda run -n samih pip install --upgrade pip && \
    conda run -n samih pip install -r requirements.txt && \
    conda clean -afy

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run Django server with the conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "samih", "python", "manage.py", "runserver", "0.0.0.0:8000"]

