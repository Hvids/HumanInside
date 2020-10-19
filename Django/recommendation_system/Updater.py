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
            maker
    ):
        self.name = name
        self.maker = maker

    def update(self):
        res = self.maker.make(self.name)
        self.maker.save_json(res, self.name)
