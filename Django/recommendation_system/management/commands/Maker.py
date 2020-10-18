import pandas as pd
from tqdm import tqdm


class MakerMatrix:
    def __init__(self, User_object, Temp_object, UserTemp_object):
        self.User_object = User_object
        self.Temp_object = Temp_object
        self.UserTemp_object = UserTemp_object

    def covert_tuple(self, tuple_list):
        tuple_list = list(tuple_list)
        res = [t[0] for t in tuple_list]
        return res

    def get_score(self, id):
        score = self.UserTemp_object.objects.get(id=id).score
        if score == None:
            return 5
        else:
            return score

    def make(self, name_process=''):
        temps_id = self.Temp_object.objects.all().values_list('id')
        temps_id = self.covert_tuple(temps_id)
        users_id = self.User_object.objects.all().values_list('id')
        users_id = self.covert_tuple(users_id)
        res_values = []
        for user_id in tqdm(users_id, desc=name_process):
            select_temps = self.UserTemp_object.objects.filter(id_user=user_id).values_list('id')
            select_temps = self.covert_tuple(select_temps)
            user_values = [self.get_score(id) if id in select_temps else 0 for id in temps_id]
            res_values.append(user_values)
        df = pd.DataFrame(res_values, columns=temps_id)
        return df

    def save_df(self, df, path, name):
        df.to_csv(path + name, index=False)
