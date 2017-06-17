import csv
from collections import namedtuple
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

output_csv_name = './tennis_atp-master/player_statics.csv'

header_pct=['playerName', 'rank',
        'avg_ace', 'p_1stInPct', 'p_2ndInPct', 'serGmWonPct',
        'retGmWonPct', 'p_1stWonPct', 'p_2ndWonPct',
        'bpSavedPct', 'bpConvertedPct', 'serPtWonPct', 'retPtWonPct']

cal = {}
cal[header_pct[3]] = lambda p_1stSerIn,serPt: p_1stSerIn/serPt
cal[header_pct[4]] = lambda p_2ndSerIn, df: p_2ndSerIn/(p_2ndSerIn+df)
cal[header_pct[5]] = lambda serGmWon, serGm: serGmWon/serGm
cal[header_pct[6]] = lambda retGmWon, retGm: retGmWon/retGm
cal[header_pct[7]] = lambda p_1stWon, p_1stSerIn: p_1stWon/p_1stSerIn
cal[header_pct[8]] = lambda p_2ndWon, p_2ndSerIn, df: p_2ndWon/(p_2ndSerIn+df)
cal[header_pct[9]] = lambda bpSaved, bpFaced: bpSaved/bpFaced
cal[header_pct[10]] = lambda bpConverted, bpGet: bpConverted/bpGet
cal[header_pct[11]] = lambda p_1stWon, p_2ndWon, serPt: (p_1stWon+p_2ndWon)/serPt
cal[header_pct[12]] = lambda retPtWon, retPt: retPtWon/retPt


def read_player_statics():
    player_statics_pct_list = []
    with open(output_csv_name) as f:
        csvfile = csv.reader(f)
        headings = next(csvfile)
        Row = namedtuple('Row', headings)
        for r in csvfile:
            def g(x):
                if x == '': return '0'
                else: return x
            row = Row(*map(g, r))
            player_statics_pct = {}
            player_statics_pct[header_pct[0]] = row.playerName
            player_statics_pct[header_pct[1]] = int(row.rank)
            player_statics_pct[header_pct[2]] = int(row.ace) / (2017-int(row.turn_pro_year))
            player_statics_pct[header_pct[3]] = cal[header_pct[3]](int(row.p_1stSerIn),int(row.serPt))
            player_statics_pct[header_pct[4]] = cal[header_pct[4]](int(row.p_2ndSerIn), int(row.df))
            player_statics_pct[header_pct[5]] = cal[header_pct[5]](int(row.serGmWon), int(row.serGm))
            player_statics_pct[header_pct[6]] = cal[header_pct[6]](int(row.retGmWon), int(row.retGm))
            player_statics_pct[header_pct[7]] = cal[header_pct[7]](int(row.p_1stWon), int(row.p_1stSerIn))
            player_statics_pct[header_pct[8]] = cal[header_pct[8]](int(row.p_2ndWon), int(row.p_2ndSerIn), int(row.df))
            player_statics_pct[header_pct[9]] = cal[header_pct[9]](int(row.bpSaved), int(row.bpFaced))
            player_statics_pct[header_pct[10]] = cal[header_pct[10]](int(row.bpConverted), int(row.bpGet))
            player_statics_pct[header_pct[11]] = cal[header_pct[11]](int(row.p_1stWon), int(row.p_2ndWon), int(row.serPt))
            player_statics_pct[header_pct[12]] = cal[header_pct[12]](int(row.retPtWon), int(row.retPt))
            player_statics_pct_list.append(player_statics_pct)

    return player_statics_pct_list

def preprocess(statics):
    retData = []
    retName = []
    for line in statics:
        retName.append(line[header_pct[0]])
        retData.append([line[header_pct[i]] for i in range(2, len(header_pct))])
    return retData, retName


if __name__ == '__main__':
    data, playerName = preprocess(read_player_statics())
    km = KMeans(n_clusters=5)
    label = km.fit_predict(data)
    NameCluster = [[],[],[],[],[]]
    for i in range(len(playerName)):
        NameCluster[label[i]].append(playerName[i])
    for i in range(len(NameCluster)):
        print('Cluster '+str(i))
        print(NameCluster[i])


    pca = PCA(n_components=2)
    reduced_stat = pca.fit_transform(data)
    red_x, red_y = [], []
    blue_x, blue_y = [], []
    green_x, green_y = [], []
    yellow_x, yellow_y = [], []
    magenta_x, magenta_y = [], []

    for i in range(len(reduced_stat)):
        if 0 == label[i]:
            red_x.append(reduced_stat[i][0])
            red_y.append(reduced_stat[i][1])
        elif 1 == label[i]:
            blue_x.append(reduced_stat[i][0])
            blue_y.append(reduced_stat[i][1])
        elif 2 == label[i]:
            green_x.append(reduced_stat[i][0])
            green_y.append(reduced_stat[i][1])
        elif 3 == label[i]:
            yellow_x.append(reduced_stat[i][0])
            yellow_y.append(reduced_stat[i][1])
        else:
            magenta_x.append(reduced_stat[i][0])
            magenta_y.append(reduced_stat[i][1])

    plt.scatter(red_x, red_y, c='r', marker='x')
    plt.scatter(blue_x, blue_y, c='b', marker='D')
    plt.scatter(green_x, green_y, c='g', marker='.')
    plt.scatter(yellow_x, yellow_y, c='y', marker='s')
    plt.scatter(magenta_x, magenta_y, c='m', marker='o')
    plt.show()