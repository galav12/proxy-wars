# Proxy Wars

## 1. Introduction

The **Proxy Wars Tool** helps data scientists identify and mitigate bias-inducing proxy variables within datasets. Proxy variables are attributes that correlate with sensitive variables (e.g., gender, race, age) and may unintentionally introduce bias into machine learning models.

### Key Features:
- **CSV Dataset Upload**: Analyze numerical data from uploaded files.
- **Algorithm Selection**: Choose from Correlation Analysis, FACET, or Association Rule Mining (ARM) to identify proxy variables.
- **Dataset Filtering**: Refine datasets using random sampling or SQL-based filters.
- **Dark Mode Support**: Toggle between light and dark themes for a better user experience.
- **Results Visualization**: Display outputs in dynamic tables with sorting capabilities.

---

## 2. Getting Started

### System Requirements

- **Operating System**: Windows, macOS, or Linux

#### Dependencies:
- **Node.js**: v18.16.0 or higher
- **Python**: v3.11 or higher
- **Flask**: v2.3.3
- **React**: v18.2.0

### Installation

#### Install Dependencies:

1. Navigate to the **/frontend** folder and run:
   ```bash
   npm install
   ```

2. Navigate to the **/backend** folder and run:
   ```bash
   pip install -r requirements.txt
   ```

### Run the Application:

#### **Using Docker Container**

1. If not already installed, download Docker Desktop from [here](https://www.docker.com/products/docker-desktop).
2. Verify Docker installation:
   ```bash
   docker --version
   ```

3. Navigate to your project folder:
   ```bash
   cd path/to/project
   ```

4. Build the Docker container:
   ```bash
   docker-compose build
   ```

5. Start the Docker container:
   ```bash
   docker-compose up
   ```

6. Access the tool in Chrome:
   Open [http://localhost:3000](http://localhost:3000).

---

#### **Running on Terminals**

Open **2 terminals**: one for the frontend and one for the backend.

**Backend Setup:**
1. Navigate to the **backend** folder:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```bash
   python src/controllers/app.py
   ```

**Frontend Setup:**
1. Navigate to the **frontend** folder:
   ```bash
   cd frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

---

## 3. Features and Use Cases

#### 1. **Uploading a Dataset**

- Click the **Upload Dataset** button.
- Select a valid `.csv` file (only numerical columns).
- Click **Upload**.
- A confirmation message will appear, and the dataset columns will be listed.

---

#### 2. **Switching Between Dark Mode and Light Mode**

- Locate the **Dark Mode Toggle** in the top-right corner of the interface.
- Click to switch between **Light Mode** (default) and **Dark Mode**.

---

#### 3. **Algorithm Selection**

- From the dropdown menu, choose an algorithm:
  - **Correlation Analysis**: Calculates relationships between variables.
  - **FACET**: Detects redundancy using feature selection.
  - **Association Rule Mining (ARM)**: Generates association rules.

- If selecting **FACET**, specify a **Target Variable**.

---

#### 4. **Dataset Filtering Options**

- **Complete Dataset**: Use the full dataset.
- **Random Sampling**:
  - Specify a percentage (e.g., 50%).
  - Enter a **Random Seed** for reproducibility.
- **SQL Filter**: Enter a filter condition (e.g., `age > 30 AND income < 50000`).

---

#### 5. **Viewing Results**

- Click **Results** to run the analysis.
- The results are displayed in a table:
  - **Correlation Analysis**: Displays Pearson, Kendall, and Spearman coefficients.
  - **FACET**: Displays redundancy metrics.
  - **ARM**: Displays support, confidence, and lift values.

- **Sort** results by clicking on the column headers to organize by any metric.

---

#### 6. **Dark Mode Results Visualization**

- All tables and UI elements will adapt to **Dark Mode** when enabled.

---

#### 7. **Sorting Results**

- Use dropdowns to:
  - Select a column for sorting.
  - Choose a metric (e.g., Pearson coefficient for Correlation Analysis).
- Click the **Sort** button to organize results.

---

## 4. Troubleshooting

### Common Issues:
- **No File Uploaded**: Ensure you have selected a valid `.csv` file.
- **Target Variable Missing**: Choose a target variable if using **FACET**.
- **Sensitive Variables Not Set**: Ensure you have selected sensitive variables for analysis.

---

## 5. Appendix

### **Algorithm Details**:

- **Correlation Analysis**: Calculates relationships between variables using Pearson, Kendall, and Spearman coefficients.
- **FACET**: Detects redundancy using Random Forest feature selection.
- **Association Rule Mining (ARM)**: Identifies patterns and associations with metrics like support, confidence, and lift.

### **Example Datasets**:
- **Titanic Dataset**: Analyze survival likelihood based on various features.
- **Census Data**: Explore income-related proxies, such as education and occupation.

---
