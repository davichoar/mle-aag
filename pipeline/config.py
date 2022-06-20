import pathlib
root_dir = pathlib.Path(__file__).parent.parent

# Wrangle params
DATA_PATH = f'{root_dir}/data'
PRECIP_PATH = f'{DATA_PATH}/precipitaciones.csv'
CENTRAL_BANK_PATH = f'{DATA_PATH}/banco_central.csv'
MILK_PRICE_PATH = f'{DATA_PATH}/precio_leche.csv'
PRECIP_DATE_COL = 'date'
BANK_DATE_COL = 'Periodo'
DATE_FORMAT = '%Y-%m-%d'
REPLACE_MILK_COLS = {'Anio': 'anho', 'Mes': 'mes'}
MONTH_COL = 'mes'
YEAR_COL = 'anho'

# Preprocess params
PIB_COLS = ['PIB_Agropecuario_silvicola', 'PIB_Pesca',
       'PIB_Mineria', 'PIB_Mineria_del_cobre', 'PIB_Otras_actividades_mineras',
       'PIB_Industria_Manufacturera', 'PIB_Alimentos', 'PIB_Bebidas_y_tabaco',
       'PIB_Textil', 'PIB_Maderas_y_muebles', 'PIB_Celulosa',
       'PIB_Refinacion_de_petroleo', 'PIB_Quimica',
       'PIB_Minerales_no_metalicos_y_metalica_basica',
       'PIB_Productos_metalicos', 'PIB_Electricidad', 'PIB_Construccion',
       'PIB_Comercio', 'PIB_Restaurantes_y_hoteles', 'PIB_Transporte',
       'PIB_Comunicaciones', 'PIB_Servicios_financieros',
       'PIB_Servicios_empresariales', 'PIB_Servicios_de_vivienda',
       'PIB_Servicios_personales', 'PIB_Administracion_publica',
       'PIB_a_costo_de_factores', 'PIB']

IMACEC_COLS = ['Imacec_empalmado', 'Imacec_produccion_de_bienes', 'Imacec_minero',
       'Imacec_industria', 'Imacec_resto_de_bienes', 'Imacec_comercio',
       'Imacec_servicios', 'Imacec_a_costo_de_factores', 'Imacec_no_minero']

IV_COL = 'Indice_de_ventas_comercio_real_no_durables_IVCM'
TARGET_COL = 'Precio_leche'

#Training params
SELECTOR_K_GRID = [3, 4, 5, 6, 7, 10]
REGRESSION_ALPHA_GRID = [1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
POLYNOMIAL_DEGREE_GRID = [1, 2, 3, 5, 7]

TEST_SET_SIZE = 0.2
SEED_SPLIT = 42
SEED_NUMPY = 0

CV_FOLDS = 3

ARTIFACT_PATH = 'pipeline.joblib'