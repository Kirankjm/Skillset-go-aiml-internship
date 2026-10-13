# Web Interface Guide

Perfect Fitness Agent now includes a beautiful web-based interface built with Streamlit, providing a modern and user-friendly alternative to the terminal interface.

## 🌟 Features

- **Modern UI**: Clean, professional design with intuitive navigation
- **Interactive Forms**: Easy-to-use input fields with validation
- **Visual Results**: Metrics displayed with colorful charts and cards
- **Real-time Calculations**: Instant results as you input data
- **Responsive Design**: Works on desktop, tablet, and mobile
- **No Coding Required**: Click-based interactions
- **Sidebar Navigation**: Easy switching between tools

## 🚀 How to Run

### Step 1: Install Streamlit

If you haven't already, install Streamlit:

```bash
pip install streamlit
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

### Step 2: Launch the Web Interface

**Windows (Recommended):**
```bash
run_web.bat
```

**Mac/Linux:**
```bash
streamlit run web_interface.py
```

### Step 3: Open in Browser

The web interface will automatically open in your default browser at:
```
http://localhost:8501
```

If it doesn't open automatically, manually navigate to this URL in your browser.

## 📋 Available Tools

### 1. BMI Calculator
- Input your weight and height
- Get instant BMI calculation
- See health category (Underweight, Normal, Overweight, Obese)
- Receive personalized recommendations
- Visual health indicators

### 2. Calorie Calculator
- Enter age, gender, weight, height
- Select activity level
- Choose your goal (maintain, lose, gain weight)
- See BMR, TDEE, and target calories
- Visual breakdown of calorie needs

### 3. Meal Plan Calculator
- Add foods with calories and macronutrients
- Build your meal plan interactively
- See real-time totals
- Track protein, carbs, and fat
- Clear and rebuild as needed

### 4. Water Intake Calculator
- Enter your weight
- Select activity level
- Get daily water intake recommendations
- See liters, milliliters, and glass equivalents
- Helpful hydration tips

### 5. Sleep Calculator
- Enter your age
- Get recommended sleep duration
- See age-specific recommendations
- Sleep tips and best practices

### 6. Heart Rate Calculator
- Enter your age
- Select exercise intensity
- Get target heart rate zone
- See max heart rate
- Exercise tips for different intensities

### 7. Web Search
- Search for health information
- Get results from DuckDuckGo
- Browse titles, URLs, and snippets
- No API key required

## 🎨 Interface Features

### Sidebar Navigation
- Easy switching between tools
- Always visible on the left
- Collapsible on mobile

### Metric Cards
- Colorful result displays
- Large, readable numbers
- Clear labels

### Input Validation
- Prevents invalid inputs
- Helpful error messages
- Sensible default values

### Responsive Design
- Adapts to screen size
- Works on mobile devices
- Touch-friendly buttons

## 💡 Tips for Best Experience

1. **Use a Modern Browser**: Chrome, Firefox, Safari, or Edge for best performance
2. **Keep the Tab Open**: The Streamlit server runs as long as the tab is open
3. **Refresh for Updates**: If needed, refresh the page to reset the interface
4. **Use Keyboard Navigation**: Tab through input fields for faster data entry
5. **Bookmark the URL**: Save `http://localhost:8501` for quick access

## 🔧 Troubleshooting

### Port Already in Use
If you see "Port 8501 is already in use", run:
```bash
streamlit run web_interface.py --server.port 8502
```

### Streamlit Not Found
Make sure Streamlit is installed:
```bash
pip install streamlit
```

### Interface Not Loading
- Check that the terminal is still running
- Ensure no firewall is blocking localhost
- Try refreshing the browser

### Calculations Not Working
- Ensure all required fields are filled
- Check for valid numeric inputs
- Try refreshing the page

## 🎯 When to Use Web Interface vs Terminal

### Use Web Interface When:
- You want a modern, beautiful UI
- You're demonstrating to others
- You prefer click-based interactions
- You want visual metrics and charts
- You're on a tablet or mobile device

### Use Terminal Interface When:
- You prefer command-line tools
- You're scripting or automating
- You want faster startup time
- You're on a server without GUI
- You need to integrate with other CLI tools

## 📱 Mobile Access

The web interface is responsive and works on mobile devices:

1. Ensure your computer and mobile are on the same network
2. Find your computer's IP address (run `ipconfig` on Windows or `ifconfig` on Mac/Linux)
3. Run Streamlit with network access:
   ```bash
   streamlit run web_interface.py --server.address 0.0.0.0
   ```
4. On your mobile, navigate to: `http://YOUR_IP_ADDRESS:8501`

## 🔒 Security Note

The web interface runs locally on your machine. No data is sent to external servers (except for web search which uses DuckDuckGo). All calculations happen locally.

## 🎉 Enjoy Your New Web Interface!

The web interface provides the same powerful health calculations as the terminal version, but with a much more user-friendly and visually appealing experience. Perfect for demonstrations, daily use, or showing to friends and family!
