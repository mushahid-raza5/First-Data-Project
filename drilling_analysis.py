
import pandas as pd
import matplotlib.pyplot as plt

file_path = r"C:\Users\dell\OneDrive\Documents\Python Scripts\Drilling_Data_Sample.CSV"

def load_data(file_path):
    """Reads a CSV file into a DataFrame."""
    try:
        data = pd.read_csv(file_path)
        print("Data successfully loaded!")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

data = load_data(file_path)

if data is not None:
    print(data.head())

def clean_data(data):
    """Cleans and wrangles the data by handling missing values, normalizing column names, and reporting types."""
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
    print("Cleaning data...")
    data = data.dropna()
    data.columns = [col.strip().replace(" ", "_").lower() for col in data.columns]
    print("Column names normalized.")

    for col in data.columns:
        dtype = data[col].dtype
        if dtype == 'object':
            continue
        elif pd.api.types.is_numeric_dtype(data[col]):
            data[col] = data[col].clip(upper=data[col].quantile(0.99))
    print("Data wrangling complete!")
    return data

def analyze_data(data):
    """Analyzes the data by displaying basic statistics."""
    print("Analyzing data...")
    print("\nSummary Statistics:")
    print(data.describe())

    print("\nData Types:")
    print(data.dtypes)

def plot_rop(data):
    """Plots Rate of Penetration over time."""
    plt.figure(figsize=(10, 6))
    plt.plot(data['time'], data['md_rop'], marker='o', linestyle='-', color='b')
    plt.title("Rate of Penetration (MD_ROP) Over Time")
    plt.xlabel("Time")
    plt.ylabel("MD_ROP (ft/h)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("md_rop_trend.png")
    plt.show()

def custom_analysis(data, column_name):
    """Custom function to calculate skewness of a column."""
    if column_name in data.columns:
        if pd.api.types.is_numeric_dtype(data[column_name]):
            skewness = data[column_name].skew()
            print(f"The skewness of '{column_name}' is: {skewness}")
        else:
            print(f"Column '{column_name}' is not numeric. Skewness not applicable.")
    else:
        print(f"Column '{column_name}' does not exist in the dataset.")

if __name__ == "__main__":
    dataset = load_data(file_path)
    if dataset is not None:
        cleaned_data = clean_data(dataset)
        print("Column names after cleaning:", cleaned_data.columns)
        analyze_data(cleaned_data)
        plot_rop(cleaned_data)
        custom_analysis(cleaned_data, 'md_rop')
