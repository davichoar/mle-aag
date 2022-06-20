from pydantic import BaseModel, confloat, validator
from datetime import datetime

        
class PrecipitacionData(BaseModel):
    coquimbo: float
    valparaiso: float
    metropolitanaSantiago: float
    oHiggins: float
    maule: float
    biobio: float
    laAraucania: float
    losRios: float
    
class PIBData(BaseModel):
    agropecuarioSilvicola: int
    pesca: int
    mineria: int
    mineriaCobre: int
    otrasMineria: int
    industriaManufacturera: int
    alimentos: int
    bebidasYTabaco: int
    textil: int
    maderasYMuebles: int
    celulosa: int
    refinacionPetroleo: int
    quimica: int
    mineralesNoMetalicos: int
    productosMetalicos: int
    electricidad: int
    construccion: int
    comercio: int
    restaurantesHoteles: int
    transporte: int
    comunicaciones: int
    serviciosFinancieros: int
    serviciosEmpresariales: int
    serviciosVivienda: int
    serviciosPersonales: int
    adminPublica: int
    aCostoFactores: int
    absoluto: int

class IMACECData(BaseModel):
    empalmado: float
    produccionBienes: float
    minero: float
    industria: float
    restoBienes: float
    comercio: float
    servicio: float
    aCostoFactores: float
    noMinero: float
    

class MonthData(BaseModel):
    periodo: datetime
    precipitaciones: PrecipitacionData
    pib: PIBData
    imacec: IMACECData
    indiceVentasNoDurablesIVCM: float
    
    @validator("periodo", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(value,"%Y-%m-%d")  


class PredictResponse(BaseModel):
    precio: confloat(ge=0.0)