import pipeline.wrangler as wr
import pipeline.preprocess as pre
import pipeline.train as train


def main():
    """ Full training pipeline and model serialization"""
    
    precipitaciones_df, banco_central_df, milk_price_df = wr.load_data()
    precipitaciones_df, banco_central_df, milk_price_df = wr.format_data(precipitaciones_df, 
                                                                         banco_central_df, 
                                                                         milk_price_df)
    
    banco_central_df = pre.drop_duplicate_bank_rows(banco_central_df)
    banco_central_df = pre.clean_bank_num_features(banco_central_df)
    
    X, y = pre.merge_datasets(precipitaciones_df, 
                          banco_central_df, 
                          milk_price_df)
    
    train.set_numpy_seed()
    X_train, X_test, y_train, y_test = train.split_train_set(X, y)
    grid = train.find_best_model(X_train, y_train)
    train.evaluate_model(grid, X_test, y_test)
    pipe_path = train.get_final_model(grid, X_train, y_train)
    


if __name__ == '__main__':
    main()