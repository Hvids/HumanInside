class UpdateFilterModel:
    def __init__(
            self,
            path_matrix,
            name_matrix,
            name_model,
            path_model,
            maker_matrix,
            name_for_maker_model,
            maker_model

    ):
        self.name_for_maker_model = name_for_maker_model
        self.maker_model = maker_model
        self.maker_matrix = maker_matrix
        self.path_matrix = path_matrix
        self.name_matrix = name_matrix
        self.name_model = name_model
        self.path_model = path_model

    def update(self):
        df = self.maker_matrix.make(self.name_matrix)
        self.maker_matrix.save_df(df, self.path_matrix, self.name_matrix)


class UpdaterJson:
    def __init__(
            self,
            name,
            select_columns,
            maker_temp,
            maker_df,
            maker_json

    ):
        self.name = name
        self.maker_temp = maker_temp
        self.select_columns = select_columns
        self.maker_json = maker_json
        self.maker_df = maker_df

    def update(self):
        path = './recommendation_system/data/'
        df = self.maker_temp.make(self.select_columns)
        con, df = self.maker_df.make(df, load=False)

        self.maker_temp.save_df(df, path,'preprocessing_' + self.name + '.csv')
        self.maker_temp.save_df(con, path, 'content_'+'preprocessing_' + self.name + '.csv')

        res = self.maker_json.make(self.name)
        self.maker_json.save_json(res, self.name)
