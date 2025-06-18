import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(num_entries=50):
    """Generate sample data for testing the efficiency tracker"""
    
    # Sample data pools
    developers = ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Wilson', 
                 'Frank Miller', 'Grace Lee', 'Henry Davis', 'Ivy Chen', 'Jack Taylor']
    
    teams = ['Platform Team', 'Frontend Team', 'Backend Team', 'DevOps Team', 'QA Team', 'Data Team']
    
    technologies = ['React', 'Java', 'Python', 'JavaScript', 'C#', '.NET', 'Node.js', 'Angular', 'Vue.js', 'Go']
    
    categories = ['Feature', 'Bug', 'Chore', 'Refactor', 'Documentation']
    
    areas_of_efficiency = ['Boilerplate Code', 'Test Cases', 'Documentation', 'API Integration', 
                          'Database Queries', 'Error Handling', 'Code Review', 'Debugging', 'Regex/Validation']
    
    task_types = ['API Development', 'UI Work', 'Test Writing', 'Bug Fixing', 'Code Review', 
                 'Database Work', 'Integration', 'Performance Optimization']
    
    completion_types = ['Inline Suggestion', 'Whole File', 'Code Completion', 'Chat Assistance']
    
    sample_notes = [
        'Generated regex in seconds', 'Helped with complex algorithm', 'Auto-completed API endpoints',
        'Suggested better error handling', 'Generated comprehensive tests', 'Improved code structure',
        'Faster database query optimization', 'Automated boilerplate creation', 'Enhanced documentation',
        'Streamlined integration logic', 'Optimized performance bottlenecks', 'Simplified complex logic'
    ]
    
    data = []
    
    # Generate data for the last 12 weeks
    start_date = datetime.now() - timedelta(weeks=12)
    
    for i in range(num_entries):
        # Random week within the last 12 weeks
        week_offset = random.randint(0, 11)
        week = start_date + timedelta(weeks=week_offset)
        
        # Generate realistic estimates and efficiency gains
        original_estimate = round(random.uniform(1, 16), 1)  # 1-16 hours
        efficiency_percentage = random.uniform(10, 50)  # 10-50% efficiency gain
        efficiency_gained = round(original_estimate * (efficiency_percentage / 100), 1)
        
        # Copilot usage (80% of entries use Copilot)
        copilot_used = random.choices(['Yes', 'No'], weights=[0.8, 0.2])[0]
        
        # If Copilot is used, higher efficiency gains
        if copilot_used == 'Yes':
            efficiency_gained = max(efficiency_gained, round(original_estimate * 0.15, 1))
        else:
            efficiency_gained = min(efficiency_gained, round(original_estimate * 0.1, 1))
        
        # Lines of code saved (correlated with time saved)
        lines_saved = int(efficiency_gained * random.uniform(20, 80))
        
        # Review time saved (usually less than efficiency gained)
        review_time_saved = round(efficiency_gained * random.uniform(0.1, 0.4), 1)
        
        entry = {
            'Week': week.strftime('%Y-%m-%d'),
            'Story_ID': f"ENG-{random.randint(1000, 9999)}",
            'Developer_Name': random.choice(developers),
            'Team_Name': random.choice(teams),
            'Technology': random.choice(technologies),
            'Original_Estimate_Hours': original_estimate,
            'Efficiency_Gained_Hours': efficiency_gained,
            'Copilot_Used': copilot_used,
            'Category': random.choice(categories),
            'Area_of_Efficiency': random.choice(areas_of_efficiency),
            'Task_Type': random.choice(task_types),
            'Completion_Type': random.choice(completion_types),
            'Lines_of_Code_Saved': lines_saved,
            'Subjective_Ease_Rating': random.randint(3, 5) if copilot_used == 'Yes' else random.randint(2, 4),
            'Review_Time_Saved_Hours': review_time_saved,
            'Bugs_Prevented': random.choices(['Yes', 'No'], weights=[0.3, 0.7])[0],
            'PR_Merged': random.choices(['Yes', 'No'], weights=[0.85, 0.15])[0],
            'Notes_Observations': random.choice(sample_notes)
        }
        
        data.append(entry)
    
    return pd.DataFrame(data)

def main():
    """Generate and save sample data"""
    print("Generating sample data...")
    
    # Generate sample data
    df = generate_sample_data(50)
    
    # Save to Excel
    filename = "developer_efficiency_data.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Efficiency_Data')
        
        # Calculate and save metrics
        df['Efficiency_Percentage'] = (df['Efficiency_Gained_Hours'] / df['Original_Estimate_Hours'] * 100).round(2)
        
        # Developer summary
        dev_summary = df.groupby('Developer_Name').agg({
            'Efficiency_Gained_Hours': 'sum',
            'Original_Estimate_Hours': 'sum',
            'Lines_of_Code_Saved': 'sum',
            'Story_ID': 'count'
        }).round(2)
        dev_summary.columns = ['Total_Time_Saved', 'Total_Original_Time', 'Total_Lines_Saved', 'Total_Stories']
        dev_summary['Overall_Efficiency_Percentage'] = (
            dev_summary['Total_Time_Saved'] / dev_summary['Total_Original_Time'] * 100
        ).round(2)
        
        dev_summary.to_excel(writer, sheet_name='Calculated_Metrics')
    
    print(f"Sample data saved to {filename}")
    print(f"Generated {len(df)} entries")
    print("\nSample statistics:")
    print(f"Total time saved: {df['Efficiency_Gained_Hours'].sum():.1f} hours")
    print(f"Average efficiency: {df['Efficiency_Percentage'].mean():.1f}%")
    print(f"Copilot usage rate: {(df['Copilot_Used'] == 'Yes').mean() * 100:.1f}%")
    print(f"Total lines saved: {df['Lines_of_Code_Saved'].sum():,}")

if __name__ == "__main__":
    main() 