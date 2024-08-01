# statistics_logic.py

def calculate_points(events):
    points = 0
    for _, event in events.iterrows():
        if event['Code'] == '3-P':
            points += 3
        elif event['Code'] == '2-P':
            points += 2
        elif event['Code'] == 'F-T':
            points += 1
    return points

def calculate_field_goal_percentage(events):
    fgm = sum(1 for _, event in events.iterrows() if event['Code'] in ['2-P', '3-P'])
    fga = sum(1 for _, event in events.iterrows() if event['Code'] in ['2-P', '3-P', 'M2P', 'M3P'])
    return (fgm / fga) * 100 if fga else 0

def aggregate_statistics(events):
    stats = {
        'GP': len(events['Date'].unique()),
        'PTS': calculate_points(events),
        'FGM': sum(1 for _, event in events.iterrows() if event['Code'] in ['2-P', '3-P']),
        'FGA': sum(1 for _, event in events.iterrows() if event['Code'] in ['2-P', '3-P', 'M2P', 'M3P']),
        'FG%': calculate_field_goal_percentage(events),
        '3PM': sum(1 for _, event in events.iterrows() if event['Code'] == '3-P'),
        '3PA': sum(1 for _, event in events.iterrows() if event['Code'] in ['3-P', 'M3P']),
        'FTM': sum(1 for _, event in events.iterrows() if event['Code'] == 'F-T'),
        'FTA': sum(1 for _, event in events.iterrows() if event['Code'] in ['F-T', 'MFT']),
        'OREB': sum(1 for _, event in events.iterrows() if event['Code'] == 'ORB'),
        'DREB': sum(1 for _, event in events.iterrows() if event['Code'] == 'DRB'),
        'REB': sum(1 for _, event in events.iterrows() if event['Code'] in ['ORB', 'DRB']),
        'AST': sum(1 for _, event in events.iterrows() if event['Code'] == 'AST'),
        'TOV': sum(1 for _, event in events.iterrows() if event['Code'] == 'T-O'),
        'STL': sum(1 for _, event in events.iterrows() if event['Code'] == 'STL'),
        'BLK': sum(1 for _, event in events.iterrows() if event['Code'] == 'BLK'),
    }
    stats['3P%'] = (stats['3PM'] / stats['3PA']) * 100 if stats['3PA'] else 0
    stats['FT%'] = (stats['FTM'] / stats['FTA']) * 100 if stats['FTA'] else 0
    return stats
