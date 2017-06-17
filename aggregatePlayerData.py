import csv
from collections import namedtuple # for readable code

output_csv_name = './tennis_atp-master/player_statics.csv'
result_list = []
header_statics=['playerName', 'rank', 'ace', 'serPt', 'df', 'p_1stSerIn', 'p_2ndSerIn',
                'p_1stWon', 'p_2ndWon', 'bpSaved','bpFaced', 'bpConverted', 'bpGet',
                'retPtWon', 'retPt', 'serGmWon', 'serGm', 'retGmWon', 'retGm']


def read_player_data(player, rank, startyear = 1968, endyear = 2017):
    statics = {} # for saving the data of player
    # initial the dict
    for keyword in header_statics:
        if keyword == 'playerName':
            statics['playerName'] = player
        elif keyword == 'rank':
            statics['rank'] = int(rank)
        else:
            statics[keyword] = 0

    for year in range(startyear, endyear+1): # from staryear to endyear(inclusive)
        with open('./tennis_atp-master/atp_matches_'+str(year)+'.csv') as f:
            csvfile = csv.reader(f)
            headings = next(csvfile)
            Row = namedtuple('Row', headings)
            # search player in csvfiles
            for r in csvfile:
                # clear empty string
                def g(x):
                    if '' == x:
                        return '0'
                    else:
                        return x
                row = Row(*map(g, r))
                if row.winner_name == player: # if the player is winner of the match
                    statics['ace'] += int(row.w_ace)
                    statics['serPt'] += int(row.w_svpt)
                    statics['df'] += int(row.w_df)
                    statics['p_1stSerIn'] += int(row.w_1stIn)
                    statics['p_2ndSerIn'] += int(row.w_svpt) - int(row.w_1stIn) - int(row.w_df)
                    statics['p_1stWon'] += int(row.w_1stWon)
                    statics['p_2ndWon'] += int(row.w_2ndWon)
                    statics['bpSaved'] += int(row.w_bpSaved)
                    statics['bpFaced'] += int(row.w_bpFaced)
                    statics['bpConverted'] += int(row.l_bpFaced) - int(row.l_bpSaved)
                    statics['bpGet'] += int(row.l_bpFaced)
                    statics['retPtWon'] += int(row.l_svpt) - int(row.l_1stWon) - int(row.l_2ndWon) + int(row.l_df)
                    statics['retPt'] += int(row.l_svpt)
                    statics['serGmWon'] += int(row.w_SvGms) - (int(row.w_bpFaced) - int(row.w_bpSaved))
                    statics['serGm'] += int(row.w_SvGms)
                    statics['retGmWon'] += int(row.l_bpFaced) - int(row.l_bpSaved)
                    statics['retGm'] += int(row.l_SvGms)
                elif row.loser_name == player: # if the player is loser of the match
                    statics['ace'] += int(row.l_ace)
                    statics['serPt'] += int(row.l_svpt)
                    statics['df'] += int(row.l_df)
                    statics['p_1stSerIn'] += int(row.l_1stIn)
                    statics['p_2ndSerIn'] += int(row.l_svpt) - int(row.l_1stIn) - int(row.l_df)
                    statics['p_1stWon'] += int(row.l_1stWon)
                    statics['p_2ndWon'] += int(row.l_2ndWon)
                    statics['bpSaved'] += int(row.l_bpSaved)
                    statics['bpFaced'] += int(row.l_bpFaced)
                    statics['bpConverted'] += int(row.w_bpFaced) - int(row.w_bpSaved)
                    statics['bpGet'] += int(row.w_bpFaced)
                    statics['retPtWon'] += int(row.w_svpt) - int(row.w_1stWon) - int(row.w_2ndWon) + int(row.w_df)
                    statics['retPt'] += int(row.w_svpt)
                    statics['serGmWon'] += int(row.l_SvGms) - (int(row.l_bpFaced) - int(row.l_bpSaved))
                    statics['serGm'] += int(row.l_SvGms)
                    statics['retGmWon'] += int(row.w_bpFaced) - int(row.w_bpSaved)
                    statics['retGm'] += int(row.w_SvGms)
    return statics


def process(player_name, rank):
    statics = read_player_data(player_name, rank)
    result_list.append(statics)


if __name__ == '__main__':
    with open('./tennis_atp-master/atp_players.csv') as f:
        csvfile = csv.reader(f)
        top900_2017 = []
        with open('./tennis_atp-master/atp_rankings_current.csv') as rank_f:
            rank_csv = csv.reader(rank_f)
            for row in rank_csv:
                if row[0] == '20170206' and 100 > int(row[1]):
                    top900_2017.append({'id':row[2], 'rank':row[1]})
        for row in csvfile:
            for p in top900_2017:
                if p['id'] == row[0]:
                    name = row[1]+' '+row[2]
                    print(p['rank'])
                    process(name, p['rank'])
                    break
    with open(output_csv_name, 'w') as output_cf:
        f_csv = csv.DictWriter(output_cf, header_statics)
        f_csv.writeheader()
        f_csv.writerows(result_list)