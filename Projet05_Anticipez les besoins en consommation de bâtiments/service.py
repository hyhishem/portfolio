import bentoml
import numpy as np
from pydantic import BaseModel, confloat, conint


NEIGHBORHOODS = [
    "Ballard", "Central", "Delridge", "Downtown", "East",
    "Greater Duwamish", "Lake Union", "Magnolia / Queen Anne",
    "North", "Northeast", "Northwest", "Southeast", "Southwest"
]

PROPERTY_TYPES = [
    "Bureau", "Logistique", "Commerce", "Autres", "Public" ,"Soins", "Education", "Hotel" , "Restauration" ,  "Mall"
]

    
 

class ModelInput(BaseModel):
    YearBuilt: confloat(gt=0) 
    NumberofBuildings: confloat(gt=0)
    NumberofFloors: confloat(gt=0)
    PropertyUseTypeGFA: confloat(gt=0)

    NaturalGas: conint(ge=0, le=1)

    Neighborhood: str
    PropertyUseType: str



@bentoml.service
class EnergyModel:
    def __init__(self) -> None:
        self.model = bentoml.sklearn.load_model("energy_rf_model:latest")

    @bentoml.api
    def predict(self, input_data: ModelInput) -> float:


        numeric_vector = [input_data.YearBuilt, input_data.NumberofBuildings, input_data.NumberofFloors,
        input_data.PropertyUseTypeGFA, float(input_data.NaturalGas)]


        neighborhood_ohe = [1.0 if input_data.Neighborhood == n else 0.0 for n in NEIGHBORHOODS ]


        property_type_ohe = [1.0 if input_data.PropertyUseType == p else 0.0 for p in PROPERTY_TYPES]


        full_vector = np.array(numeric_vector + neighborhood_ohe + property_type_ohe, dtype=float).reshape(1, -1)


        pred = self.model.predict(full_vector)[0]
        return float(pred)
