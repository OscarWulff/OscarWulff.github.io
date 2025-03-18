import matplotlib.pyplot as plt

# Sample data for the plot
x = [1, 2, 3, 4, 5]
y = [10, 20, 30, 40, 50]

# Create the plot
plt.figure(figsize=(6, 4))
plt.plot(x, y, marker="o", linestyle="-", color="blue", label="Trend Line")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Sample Matplotlib Plot")
plt.legend()
plt.grid(True)

# Save the plot
plt.savefig("assets/images/matplotlib_plot.png")  # Save to Jekyll's assets folder
plt.show()
