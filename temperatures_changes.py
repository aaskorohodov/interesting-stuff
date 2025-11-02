"""Compares months temperatures in a year in a plot"""

import matplotlib.pyplot as plt


# Original temperatures (Jan to Feb, representing the months) Collected 1881-1915
original_temps = [-15.7, -13.7, -7.4, 1.7, 9.9, 14.8, 17.2, 14.7, 8.8, 0.5, -7.8, -13.5]

# Later temperatures (Jan to Feb, representing the months) Collected 1986-2020
later_temps = [-11.8, -9.5, -2.1, 6.2, 13.6, 17.0, 20.5, 17.8, 11.1, 4.7, -4.5, -9.5]

# Calculate the temperature difference for each month
temp_diffs = [later - original for later, original in zip(later_temps, original_temps)]

# Create a list of month numbers for the x-axis (1 to 12 representing Jan to Feb)
months = range(1, 13)

month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(months, temp_diffs, marker='o', linestyle='-', color='blue')

# Add labels and title
plt.xlabel("Month")  # Simplified x-axis label
plt.ylabel("Temperature Change (°C)")
plt.title("Temperature Change Over Time")

# Add a horizontal line at zero for reference
plt.axhline(y=0, color='gray', linestyle='--')

# Customize the plot
plt.xticks(months, month_names)  # Set x-axis ticks to month names
plt.grid(True)

# Show the plot
plt.show()

# Analyze the data
for i, diff in enumerate(temp_diffs):
    month = i + 1
    if diff > 0:
        print(f"Month {month}: Temperature increased by {diff:.1f}°C")
    elif diff < 0:
        print(f"Month {month}: Temperature decreased by {abs(diff):.1f}°C")
    else:
        print(f"Month {month}: Temperature remained the same")