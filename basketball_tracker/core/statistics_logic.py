class StatisticsLogic:
    def __init__(self, events):
        self.events = events

    def calculate_points(self):
        points = 0
        for _, event in self.events.iterrows():
            if event['Code'] == '3-P':
                points += 3
            elif event['Code'] == '2-P':
                points += 2
            elif event['Code'] == 'F-T':
                points += 1
        return points

    def calculate_field_goal_percentage(self):
        shots_made = sum(1 for _, event in self.events.iterrows() if event['Code'] == '2-P')
        shots_attempted = sum(1 for _, event in self.events.iterrows() if event['Code'] in ['2-P', 'M2P'])
        return (shots_made / shots_attempted) * 100 if shots_attempted else 0

    def calculate_three_point_percentage(self):
        shots_made = sum(1 for _, event in self.events.iterrows() if event['Code'] == '3-P')
        shots_attempted = sum(1 for _, event in self.events.iterrows() if event['Code'] in ['3-P', 'M3P'])
        return (shots_made / shots_attempted) * 100 if shots_attempted else 0

    def calculate_free_throw_percentage(self):
        shots_made = sum(1 for _, event in self.events.iterrows() if event['Code'] == 'F_T')
        shots_attempted = sum(1 for _, event in self.events.iterrows() if event['Code'] in ['F-T', 'MFT'])
        return (shots_made / shots_attempted) * 100 if shots_attempted else 0

    def aggregate_statistics(self):
        stats = {
            'PTS': self.calculate_points(),
            'FGM': sum(1 for _, event in self.events.iterrows() if event['Code'] == '2-P'),
            'FGA': sum(1 for _, event in self.events.iterrows() if event['Code'] in ['2-P', 'M2P']),
            'FG%': self.calculate_field_goal_percentage(),
            '3PM': sum(1 for _, event in self.events.iterrows() if event['Code'] == '3-P'),
            '3PA': sum(1 for _, event in self.events.iterrows() if event['Code'] in ['3-P', 'M3P']),
            '3P%': self.calculate_three_point_percentage(),
            'FTM': sum(1 for _, event in self.events.iterrows() if event['Code'] == 'F-T'),
            'FTA': sum(1 for _, event in self.events.iterrows() if event['Code'] in ['F-T', 'MFT']),
            'FT%': self.calculate_free_throw_percentage(),
            'OREB': sum(1 for _, event in self.events.iterrows() if event['Code'] == 'ORB'),
            'DREB': sum(1 for _, event in self.events.iterrows() if event['Code'] == 'DRB'),
            'REB': sum(1 for _, event in self.events.iterrows() if event['Code'] in ['ORB', 'DRB']),
            'AST': sum(1 for _, event in self.events.iterrows() if event['Code'] == 'AST'),
            'TOV': sum(1 for _, event in self.events.iterrows() if event['Code'] == 'T-O'),
            'STL': sum(1 for _, event in self.events.iterrows() if event['Code'] == 'STL'),
            'BLK': sum(1 for _, event in self.events.iterrows() if event['Code'] == 'BLK'),
            'PFL': sum(1 for _, event in self.events.iterrows() if event['Code'] == 'PFL'),
            'SFL': sum(1 for _, event in self.events.iterrows() if event['Code'] == 'SFL'),
            'GP': len(self.events['Date'].unique()),
        }
        return stats
