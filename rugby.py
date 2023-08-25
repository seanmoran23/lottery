import random
import pandas as pd

def assign_teams_randomly(participants, num_teams_per_participant, teams):
    """
    Assign teams to participants randomly.

    Args:
        participants (list): List of participant names.
        num_teams_per_participant (int): Number of teams to assign to each participant.
        teams (list): List of team dictionaries.

    Returns:
        dict: A dictionary containing participant names as keys and assigned teams as values.
    """
    random.shuffle(teams)
    assignments = {}

    for participant in participants:
        assigned_teams = []
        for _ in range(num_teams_per_participant):
            if teams:
                assigned_team = teams.pop()
                assigned_teams.append(assigned_team["Country"])  # Access the "Country" value
            else:
                break  # No more teams to assign
        assignments[participant] = assigned_teams

    return assignments

def calculate_implied_probabilities():
    """
    Calculate implied probabilities based on team odds.

    Args:
        teams (list): List of team dictionaries.

    Returns:
        dict: A dictionary containing team names as keys and their implied probabilities as values.
    """
    implied_probabilities = {team["Country"]: 1 / (team["Odds"] / 100) for team in teams}
    return implied_probabilities

def calculate_odds(team_assignments, implied_probabilities):
    """
    Calculate participant probabilities based on team assignments and implied probabilities.

    Args:
        participant_probabilities (dict): Dictionary containing participant names as keys and probabilities as values.
        implied_probabilities (dict): Dictionary containing team names as keys and implied probabilities as values.

    Returns:
        dict: A dictionary containing participant names as keys and their updated probabilities as values.
    """
    total_implied_probability = sum(implied_probabilities.values())

    # Calculate probability for each participant
    participant_probabilities = {participant: 0 for participant in participants}

    for participant in participants:
        for team in team_assignments[participant]:
            participant_probabilities[participant] += implied_probabilities[team] / total_implied_probability

    return participant_probabilities

if __name__ == "__main__":

    # https://www.world.rugby/tournaments/rankings/mru
    teams = [
        {'Country': 'Ireland', 'Rank': 91.82, 'Odds': 500},
        {'Country': 'New Zealand', 'Rank': 90.77, 'Odds': 250},
        {'Country': 'South Africa', 'Rank': 89.37, 'Odds': 450},
        {'Country': 'France', 'Rank': 89.22, 'Odds': 300},
        {'Country': 'Scotland', 'Rank': 84.01, 'Odds': 4000},
        {'Country': 'England', 'Rank': 81.53, 'Odds': 1100},
        {'Country': 'Argentina', 'Rank': 80.86, 'Odds': 2500},
        {'Country': 'Australia', 'Rank': 79.87, 'Odds': 1000},
        {'Country': 'Fiji', 'Rank': 78.7, 'Odds': 15000},
        {'Country': 'Wales', 'Rank': 78.26, 'Odds': 3300},
        {'Country': 'Georgia', 'Rank': 76.23, 'Odds': 50000},
        {'Country': 'Samoa', 'Rank': 76.19, 'Odds': 50000},
        {'Country': 'Italy', 'Rank': 74.63, 'Odds': 50000},
        {'Country': 'Japan', 'Rank': 74.29, 'Odds': 25000},
        {'Country': 'Tonga', 'Rank': 70.29, 'Odds': 50000},
        {'Country': 'Portugal', 'Rank': 68.61, 'Odds': 250000},
        {'Country': 'Uruguay', 'Rank': 66.63, 'Odds': 200000},
        {'Country': 'Romania', 'Rank': 64.56, 'Odds': 250000},
        {'Country': 'Namibia', 'Rank': 61.61, 'Odds': 250000},
        {'Country': 'Chile', 'Rank': 60.49, 'Odds': 250000},
    ]

    team_emojis = {
        'Ireland': '🇮🇪', 'New Zealand': '🇳🇿', 'South Africa': '🇿🇦', 'France': '🇫🇷', 'Scotland': '🏴󠁧󠁢󠁳󠁣󠁴󠁿',
        'England': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'Argentina': '🇦🇷', 'Australia': '🇦🇺', 'Wales': '🏴󠁧󠁢󠁷󠁬󠁳󠁿', 'Fiji': '🇫🇯',
        'Samoa': '🇼🇸', 'Georgia': '🇬🇪', 'Tonga': '🇹🇴', 'Italy': '🇮🇹', 'Japan': '🇯🇵', 'Portugal': '🇵🇹',
        'Namibia': '🇳🇦', 'Romania': '🇷🇴', 'Uruguay': '🇺🇾', 'Chile': '🇨🇱'
    }

    participants = ['Aisling', 'Peadar', 'Bróna', 'Ciarán', 'Conor Byrne', 'Conor Birkett', 'Félim', 'Paul', 'Sadhbh', 'Seán', 'Shauna', 'Stuart']

    num_teams_per_participant = len(teams) // len(participants)
    
    # Get teams based on rank
    teams = teams[:12]

    team_assignments = assign_teams_randomly(participants, 1, teams)

    implied_probabilities = calculate_implied_probabilities()

    participant_probabilities = calculate_odds(team_assignments, implied_probabilities)
    
    team_dict = {team['Country']: team for team in teams}

    # Create a list to store assignment data
    assignments_df = pd.DataFrame(columns=["Participant", "Country"])

    # Populate the list with assignment data
    for participant, countries in team_assignments.items():
        for country in countries:
            emoji = team_emojis[country]
            assignments_df = assignments_df.append({"Participant": participant, "Country": emoji + " " + country}, ignore_index=True)

    # Add the odds column to the DataFrame
    assignments_df = assignments_df.assign(Odds=[participant_probabilities[participant] for participant in assignments_df["Participant"]])
    assignments_df = assignments_df.sort_values(by="Participant")

    # Display team assignments and participant probabilities using the DataFrame
    for _, row in assignments_df.iterrows():
        print(f"{row['Participant']} was assigned to team: {row['Country']}")
        
    print("-------------------------")

    for _, row in assignments_df.iterrows():
        print(f"{row['Participant']} has a {row['Odds']*100:.2f}% chance of having a winning team.")

    print(assignments_df)