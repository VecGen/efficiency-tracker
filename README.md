# 🚀 Developer Efficiency Tracker with Copilot

A comprehensive Streamlit application for tracking and analyzing developer productivity gains from AI coding assistants like GitHub Copilot. This tool helps engineering teams measure, visualize, and optimize their efficiency improvements.

## ✨ Features

### 📝 Data Entry
- **User-friendly forms** for recording efficiency data
- **Comprehensive tracking** of 18+ metrics per entry
- **Real-time validation** and data persistence
- **Excel integration** for seamless data management

### 📊 Interactive Dashboard
- **Key Performance Metrics** - Total time saved, efficiency percentages, usage rates
- **Time Series Analysis** - Weekly efficiency trends over time
- **Category Breakdown** - Efficiency by task type, technology, and area
- **Team Performance** - Compare efficiency across teams and developers
- **Correlation Analysis** - Identify relationships between different metrics
- **Export Capabilities** - Download data and visualizations

### 🗂️ Data Management
- **Import/Export** Excel files
- **Data validation** and cleaning
- **Row-level editing** and deletion
- **Backup and restore** functionality

## 📋 Tracked Metrics

### Core Metrics (Your Original Requirements)
| Metric | Description | Sample Value |
|--------|-------------|--------------|
| **Week** | Tracking period | `2024-01-15` |
| **Story ID** | Ticket/task identifier | `ENG-1542` |
| **Original Estimate** | Time without AI assistance | `8 hours` |
| **Efficiency Gained** | Time saved using Copilot | `2 hours` |
| **Category** | Type of work | `Feature/Bug/Chore` |
| **Area of Efficiency** | Where Copilot helped most | `Boilerplate Code` |

### Enhanced Metrics (Additional Insights)
| Metric | Purpose | Sample Value |
|--------|---------|--------------|
| **Developer Name** | Individual tracking | `John Doe` |
| **Team Name** | Team-level analysis | `Platform Team` |
| **Technology** | Tech stack insights | `React/Java/Python` |
| **Copilot Usage** | Adoption tracking | `Yes/No` |
| **Task Type** | Granular categorization | `API Development` |
| **Completion Type** | Type of AI assistance | `Inline Suggestion` |
| **Lines of Code Saved** | Quantitative impact | `120 lines` |
| **Subjective Ease Rating** | Developer satisfaction | `4/5` |
| **Review Time Saved** | Code review efficiency | `1 hour` |
| **Bugs Prevented** | Quality improvement | `Yes/No` |
| **PR Merged Status** | Completion tracking | `Yes/No` |
| **Notes** | Qualitative feedback | `Generated regex instantly` |

### Calculated Metrics
- **Efficiency Percentage** = (Time Saved / Original Estimate) × 100
- **Adoption Rate** = (Copilot Usage / Total Entries) × 100
- **Average Time Saved per Week** - Trend analysis
- **Team Efficiency Comparison** - Relative performance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data** (optional):
   ```bash
   python sample_data_generator.py
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📖 Usage Guide

### 1. Data Entry Page
- Navigate to **"Data Entry"** from the sidebar
- Fill out the comprehensive form with your efficiency data
- Click **"Add Entry"** to save to Excel
- Data is automatically validated and stored

### 2. Dashboard Page
- View **key metrics** at the top (total time saved, efficiency %, etc.)
- Explore **interactive charts**:
  - Weekly efficiency trends
  - Category and technology breakdowns
  - Developer performance comparisons
  - Correlation analysis heatmap
- Use **team performance table** for detailed comparisons

### 3. Data Management Page
- **Export** your data as Excel files
- **Import** existing Excel data
- **View and edit** current entries
- **Delete** specific rows or clear all data

## 📊 Dashboard Insights

### Key Visualizations
1. **Time Series Chart** - Track efficiency trends over time
2. **Category Bar Charts** - Identify most impactful areas
3. **Technology Pie Chart** - See which tech stacks benefit most
4. **Developer Performance** - Compare individual contributions
5. **Correlation Heatmap** - Understand metric relationships
6. **Team Comparison Table** - Aggregate team statistics

### Sample Dashboard Metrics
- **Total Time Saved**: 156.3 hours
- **Average Efficiency**: 28.5%
- **Copilot Usage Rate**: 78.2%
- **Total Lines Saved**: 15,420

## 🗃️ Data Structure

The Excel file contains two sheets:
1. **Efficiency_Data** - Raw entry data
2. **Calculated_Metrics** - Derived analytics

### Excel Column Mapping
```
Week → Date of work completion
Story_ID → Jira/ticket reference
Developer_Name → Team member identifier
Team_Name → Organizational unit
Technology → Programming language/framework
Original_Estimate_Hours → Baseline time estimate
Efficiency_Gained_Hours → Time saved with Copilot
... (and 11 more columns)
```

## 🔧 Customization

### Adding New Categories
Edit the dropdown options in `app.py`:
```python
categories = ["Feature", "Bug", "Chore", "Refactor", "Documentation", "YourNewCategory"]
```

### Modifying Metrics
Add new columns to the `create_empty_dataframe()` function and corresponding form fields.

### Styling
Customize the CSS in the `st.markdown()` section for different themes and layouts.

## 📈 Best Practices

### Data Collection
- **Consistent timing** - Record data weekly
- **Accurate estimates** - Use realistic baseline times
- **Detailed notes** - Capture qualitative insights
- **Regular reviews** - Analyze trends monthly

### Analysis Tips
- **Focus on trends** rather than absolute numbers
- **Compare teams** with similar tech stacks
- **Identify top performers** for knowledge sharing
- **Track adoption rates** to measure tool effectiveness

## 🔍 Troubleshooting

### Common Issues
1. **Excel file locked** - Close Excel before running the app
2. **Import errors** - Ensure Excel file has correct column names
3. **Chart not displaying** - Check if data exists for selected filters
4. **Performance issues** - Limit data to recent time periods

### Error Messages
- **"No data available"** - Add entries via Data Entry page
- **"Error loading Excel"** - Check file permissions and format
- **"Error saving to Excel"** - Ensure file isn't open in another program

## 📝 Sample Data

Run the sample data generator to create realistic test data:
```bash
python sample_data_generator.py
```

This creates 50 sample entries with:
- 10 developers across 6 teams
- 12 weeks of historical data
- Realistic efficiency patterns
- Varied technology usage

## 🤝 Contributing

Feel free to enhance this tool by:
- Adding new visualization types
- Implementing additional metrics
- Improving the UI/UX
- Adding data export formats
- Creating automated reports

## 📄 License

This project is open source and available under the MIT License.

---

**Happy tracking! 🚀** 

*Measure your AI-assisted development efficiency and unlock your team's potential.* 