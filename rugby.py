import random

def assign_teams_randomly(participants, num_teams_per_participant, teams):
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
    implied_probabilities = {team["Country"]: 1 / (team["Odds"] / 100) for team in teams}
    return implied_probabilities

def calculate_odds(team_assignments):
    implied_probabilities = calculate_implied_probabilities()
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
        {'Tier': "1", 'Country': 'Ireland', 'Rank': 91.82, 'Odds': 500},
        {'Tier': "1", 'Country': 'New Zealand', 'Rank': 90.77, 'Odds': 250},
        {'Tier': "1", 'Country': 'South Africa', 'Rank': 89.37, 'Odds': 450},
        {'Tier': "1", 'Country': 'France', 'Rank': 89.22, 'Odds': 300},
        {'Tier': "1", 'Country': 'Scotland', 'Rank': 84.01, 'Odds': 4000},
        {'Tier': "1", 'Country': 'England', 'Rank': 81.53, 'Odds': 1100},
        {'Tier': "1", 'Country': 'Argentina', 'Rank': 80.86, 'Odds': 2500},
        {'Tier': "1", 'Country': 'Australia', 'Rank': 79.87, 'Odds': 1000},
        {'Tier': "1", 'Country': 'Wales', 'Rank': 78.26, 'Odds': 3300},
        {'Tier': "1", 'Country': 'Fiji', 'Rank': 78.7, 'Odds': 15000},
        {'Tier': "2", 'Country': 'Samoa', 'Rank': 76.19, 'Odds': 50000},
        {'Tier': "2", 'Country': 'Georgia', 'Rank': 76.23, 'Odds': 50000},
        {'Tier': "2", 'Country': 'Tonga', 'Rank': 70.29, 'Odds': 50000},
        {'Tier': "2", 'Country': 'Italy', 'Rank': 74.63, 'Odds': 50000},
        {'Tier': "2", 'Country': 'Japan', 'Rank': 74.29, 'Odds': 25000},
        {'Tier': "2", 'Country': 'Portugal', 'Rank': 68.61, 'Odds': 250000},
        {'Tier': "2", 'Country': 'Namibia', 'Rank': 61.61, 'Odds': 250000},
        {'Tier': "2", 'Country': 'Romania', 'Rank': 64.56, 'Odds': 250000},
        {'Tier': "2", 'Country': 'Uruguay', 'Rank': 66.63, 'Odds': 200000},
        {'Tier': "2", 'Country': 'Chile', 'Rank': 60.49, 'Odds': 250000},
    ]

    participants = ['Aisling', 'Peadar', 'Bróna', 'Ciarán', 'Conor Byrne', 'Conor Birkett', 'Félim', 'Paul', 'Sadhbh', 'Seán', 'Shauna', 'Stuart']

    num_teams_per_participant = len(teams) // len(participants)
    
    # Splitting teams based on rank
    tier_one = teams[:12]
    tier_two = teams[20:]

    tier_one_assignments = assign_teams_randomly(participants, 1, tier_one)
    tier_two_assignments = assign_teams_randomly(participants, 1, tier_two)
    # Combining the two assignments
    team_assignments = {
        participant: tier_one_assignments[participant] + tier_two_assignments[participant]
        for participant in participants
    }

    implied_probabilities = calculate_implied_probabilities()
    participant_probabilities = calculate_odds(team_assignments)
    team_dict = {team['Country']: team for team in teams}

    # Print team assignments and participant probabilities
    for participant, assigned_teams in team_assignments.items():
        formatted_teams = ''.join(
            f"[Tier {team_dict[team]['Tier']}] {team: <15}" for team in assigned_teams
        )
        print(f"{participant:<10} got assigned to teams: {formatted_teams}")


    print("-------------------------")

    for participant, probability in participant_probabilities.items():
        print(f"{participant:<10} has a probability of {probability * 100:.2f}% to have a winning team.")