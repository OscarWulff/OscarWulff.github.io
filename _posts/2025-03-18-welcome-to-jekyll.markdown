---
layout: post
title: "Visualizing Data with Jekyll"
date: 2025-03-18 10:33:09 +0100
categories: data visualization
---

# **Visualizing Data with Jekyll** 📊  

One of the great things about Jekyll is that you can use it to create a blog that showcases **data visualizations**! Today, we’ll walk through embedding both **static** and **interactive** plots into a Jekyll post.  

---

## **📌 Adding a Static Plot (Matplotlib)**  

Let's start with a simple **Matplotlib** plot. Below, we’ve generated and saved a plot showing a basic trend line.  

### **Python Code to Generate the Plot**
To create this plot, run the following Python script in your local environment:  

```python
import matplotlib.pyplot as plt

# Sample data
x = [1, 2, 3, 4, 5]
y = [10, 20, 30, 40, 50]

# Create the plot
plt.figure(figsize=(6,4))
plt.plot(x, y, marker="o", linestyle="-", color="blue", label="Trend Line")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Sample Matplotlib Plot")
plt.legend()
plt.grid(True)

# Save the plot in your Jekyll assets folder
plt.savefig("assets/images/matplotlib_plot.png")
plt.show()
```

### **Testing*
Test