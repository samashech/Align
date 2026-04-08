import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_chart(skills):
    # Creating dummy frequency for visualization
    data = {"Skills": skills, "Demand Score": [i*10 for i in range(len(skills), 0, -1)]}
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(8, 4))
    sns.barplot(x="Demand Score", y="Skills", data=df, palette="viridis")
    plt.title("Market Demand for Your Skills")
    
    path = "static/trend_chart.png"
    plt.savefig(path)
    plt.close()
    return path
